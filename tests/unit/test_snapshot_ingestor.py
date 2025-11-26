import sys
import os
import json
import base64
import boto3
import pytest
from moto import mock_aws

# Add lambda directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../lambdas/snapshot_ingestor')))

# Set env var before import
os.environ["BUCKET_NAME"] = "test-bucket"
os.environ["AWS_DEFAULT_REGION"] = "us-east-1"

from snapshot_ingestor import lambda_handler

@pytest.fixture
def s3_setup():
    with mock_aws():
        s3 = boto3.client("s3", region_name="us-east-1")
        s3.create_bucket(Bucket="test-bucket")
        yield s3

def test_snapshot_ingestor_success(s3_setup):
    # Create a dummy image
    image_content = b"fakeimagecontent"
    image_b64 = base64.b64encode(image_content).decode("utf-8")
    
    event = {
        "body": json.dumps({
            "image": image_b64
        })
    }
    
    response = lambda_handler(event, None)
    
    assert response["statusCode"] == 200
    body = json.loads(response["body"])
    assert "file" in body
    
    # Verify S3
    s3 = boto3.client("s3", region_name="us-east-1")
    objects = s3.list_objects(Bucket="test-bucket")
    assert "Contents" in objects
    assert len(objects["Contents"]) == 1
    key = objects["Contents"][0]["Key"]
    assert key == body["file"]
