import pytest
import boto3
import time
import os
from botocore.exceptions import ClientError

def test_s3_trigger_analysis(s3_client, dynamodb_client, bucket_name, table_name, keep_resources):
    """
    Stage 2 Integration Test:
    1. Upload image to S3.
    2. Poll DynamoDB for analysis result.
    """
    image_id = f"test-stage2-{int(time.time())}.jpg"
    image_path = os.path.join(os.path.dirname(__file__), "../assets/image.png")
    
    if not os.path.exists(image_path):
        pytest.fail(f"Test image not found at {image_path}")

    print(f"Uploading {image_id} to {bucket_name}...")
    s3_client.upload_file(image_path, bucket_name, image_id)

    # Poll DynamoDB
    print(f"Polling DynamoDB table {table_name} for image_id {image_id}...")
    found = False
    retries = 10
    
    for i in range(retries):
        try:
            # Query by Partition Key (image_id)
            response = dynamodb_client.query(
                TableName=table_name,
                KeyConditionExpression="image_id = :id",
                ExpressionAttributeValues={":id": {"S": image_id}}
            )
            
            if response["Count"] > 0:
                print(f"Record found: {response['Items'][0]}")
                found = True
                break
        except ClientError as e:
            print(f"Error querying DynamoDB: {e}")
        
        time.sleep(2)
        
    assert found, f"Record for {image_id} not found in DynamoDB after {retries*2} seconds."

    # Cleanup
    if not keep_resources:
        print("Cleaning up resources...")
        s3_client.delete_object(Bucket=bucket_name, Key=image_id)
        # We should also delete the DynamoDB record, but we need the Sort Key (timestamp)
        # The query response has it.
        if found:
            items = response['Items']
            for item in items:
                timestamp = item['timestamp']['S']
                dynamodb_client.delete_item(
                    TableName=table_name,
                    Key={"image_id": {"S": image_id}, "timestamp": {"S": timestamp}}
                )
    else:
        print("Skipping cleanup (--keep-resources set)")
