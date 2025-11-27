import pytest
import boto3
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def pytest_addoption(parser):
    parser.addoption(
        "--keep-resources", action="store_true", default=False, help="Do not delete resources created during tests"
    )

@pytest.fixture(scope="session")
def keep_resources(request):
    return request.config.getoption("--keep-resources")

@pytest.fixture(scope="session")
def env():
    return os.environ.get("ENV", "dev")

@pytest.fixture(scope="session")
def region():
    return os.environ.get("AWS_REGION", "us-east-1")

@pytest.fixture(scope="session")
def s3_client(region):
    return boto3.client("s3", region_name=region)

@pytest.fixture(scope="session")
def dynamodb_client(region):
    return boto3.client("dynamodb", region_name=region)

@pytest.fixture(scope="session")
def logs_client(region):
    return boto3.client("logs", region_name=region)

@pytest.fixture(scope="session")
def apigateway_client(region):
    return boto3.client("apigateway", region_name=region)

@pytest.fixture(scope="session")
def bucket_name(env):
    return f"snapsentinel-images-{env}"

@pytest.fixture(scope="session")
def table_name(env):
    return f"analysis_results-{env}"

@pytest.fixture(scope="session")
def api_url(apigateway_client, env, region):
    """
    Dynamically fetches the API Gateway URL for the given environment.
    Looks for an API named 'snapshot-api-{env}'.
    """
    api_name = f"snapshot-api-{env}"
    apis = apigateway_client.get_rest_apis()
    
    api_id = None
    for item in apis.get("items", []):
        if item["name"] == api_name:
            api_id = item["id"]
            break
    
    if not api_id:
        pytest.fail(f"API Gateway with name '{api_name}' not found.")
        
    url = f"https://{api_id}.execute-api.{region}.amazonaws.com/{env}/snapshot"
    logger.info(f"Discovered API URL: {url}")
    return url

@pytest.fixture(scope="session")
def log_group_name(env):
    return f"/aws/lambda/event_classifier-{env}"
