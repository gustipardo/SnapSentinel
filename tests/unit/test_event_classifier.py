import sys
import os
import json
import boto3
import pytest
from moto import mock_aws
from unittest.mock import MagicMock, patch

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../lambdas/event_classifier')))

# Set env var for import
os.environ['SNS_TOPIC_ARN'] = "arn:aws:sns:us-east-1:123456789012:test-topic"
os.environ["AWS_DEFAULT_REGION"] = "us-east-1"

import event_classifier

def test_event_classifier_critical():
    sns_mock = MagicMock()
    topic_arn = "arn:aws:sns:us-east-1:123456789012:test-topic"
    
    event = {
        "Records": [
            {
                "eventName": "INSERT",
                "dynamodb": {
                    "NewImage": {
                        "image_id": {"S": "test.jpg"},
                        "timestamp": {"S": "2023-01-01T00:00:00"},
                        "labels": {
                            "L": [
                                {
                                    "M": {
                                        "Name": {"S": "Person"},
                                        "Confidence": {"S": "95.0"}
                                    }
                                }
                            ]
                        }
                    }
                }
            }
        ]
    }
    
    with patch('event_classifier.sns_client', sns_mock), \
         patch('event_classifier.SNS_TOPIC_ARN', topic_arn):
         
        event_classifier.lambda_handler(event, None)
        
        sns_mock.publish.assert_called_once()
        call_args = sns_mock.publish.call_args[1]
        assert call_args['TopicArn'] == topic_arn
        assert "CRITICAL ALERT" in call_args['Message']
        assert "Person detected" in call_args['Message']

def test_event_classifier_no_critical():
    sns_mock = MagicMock()
    topic_arn = "arn:aws:sns:us-east-1:123456789012:test-topic"
    
    event = {
        "Records": [
            {
                "eventName": "INSERT",
                "dynamodb": {
                    "NewImage": {
                        "image_id": {"S": "test.jpg"},
                        "timestamp": {"S": "2023-01-01T00:00:00"},
                        "labels": {
                            "L": [
                                {
                                    "M": {
                                        "Name": {"S": "Cat"},
                                        "Confidence": {"S": "95.0"}
                                    }
                                }
                            ]
                        }
                    }
                }
            }
        ]
    }
    
    with patch('event_classifier.sns_client', sns_mock), \
         patch('event_classifier.SNS_TOPIC_ARN', topic_arn):
         
        event_classifier.lambda_handler(event, None)
        
        sns_mock.publish.assert_not_called()
