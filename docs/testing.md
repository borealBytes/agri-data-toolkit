# Testing Strategy

This project uses `pytest` for testing. The test suite is divided into unit tests and integration tests.

## Test Categories

### Unit Tests
- **Marker**: `@pytest.mark.unit`
- **Description**: Fast tests that use local sample data and do not require network access.
- **Location**: `tests/test_downloaders/test_field_boundaries_unit.py`
- **Execution**: `pytest -m unit`

### Integration Tests
- **Marker**: `@pytest.mark.integration`
- **Description**: Slower tests that hit live external endpoints (e.g., Source Cooperative). These ensure end-to-end functionality with real data.
- **Location**: `tests/test_downloaders/test_field_boundaries.py`
- **Execution**: `pytest -m integration`

## Running Tests

To run all tests:
```bash
pytest
```

To run only unit tests (recommended for development):
```bash
pytest -m unit
```

To run only integration tests (recommended for CI/CD or pre-release):
```bash
pytest -m integration
```

## Sample Data

Unit tests use a local sample Parquet file located at `tests/data/sample_field_boundaries.parquet`. This file contains a small subset of real data from Source Cooperative.

### Regenerating Sample Data

If the data schema changes or the sample data becomes outdated, you can regenerate it using the provided script:

```bash
python scripts/generate_sample_field_boundaries.py --count 10
```

This script downloads fresh data from the live endpoint and saves it to the test data directory.
