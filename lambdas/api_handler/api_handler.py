import json
import os
import boto3
import base64
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
TABLE_NAME = os.environ['DYNAMODB_TABLE']
table = dynamodb.Table(TABLE_NAME)

def lambda_handler(event, context):
    print(f"Received event: {json.dumps(event)}")
    
    try:
        query_params = event.get('queryStringParameters', {}) or {}
        limit = int(query_params.get('limit', 20))
        next_token = query_params.get('next_page_token')
        
        query_kwargs = {
            'IndexName': 'AlertsByIndex',
            'KeyConditionExpression': Key('status').eq('ALERT'),
            'ScanIndexForward': False, # Descending order (newest first)
            'Limit': limit
        }
        
        if next_token:
            try:
                decoded_key = json.loads(base64.b64decode(next_token).decode('utf-8'))
                query_kwargs['ExclusiveStartKey'] = decoded_key
            except Exception as e:
                print(f"Invalid next_token: {e}")
                return {
                    'statusCode': 400,
                    'body': json.dumps({'error': 'Invalid next_page_token'})
                }
        
        response = table.query(**query_kwargs)
        
        items = response.get('Items', [])
        last_evaluated_key = response.get('LastEvaluatedKey')
        
        # Format items
        formatted_items = []
        for item in items:
            formatted_items.append({
                'id': item.get('image_id'),
                'timestamp': item.get('timestamp'),
                'labels': item.get('labels'),
                'status': item.get('status')
            })
            
        response_body = {
            'items': formatted_items
        }
        
        if last_evaluated_key:
            encoded_key = base64.b64encode(json.dumps(last_evaluated_key).encode('utf-8')).decode('utf-8')
            response_body['next_page_token'] = encoded_key
            
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': json.dumps(response_body, default=str)
        }
        
    except Exception as e:
        print(f"Error: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
