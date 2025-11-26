#!/bin/bash

# Load environment variables if needed
# source ../step1/test.env

TABLE_NAME="analysis_results-dev"
TIMESTAMP=$(date +%s)

echo "Inserting SAFE record (No Alert expected)..."
aws dynamodb put-item \
    --table-name "$TABLE_NAME" \
    --item '{
        "image_id": {"S": "safe_test_image.jpg"},
        "timestamp": {"S": "'"$TIMESTAMP"'"},
        "labels": {"L": [
            {"M": {"Name": {"S": "Tree"}, "Confidence": {"S": "99.9"}}}
        ]}
    }' \
    --region us-east-1

echo "Inserted safe record."

echo "Inserting CRITICAL record (Person > 90% - Alert expected)..."
aws dynamodb put-item \
    --table-name "$TABLE_NAME" \
    --item '{
        "image_id": {"S": "critical_test_image.jpg"},
        "timestamp": {"S": "'"$TIMESTAMP"'"},
        "labels": {"L": [
            {"M": {"Name": {"S": "Person"}, "Confidence": {"S": "95.5"}}}
        ]}
    }' \
    --region us-east-1

echo "Inserted critical record."

echo "Please check the email sandbox17201@gmail.com for the alert."
echo "You can also check CloudWatch Logs for the Lambda function 'EventClassifier'."
