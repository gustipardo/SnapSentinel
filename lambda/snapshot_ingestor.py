import boto3 # AWS SDK
import json
import base64
import uuid
from datetime import datetime
import os

# Initialize the S3 client
s3 = boto3.client("s3")
BUCKET = os.environ["BUCKET_NAME"]

def lambda_handler(event, context): # event has Api Gateway request data
    try:
        body = json.loads(event["body"])
        image_data = base64.b64decode(body["image"])
        file_name = f"{datetime.utcnow().isoformat()}_{uuid.uuid4()}.jpg"
        
        s3.put_object(
            Bucket=BUCKET,
            Key=file_name,
            Body=image_data,
            ContentType="image/jpeg"
        )

        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Snapshot received", "file": file_name})
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
