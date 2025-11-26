# Verification: Phase 3 - Detailed Testing Strategy

## Changes Made
- Created directory structure:
    - `tests/unit/`
    - `tests/integration/`
    - `tests/e2e/`
- Implemented unit tests in `tests/unit/`:
    - `test_snapshot_ingestor.py`: Tests `snapshot_ingestor` lambda with Moto S3.
    - `test_analyzer.py`: Tests `analyzer` lambda with Moto S3/DynamoDB and Mock Rekognition.
    - `test_event_classifier.py`: Tests `event_classifier` lambda with Mock SNS.
- Created `tests/requirements.txt` with testing dependencies.

## Verification Results
Ran `pytest` in a virtual environment.

```bash
$ .venv/bin/pytest tests/unit
================================ test session starts =================================
platform linux -- Python 3.12.3, pytest-8.3.4, pluggy-1.5.0
rootdir: /home/gustipardo/Projects/SnapSentinel
collected 4 items

tests/unit/test_analyzer.py .                                                  [ 25%]
tests/unit/test_event_classifier.py ..                                         [ 75%]
tests/unit/test_snapshot_ingestor.py .                                         [100%]

================================= 4 passed in 0.46s ==================================
```

## How to Run Tests
1. Create and activate a virtual environment (if not already done):
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
2. Install dependencies:
   ```bash
   pip install -r tests/requirements.txt
   ```
3. Run tests:
   ```bash
   pytest tests/unit
   ```
