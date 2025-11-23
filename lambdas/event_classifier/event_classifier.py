import json
import os
import boto3
from decimal import Decimal

sns_client = boto3.client('sns')
SNS_TOPIC_ARN = os.environ['SNS_TOPIC_ARN']

def lambda_handler(event, context):
    print(f"Received event: {json.dumps(event)}")
    
    for record in event.get('Records', []):
        if record['eventName'] == 'INSERT':
            new_image = record['dynamodb']['NewImage']
            process_record(new_image)
            
    return {
        'statusCode': 200,
        'body': json.dumps('Processing complete')
    }

def process_record(record):
    # DynamoDB JSON format requires parsing
    # Example structure: {'labels': {'L': [{'M': {'Name': {'S': 'Person'}, 'Confidence': {'S': '99.5'}}}]}}
    
    try:
        # Extract basic info
        image_key = record.get('image_id', {}).get('S', 'Unknown')
        timestamp = record.get('timestamp', {}).get('S', 'Unknown')
        
        # Extract labels
        labels_list = record.get('labels', {}).get('L', [])
        
        critical_events = []
        
        for item in labels_list:
            label_map = item.get('M', {})
            name = label_map.get('Name', {}).get('S', '')
            # Analyzer saves Confidence as String
            confidence_str = label_map.get('Confidence', {}).get('S', '0')
            try:
                confidence = float(confidence_str)
            except ValueError:
                confidence = 0.0
            
            # Rule 1: Person detected with high confidence
            if name == 'Person' and confidence > 90:
                critical_events.append(f"Person detected (Confidence: {confidence:.2f}%)")
                
            # Rule 2: Weapon detected
            # List of dangerous objects
            weapons = ['Weapon', 'Crowbar', 'Iron Bar', 'Rod', 'Stick', 'Tool', 'Baseball Bat', 'Hammer', 'Gun', 'Pistol', 'Rifle', 'Knife']
            if name in weapons:
                critical_events.append(f"Dangerous Object detected: {name} (Confidence: {confidence:.2f}%)")

            # Rule 3: Climbing
            if name == 'Climbing':
                critical_events.append(f"Suspicious Activity detected: Climbing (Confidence: {confidence:.2f}%)")

            # Rule 4: Hooded/Masked
            disguises = ['Hood', 'Hoodie', 'Mask', 'Balaclava', 'Helmet']
            if name in disguises:
                critical_events.append(f"Disguise detected: {name} (Confidence: {confidence:.2f}%)")
                
        if critical_events:
            publish_alert(image_key, timestamp, critical_events)
            
    except Exception as e:
        print(f"Error processing record: {e}")
        raise e

def publish_alert(image_key, timestamp, events):
    message = f"CRITICAL ALERT!\n\nImage: {image_key}\nTime: {timestamp}\n\nEvents detected:\n" + "\n".join(events)
    subject = f"SnapSentinel Alert: Critical Event Detected in {image_key}"
    
    print(f"Publishing to SNS: {subject}")
    
    sns_client.publish(
        TopicArn=SNS_TOPIC_ARN,
        Message=message,
        Subject=subject
    )
