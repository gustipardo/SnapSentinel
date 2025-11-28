import pytest
import boto3
import requests
import time
import os

@pytest.fixture
def api_endpoint():
    client = boto3.client('apigatewayv2', region_name='us-east-1')
    apis = client.get_apis()
    for api in apis['Items']:
        if api['Name'] == 'snapsentinel-api-dev':
            return api['ApiEndpoint']
    pytest.skip("API Endpoint not found")

@pytest.fixture
def dynamodb_table():
    return boto3.resource('dynamodb', region_name='us-east-1').Table('analysis_results-dev')

def test_get_alerts(api_endpoint, dynamodb_table):
    # Insert a fake alert
    timestamp = str(int(time.time()))
    image_id = f"api-test-{timestamp}.jpg"
    
    print(f"Inserting alert for {image_id}...")
    dynamodb_table.put_item(Item={
        "image_id": image_id,
        "timestamp": timestamp,
        "status": "ALERT",
        "labels": {"L": [{"M": {"Name": {"S": "Test"}, "Confidence": {"S": "100"}}}]}
    })
    
    # Wait for consistency (GSI might take a moment)
    time.sleep(5)
    
    # Call API
    url = f"{api_endpoint}/alerts"
    print(f"Calling {url}...")
    response = requests.get(url)
    
    assert response.status_code == 200
    data = response.json()
    
    # Verify our item is in the list
    found = False
    for item in data['items']:
        if item['id'] == image_id:
            found = True
            break
            
    assert found, f"Alert {image_id} not found in API response"
    
    # Cleanup
    dynamodb_table.delete_item(Key={"image_id": image_id, "timestamp": timestamp})
