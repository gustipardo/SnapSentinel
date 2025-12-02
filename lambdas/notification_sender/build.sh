#!/bin/bash
set -e

# Create Layer package
rm -rf layer
mkdir -p layer/python

pip install google-auth requests -t layer/python
cd layer
zip -r ../../../terraform/stages/3_classification/google_auth_layer.zip .
cd ..

# Create function zip
zip ../../terraform/stages/3_classification/notification_sender.zip notification_sender.py

# Clean up
rm -rf layer
