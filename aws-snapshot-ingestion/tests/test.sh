#!/bin/bash

# Define the path to the .env file.
# Since test.sh is in the 'tests' directory, and .env is in the parent directory,
# the relative path is '../.env'.
ENV_FILE="../.env"

# Load variables from the .env file
# This reads the file and exports its variables to the script's environment.
if [ -f "$ENV_FILE" ]; then
    source "$ENV_FILE"
else
    echo "Error: The .env file was not found at $ENV_FILE"
    exit 1
fi

# Define the image path, which is local to the parent directory.
IMAGE_PATH="../comiendo_filtered.jpeg"

echo "Sending snapshot to the endpoint: $API_URL"

# Create temporary file with the JSON
TMP_JSON=$(mktemp)
{
  echo -n '{"image":"'
  base64 "$IMAGE_PATH" | tr -d '\n'
  echo '"}'
} > "$TMP_JSON"

RESPONSE=$(curl -s -X POST "$API_URL" \
  -H "Content-Type: application/json" \
  -d @"$TMP_JSON")

echo "Endpoint response:"
echo "$RESPONSE"

# Delete temporary file
rm "$TMP_JSON"