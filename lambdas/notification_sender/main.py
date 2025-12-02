import json
import os
import logging
import base64
from google.oauth2 import service_account
from google.auth.transport.requests import Request
import requests

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Environment variables
FCM_CLIENT_EMAIL = os.environ.get('FCM_CLIENT_EMAIL')
FCM_PRIVATE_KEY = os.environ.get('FCM_PRIVATE_KEY')
FCM_PROJECT_ID = os.environ.get('FCM_PROJECT_ID')
SCOPES = ['https://www.googleapis.com/auth/firebase.messaging']

def get_access_token():
    """Retrieves a valid OAuth2 access token for FCM."""
    try:
        # Handle potential newline characters in private key
        private_key = FCM_PRIVATE_KEY.replace('\\n', '\n') if FCM_PRIVATE_KEY else None
        
        credentials = service_account.Credentials.from_service_account_info(
            {
                "client_email": FCM_CLIENT_EMAIL,
                "private_key": private_key,
                "project_id": FCM_PROJECT_ID,
                "token_uri": "https://oauth2.googleapis.com/token",
            },
            scopes=SCOPES
        )
        credentials.refresh(Request())
        logger.info("Token obtained successfully")
        return credentials.token
    except Exception as e:
        logger.error(f"Error obtaining access token: {e}")
        raise

def send_fcm_message(access_token, data):
    """Sends a message to FCM v1 API."""
    url = f'https://fcm.googleapis.com/v1/projects/{FCM_PROJECT_ID}/messages:send'
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    
    # Construct the message payload
    # Note: 'data' fields must be strings
    message = {
        "message": {
            "topic": "all_devices",
            "data": {
                "type": str(data.get("type", "")),
                "status": str(data.get("status", "")),
                "image_id": str(data.get("image_id", "")),
                "timestamp": str(data.get("timestamp", "")),
                "title": str(data.get("title", "")),
                "body": str(data.get("body", ""))
            }
        }
    }

    try:
        response = requests.post(url, headers=headers, json=message)
        if response.status_code == 200:
            logger.info(f"FCM Response: {response.status_code}")
            logger.info(f"Message sent successfully: {response.json()}")
        else:
            logger.error(f"FCM Error: {response.status_code} - {response.text}")
            raise Exception(f"FCM API returned {response.status_code}")
    except Exception as e:
        logger.error(f"Error sending FCM message: {e}")
        raise

def lambda_handler(event, context):
    """Lambda entry point."""
    try:
        logger.info(f"Received event: {json.dumps(event)}")
        
        # Parse SNS message
        sns_message = event['Records'][0]['Sns']['Message']
        payload = json.loads(sns_message)
        
        logger.info(f"Parsed payload: {json.dumps(payload)}")
        
        # Get Access Token
        access_token = get_access_token()
        
        # Send Notification
        send_fcm_message(access_token, payload)
        
        return {
            'statusCode': 200,
            'body': json.dumps('Notification sent successfully')
        }
        
    except Exception as e:
        logger.error(f"Lambda execution failed: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error: {str(e)}')
        }
