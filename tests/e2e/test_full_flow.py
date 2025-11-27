import pytest
import requests
import boto3
import time
import os
import base64

def test_e2e_critical_flow(api_url, s3_client, bucket_name, dynamodb_client, table_name, logs_client, log_group_name, keep_resources):
    """
    E2E Test:
    1. Send a known 'Critical' image to API Gateway.
    2. Poll CloudWatch Logs for the 'Publishing to SNS' message.
    3. Cleanup resources (S3 object and DynamoDB record) unless --keep-resources is set.
    """
    # Use a known critical image (e.g. one that Rekognition will classify as Person/Hoodie/Weapon)
    # For this test, we'll use 'encapuchado_espalda.png' if available, or fallback to a generic one
    # and rely on the fact that we can't easily force Rekognition to see something unless the image is real.
    # However, for the purpose of this test, we assume the image provided IS critical.
    
    image_filename = "encapuchado_espalda.png"
    image_path = os.path.join(os.path.dirname(__file__), f"../images/{image_filename}")
    
    if not os.path.exists(image_path):
        # Fallback to step1 image if specific one not found, though it might not trigger the alert
        # This is a risk. Let's try to find any image.
        image_path = os.path.join(os.path.dirname(__file__), "../step1/image.jpeg")
        if not os.path.exists(image_path):
             pytest.fail("No test image found.")
        print(f"Warning: Using fallback image {image_path}. This might not trigger the critical alert if Rekognition doesn't see a threat.")

    print(f"Using image: {image_path}")
    
    with open(image_path, "rb") as f:
        image_data = f.read()
        
    encoded_image = base64.b64encode(image_data).decode("utf-8")

    # 1. Send to API Gateway
    print(f"Sending request to {api_url}...")
    response = requests.post(
        api_url,
        json={"image": encoded_image}
    )
    
    assert response.status_code == 200, f"API Request failed: {response.text}"
    response_json = response.json()
    file_key = response_json["file"]
    print(f"Uploaded file key: {file_key}")

    # 2. Poll CloudWatch Logs
    print(f"Polling CloudWatch Logs {log_group_name} for SNS publication...")
    
    # It takes time for:
    # API -> S3 (fast)
    # S3 -> Analyzer Lambda (fast)
    # Analyzer -> Rekognition -> DynamoDB (few seconds)
    # DynamoDB Stream -> Classifier Lambda (few seconds)
    
    # We'll wait up to 30 seconds
    found_log = False
    retries = 10
    start_time = int(time.time()) * 1000
    
    # Initial wait for pipeline to start
    time.sleep(5)
    
    for i in range(retries):
        try:
            # We look for the file_key in the logs, and "Publishing to SNS"
            # The classifier logs: "Publishing to SNS: SnapSentinel Alert: Critical Event Detected in {image_key}"
            
            response = logs_client.filter_log_events(
                logGroupName=log_group_name,
                startTime=start_time - 10000,
                filterPattern=f'"{file_key}"'
            )
            
            for event in response.get("events", []):
                message = event["message"]
                if "Publishing to SNS" in message:
                    print(f"Found confirmation log: {message}")
                    found_log = True
                    break
            
            if found_log:
                break
                
        except logs_client.exceptions.ResourceNotFoundException:
            print("Log group not found yet (Lambda might not have run).")
        except Exception as e:
            print(f"Error querying logs: {e}")
            
        print(f"Waiting... ({i+1}/{retries})")
        time.sleep(3)
        
    assert found_log, f"E2E Failed: Did not find SNS publication log for {file_key} in {log_group_name}. Pipeline might have failed or image was not deemed critical."

    # 3. Cleanup resources
    if not keep_resources:
        print("Cleaning up test resources...")
        
        # Delete S3 object
        try:
            print(f"Deleting S3 object: {file_key} from bucket {bucket_name}")
            s3_client.delete_object(Bucket=bucket_name, Key=file_key)
            print("S3 object deleted successfully")
        except Exception as e:
            print(f"Warning: Failed to delete S3 object: {e}")
        
        # Delete DynamoDB record
        try:
            print(f"Deleting DynamoDB record for image_id: {file_key}")
            # First, query to get the timestamp (sort key)
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

