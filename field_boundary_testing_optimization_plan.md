# FieldBoundaryDownloader Testing Optimization Plan

## Overview
This plan optimizes the FieldBoundaryDownloader tests by implementing industry best practices for testing with external data sources. The solution separates fast unit tests (using local fixtures) from integration tests (hitting live endpoints).

## Current Problem
- All tests hit the live Source Cooperative endpoint
- Each test downloads large Parquet files repeatedly
- Tests are slow (30-60 seconds) and inefficient
- Creates unnecessary load on external API

## Solution Architecture

### 1. Dependency Injection Pattern
**Strategy**: Add optional URL override parameter to maintain API compatibility

**Implementation**:
```python
class FieldBoundaryDownloader(BaseDownloader):
    def __init__(self, config: Optional[Config] = None, data_source_url: Optional[str] = None) -> None:
        super().__init__(config)
        self.data_source_url = data_source_url or self.SOURCE_COOP_BASE_URL
        # ... rest of initialization
```

**Benefits**:
- No breaking changes to existing API
- Easy to override for testing
- Maintains backward compatibility

### 2. Sample Data Strategy
**Approach**: Generate representative sample from live endpoint once

**Sample Data Requirements**:
- 5-10 field boundaries (small but representative)
- Include data from corn_belt region
- Include both corn and soybean crop types
- Valid fiboa schema with all required columns
- Proper geometries and CRS (EPSG:5070)

**File Location**: `tests/data/sample_field_boundaries.parquet`

### 3. Test Structure Optimization

#### Unit Tests (Fast, Local Data)
- Use local sample fixture
- Test all logic except actual data download
- Run in <1 second
- Mark with `@pytest.mark.unit`

#### Integration Tests (Live Data)
- Keep existing tests but mark as integration
- Test against real Source Cooperative endpoint
- Run less frequently (CI/CD only)
- Mark with `@pytest.mark.integration`

### 4. Pytest Configuration
Add markers to `pytest.ini` or `pyproject.toml`:
```ini
[tool.pytest.ini_options]
markers = [
    "unit: Unit tests using local fixtures",
    "integration: Integration tests hitting live endpoints",
]
```

### 5. Test Execution Strategy
```bash
# Fast unit tests (default for development)
pytest tests/test_downloaders/test_field_boundaries.py -m unit

# All tests (for CI/CD)
pytest tests/test_downloaders/test_field_boundaries.py

# Integration tests only (manual/scheduled)
pytest tests/test_downloaders/test_field_boundaries.py -m integration
```

## Implementation Steps

### Step 1: Refactor FieldBoundaryDownloader
- Add optional `data_source_url` parameter
- Update `_query_source_cooperative()` to use injected URL
- Maintain full backward compatibility

### Step 2: Generate Sample Data
- Create script to download small sample from live endpoint
- Save as Parquet in `tests/data/`
- Verify schema matches expected format

### Step 3: Update Test Structure
- Add pytest fixtures for sample data
- Mark existing tests as integration tests
- Create new unit tests using local fixture
- Update test assertions to work with sample data

### Step 4: Documentation
- Update test documentation
- Add instructions for regenerating sample data
- Document test execution strategies

## Benefits

### Performance
- Unit tests: <1 second (vs 30-60 seconds currently)
- Integration tests: Same as before but run less frequently
- Overall test suite: 10x faster for development

### Maintainability
- No dependency on external services for unit tests
- Sample data can be regenerated when needed
- Clear separation of concerns

### Reliability
- Unit tests don't fail due to network issues
- Integration tests still validate real-world scenarios
- Better test isolation

## Sample Data Schema
The sample Parquet file will contain fields with this structure:
```python
{
    'id': '17001000123456789',           # fiboa field ID
    'crop:code': '1',                    # 2023 CDL crop code
    'crop:name': 'Corn',                 # Crop name
    'crop:code_list': '1,1,1,5,5,1,1,1', # Historical codes
    'administrative_area_level_2': 'Iowa', # County name
    'geometry': <WKB binary>             # Polygon geometry (EPSG:5070)
}
```

## Migration Strategy
1. Implement new functionality alongside existing code
2. Run both unit and integration tests during transition
3. Gradually migrate tests to use local fixtures
4. Remove dependency on live endpoint for unit tests
5. Keep integration tests for CI/CD validation

## Risk Mitigation
- **Data Drift**: Sample data can be regenerated periodically
- **Schema Changes**: Integration tests catch real-world changes
- **Test Coverage**: All logic tested in both unit and integration contexts
- **Backward Compatibility**: No breaking changes to public API

This approach follows industry best practices for testing external data dependencies while maintaining full functionality validation.
