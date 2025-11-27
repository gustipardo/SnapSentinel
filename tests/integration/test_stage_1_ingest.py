import pytest
import requests
import os
import boto3
import time

def test_api_gateway_upload(api_url, s3_client, bucket_name, dynamodb_client, table_name, keep_resources):
    """
    Stage 1 Integration Test:
    1. Send image to API Gateway.
    2. Verify image is uploaded to S3.
    
    Note: Even though DynamoDB is out of scope for Stage 1, the deployed system
    automatically triggers the full pipeline (S3 -> Analyzer Lambda -> DynamoDB),
    so we need to clean up the DynamoDB record as well.
    """
    # Use an existing test image
    image_path = os.path.join(os.path.dirname(__file__), "../assets/image.jpeg")
    
    # If image doesn't exist (e.g. running from different cwd), try to find it or skip
    if not os.path.exists(image_path):
        # Fallback to creating a dummy image if needed, or fail
        pytest.fail(f"Test image not found at {image_path}")

    with open(image_path, "rb") as f:
        image_data = f.read()

    # Send POST request
    print(f"Sending request to {api_url}...")

    
    # Wait, I need to encode it to base64 first!
    import base64
    encoded_image = base64.b64encode(image_data).decode("utf-8")
    
    response = requests.post(
        api_url,
        json={"image": encoded_image}
    )

    assert response.status_code == 200, f"API Request failed: {response.text}"
    response_json = response.json()
    assert "file" in response_json
    file_key = response_json["file"]
    print(f"Uploaded file key: {file_key}")

    # Verify in S3
    print(f"Verifying object {file_key} in bucket {bucket_name}...")
    # Give it a moment just in case (though API usually returns after S3 put)
    time.sleep(1)
    
    try:
        s3_client.head_object(Bucket=bucket_name, Key=file_key)
        print("Object found in S3.")
    except Exception as e:
        pytest.fail(f"Object {file_key} not found in S3: {e}")

    # Cleanup
    if not keep_resources:
        print("Cleaning up resources...")
        
        # Delete S3 object
        print(f"Deleting S3 object: {file_key}")
        s3_client.delete_object(Bucket=bucket_name, Key=file_key)
        
        # Delete DynamoDB record (created automatically by Analyzer Lambda)
        # We need to wait a bit for the Lambda to finish processing
        print("Waiting for Analyzer Lambda to process and create DynamoDB record...")
        time.sleep(3)
        
        try:
            print(f"Deleting DynamoDB record for image_id: {file_key}")
            # Query to get the timestamp (sort key)
            response = dynamodb_client.query(
                TableName=table_name,
                KeyConditionExpression="image_id = :id",
                ExpressionAttributeValues={":id": {"S": file_key}}
            )
            
            if response["Count"] > 0:
                items = response['Items']
                for item in items:
                    timestamp = item['timestamp']['S']
                    dynamodb_client.delete_item(
                        TableName=table_name,
                        Key={
                            "image_id": {"S": file_key},
                            "timestamp": {"S": timestamp}
                        }
                    )
                    print(f"DynamoDB record deleted successfully (timestamp: {timestamp})")
            else:
                print(f"Warning: No DynamoDB record found for image_id: {file_key}")
        except Exception as e:
            print(f"Warning: Failed to delete DynamoDB record: {e}")
    else:
        print("Skipping cleanup (--keep-resources set)")

