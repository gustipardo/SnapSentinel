import pytest
import boto3
import json
import os
from moto import mock_aws

# Set env vars before importing the lambda
os.environ["AWS_ACCESS_KEY_ID"] = "testing"
os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
os.environ["AWS_SECURITY_TOKEN"] = "testing"
os.environ["AWS_SESSION_TOKEN"] = "testing"
os.environ["AWS_DEFAULT_REGION"] = "us-east-1"
os.environ["DYNAMODB_TABLE"] = "analysis_results-test"

from lambdas.api_handler import api_handler

@mock_aws
def test_api_handler_success():
    # Setup DynamoDB
    dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
    table = dynamodb.create_table(
        TableName="analysis_results-test",
        KeySchema=[{"AttributeName": "image_id", "KeyType": "HASH"}, {"AttributeName": "timestamp", "KeyType": "RANGE"}],
        AttributeDefinitions=[
            {"AttributeName": "image_id", "AttributeType": "S"},
            {"AttributeName": "timestamp", "AttributeType": "S"},
            {"AttributeName": "status", "AttributeType": "S"}
        ],
        GlobalSecondaryIndexes=[
            {
                "IndexName": "AlertsByIndex",
                "KeySchema": [{"AttributeName": "status", "KeyType": "HASH"}, {"AttributeName": "timestamp", "KeyType": "RANGE"}],
                "Projection": {"ProjectionType": "ALL"}
            }
        ],
        BillingMode="PAY_PER_REQUEST"
    )
    
    # Insert test data
    table.put_item(Item={
        "image_id": "img1",
        "timestamp": "2023-01-01T10:00:00Z",
        "status": "ALERT",
        "labels": {"L": [{"M": {"Name": {"S": "Person"}, "Confidence": {"S": "99.0"}}}]}
    })
    table.put_item(Item={
        "image_id": "img2",
        "timestamp": "2023-01-01T11:00:00Z",
        "status": "OK",
        "labels": {"L": []}
    })
    
    # Call Lambda
    event = {}
    response = api_handler.lambda_handler(event, None)
    
    assert response["statusCode"] == 200
    body = json.loads(response["body"])
    assert len(body["items"]) == 1
    assert body["items"][0]["id"] == "img1"

@mock_aws
def test_api_handler_pagination():
    # Setup DynamoDB
    dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
    table = dynamodb.create_table(
        TableName="analysis_results-test",
        KeySchema=[{"AttributeName": "image_id", "KeyType": "HASH"}, {"AttributeName": "timestamp", "KeyType": "RANGE"}],
        AttributeDefinitions=[
            {"AttributeName": "image_id", "AttributeType": "S"},
            {"AttributeName": "timestamp", "AttributeType": "S"},
            {"AttributeName": "status", "AttributeType": "S"}
        ],
        GlobalSecondaryIndexes=[
            {
                "IndexName": "AlertsByIndex",
                "KeySchema": [{"AttributeName": "status", "KeyType": "HASH"}, {"AttributeName": "timestamp", "KeyType": "RANGE"}],
                "Projection": {"ProjectionType": "ALL"}
            }
        ],
        BillingMode="PAY_PER_REQUEST"
    )
    
    # Insert test data (3 items)
    for i in range(3):
        table.put_item(Item={
            "image_id": f"img{i}",
            "timestamp": f"2023-01-01T10:00:0{i}Z",
            "status": "ALERT",
            "labels": {"L": []}
        })
        
    # Call Lambda with limit 2
    event = {"queryStringParameters": {"limit": "2"}}
    response = api_handler.lambda_handler(event, None)
    
    assert response["statusCode"] == 200
    body = json.loads(response["body"])
    assert len(body["items"]) == 2
    assert "next_page_token" in body
    
    # Call Lambda with next_page_token
    event = {"queryStringParameters": {"limit": "2", "next_page_token": body["next_page_token"]}}
    response = api_handler.lambda_handler(event, None)
    
    assert response["statusCode"] == 200
    body = json.loads(response["body"])
    assert len(body["items"]) == 1
