import json
import logging
import boto3
import datetime

logger = logging.getLogger()
logger.setLevel(logging.INFO)

rekognition = boto3.client('rekognition')
s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('analysis_results')

def lambda_handler(event, context):
    """
    Lambda function to handle S3 events and analyze images with Rekognition.
    """
    logger.info("Received event: " + json.dumps(event, indent=2))
    
    try:
        for record in event['Records']:
            bucket = record['s3']['bucket']['name']
            key = record['s3']['object']['key']
            
            # --- Step 1: Get Image Info ---
            logger.info(f"--- Step 1: Getting Image Info for s3://{bucket}/{key} ---")
            try:
                metadata = s3.head_object(Bucket=bucket, Key=key)
                size = metadata['ContentLength']
                content_type = metadata['ContentType']
                logger.info(f"Image Name: {key}")
                logger.info(f"Image Size: {size} bytes")
                logger.info(f"Content Type: {content_type}")
            except Exception as e:
                logger.error(f"Failed at Step 1 (Get Image Info): {str(e)}")
                raise e

            # --- Step 2: Rekognition Analysis ---
            logger.info("--- Step 2: Calling Rekognition DetectLabels ---")
            try:
                response = rekognition.detect_labels(
                    Image={
                        'S3Object': {
                            'Bucket': bucket,
                            'Name': key
                        }
                    },
                    MaxLabels=10,
                    MinConfidence=70
                )
                
                labels = []
                for label in response['Labels']:
                    labels.append({
                        'Name': label['Name'],
                        'Confidence': str(label['Confidence'])
                    })
                logger.info(f"Detected Labels: {json.dumps(labels)}")
            except Exception as e:
                logger.error(f"Failed at Step 2 (Rekognition): {str(e)}")
                raise e

            # --- Step 3: Save to DynamoDB ---
            logger.info("--- Step 3: Saving to DynamoDB ---")
            try:
                timestamp = datetime.datetime.now().isoformat()
                item = {
                    'image_id': key,
                    'timestamp': timestamp,
                    'bucket': bucket,
                    'labels': labels,
                    'size': size, # Added size to DB record
                    'content_type': content_type
                }
                
                table.put_item(Item=item)
                logger.info(f"Successfully saved item to DynamoDB: {key}")
                logger.info(f"Record: {json.dumps(item)}")
            except Exception as e:
                logger.error(f"Failed at Step 3 (DynamoDB): {str(e)}")
                raise e

    except Exception as e:
        logger.error(f"Error processing event: {str(e)}")
        raise e
        
    return {
        'statusCode': 200,
        'body': json.dumps('Image analysis complete')
    }
