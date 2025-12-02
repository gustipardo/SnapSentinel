import boto3
import json
import time
import uuid

def verify_notification():
    dynamodb = boto3.client('dynamodb', region_name='us-east-1')
    logs = boto3.client('logs', region_name='us-east-1')
    
    table_name = 'analysis_results-dev'
    image_id = f"test-image-{uuid.uuid4()}"
    timestamp = str(int(time.time()))
    
    print(f"Inserting test record into {table_name}...")
    
    # Insert a record that should trigger the event classifier
    # Rule: Person with Confidence > 90
    item = {
        'image_id': {'S': image_id},
        'timestamp': {'S': timestamp},
        'labels': {
            'L': [
                {
                    'M': {
                        'Name': {'S': 'Person'},
                        'Confidence': {'S': '99.9'}
                    }
                }
            ]
        },
        'status': {'S': 'ANALYZED'} # Initial status
    }
    
    try:
        dynamodb.put_item(TableName=table_name, Item=item)
        print("Record inserted successfully.")
    except Exception as e:
        print(f"Error inserting record: {e}")
        return

    print("Waiting for Lambda execution (10s)...")
    time.sleep(10)
    
    # Check CloudWatch Logs for notification_sender
    log_group_name = '/aws/lambda/notification_sender-dev'
    print(f"Checking logs in {log_group_name}...")
    
    try:
        # Get the latest log stream
        response = logs.describe_log_streams(
            logGroupName=log_group_name,
            orderBy='LastEventTime',
            descending=True,
            limit=1
        )
        
        if not response['logStreams']:
            print("No log streams found.")
            return

        log_stream_name = response['logStreams'][0]['logStreamName']
        
        # Get log events
        events = logs.get_log_events(
            logGroupName=log_group_name,
            logStreamName=log_stream_name,
            limit=20
        )
        
        found_token = False
        found_response = False
        
        for event in events['events']:
            message = event['message']
            if "Token obtained successfully" in message:
                found_token = True
                print("✅ Found: Token obtained successfully")
            if "FCM Response: 200" in message:
                found_response = True
                print("✅ Found: FCM Response: 200")
                
        if found_token and found_response:
            print("SUCCESS: Notification flow verified!")
        else:
            print("FAILURE: Could not find expected log messages.")
            print("Last logs:")
            for event in events['events']:
                print(event['message'].strip())
                
    except Exception as e:
        print(f"Error checking logs: {e}")

if __name__ == "__main__":
    verify_notification()
