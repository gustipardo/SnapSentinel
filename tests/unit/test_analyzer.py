import sys
import os
import json
import boto3
import pytest
from moto import mock_aws
from unittest.mock import MagicMock, patch

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../lambdas/analyzer')))

# Set env var for import
os.environ["DYNAMODB_TABLE_NAME"] = "test-table"
os.environ["AWS_DEFAULT_REGION"] = "us-east-1"

import analyzer

@pytest.fixture
def aws_setup():
    with mock_aws():
        s3 = boto3.client("s3", region_name="us-east-1")
        s3.create_bucket(Bucket="test-bucket")
        
        dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
        table = dynamodb.create_table(
            TableName="test-table",
            KeySchema=[{'AttributeName': 'image_id', 'KeyType': 'HASH'}],
            AttributeDefinitions=[{'AttributeName': 'image_id', 'AttributeType': 'S'}],
            ProvisionedThroughput={'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
        )
        
        yield s3, table

def test_analyzer_success(aws_setup):
    s3, table = aws_setup
    
    # Upload file
    key = "test.jpg"
    s3.put_object(Bucket="test-bucket", Key=key, Body=b"image", ContentType="image/jpeg")
    
    event = {
        "Records": [
            {
                "s3": {
                    "bucket": {"name": "test-bucket"},
                    "object": {"key": key}
                }
            }
        ]
    }
    
    # Mock Rekognition
    rekognition_mock = MagicMock()
    rekognition_mock.detect_labels.return_value = {
        'Labels': [
            {'Name': 'Person', 'Confidence': 99.5},
            {'Name': 'Dog', 'Confidence': 80.0}
        ]
    }
    
    # Patch the clients in the module
    with patch('analyzer.s3', s3), \
         patch('analyzer.rekognition', rekognition_mock), \
         patch('analyzer.table', table):
         
        response = analyzer.lambda_handler(event, None)
        
        assert response['statusCode'] == 200
        
        # Verify DynamoDB
        item = table.get_item(Key={'image_id': key})
        assert 'Item' in item
        assert item['Item']['image_id'] == key
        assert len(item['Item']['labels']) == 2
        assert item['Item']['labels'][0]['Name'] == 'Person'
