import pytest
import boto3
import time
import json

def test_dynamodb_trigger_classification(dynamodb_client, logs_client, table_name, log_group_name, keep_resources):
    """
    Stage 3 Integration Test:
    1. Insert 'Critical' record into DynamoDB.
    2. Verify 'Publishing to SNS' log in CloudWatch Logs.
    """
    timestamp = str(int(time.time()))
    image_id = f"critical-test-{timestamp}.jpg"
    
    print(f"Inserting critical record for {image_id} into {table_name}...")
    
    # Insert a record that should trigger an alert (Person > 90%)
    dynamodb_client.put_item(
        TableName=table_name,
        Item={
            "image_id": {"S": image_id},
            "timestamp": {"S": timestamp},
            "labels": {"L": [
                {"M": {"Name": {"S": "Person"}, "Confidence": {"S": "95.5"}}}
            ]}
        }
    )

    print(f"Polling CloudWatch Logs {log_group_name} for confirmation...")
    
    # Wait for Lambda to execute and logs to appear
    time.sleep(5) 
    
    found_log = False
    retries = 10
    
    start_time = int(time.time()) * 1000 # milliseconds
    
    for i in range(retries):
        try:
            # Filter logs for the specific image_id or "Publishing to SNS"
            # We look for "Publishing to SNS" and the image_id in the same log stream or time window?
            # The code prints: f"Publishing to SNS: {subject}"
            # And subject contains image_key.
            
            response = logs_client.filter_log_events(
                logGroupName=log_group_name,
                startTime=start_time - 10000, # Look back 10s just in case
                filterPattern=f'"{image_id}"' # Simple filter for the image ID
            )
            
            for event in response.get("events", []):
                message = event["message"]
                if "Publishing to SNS" in message:
                    print(f"Found log: {message}")
                    found_log = True
                    break
            
            if found_log:
                break
                
        except logs_client.exceptions.ResourceNotFoundException:
            print("Log group not found yet...")
        except Exception as e:
            print(f"Error querying logs: {e}")
            
        time.sleep(3)
        
    assert found_log, f"Did not find SNS publication log for {image_id} in {log_group_name}"

    # Cleanup
    if not keep_resources:
        print("Cleaning up DynamoDB record...")
        dynamodb_client.delete_item(
            TableName=table_name,
            Key={"image_id": {"S": image_id}, "timestamp": {"S": timestamp}}
        )
    else:
        print("Skipping cleanup (--keep-resources set)")
