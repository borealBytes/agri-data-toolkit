# Test Data Visualization Map Generation Fix

## Problem Summary

The GitHub Actions workflow was failing to generate test data visualization maps because the "Find the test GeoJSON file" step couldn't locate any GeoJSON files in `data/raw/field_boundaries`. The root cause was that all existing tests used temporary directories (`tmp_path`) that get cleaned up after each test, so no files persisted in the expected workspace location.

## Root Cause Analysis

### Original Test Behavior
- **Tests used temporary directories**: Both `test_field_boundaries.py` and `test_field_boundaries_unit.py` configured the downloader to use `tmp_path`
- **Files were cleaned up**: Pytest automatically cleans up temporary directories after each test
- **No persistent output**: The workflow expected files in `data/raw/field_boundaries/` but tests wrote to temporary locations

### Workflow Expectations vs Reality
- **Workflow expected**: GeoJSON files in `data/raw/field_boundaries/`
- **Tests produced**: Files in `tmp_path/raw/field_boundaries/` (cleaned up after test)
- **Result**: Workflow step `find data/raw/field_boundaries -name "*.geojson"` found nothing

## Solution Implemented

### 1. Created Persistent Integration Test
**File**: `tests/test_downloaders/test_field_boundaries_persistent.py`

- **Purpose**: Generate test data that persists in workspace for CI/CD visualization
- **Key difference**: Uses default `Config()` instead of `tmp_path` configuration
- **Output location**: `data/raw/field_boundaries/fields.geojson` and `fields.shp`
- **Markers**: `@pytest.mark.persistent` and `@pytest.mark.integration`

### 2. Updated Pytest Configuration
**File**: `pyproject.toml`

- **Added marker**: `"persistent: Tests that generate persistent data for CI/CD artifacts"`
- **Purpose**: Register the new `persistent` marker to avoid pytest warnings

### 3. Modified GitHub Actions Workflow
**File**: `.github/workflows/ci.yml`

- **Added explicit test run**: Run persistent test after standard tests
- **Improved map generation step**:
  - Ensure directory exists before searching
  - Prefer specific file path from persistent test
  - Better error handling and debugging output
  - More robust file detection logic

### 4. Test Execution Flow
```bash
# Standard tests (using tmp_path, files cleaned up)
poetry run pytest tests/ -v --cov=src/agri_toolkit --cov-report=xml --cov-report=term

# Persistent test (using workspace paths, files persist)
poetry run pytest tests/test_downloaders/test_field_boundaries_persistent.py -v
```

## Files Modified

1. **Created**: `tests/test_downloaders/test_field_boundaries_persistent.py`
   - New persistent integration test class
   - Two test methods: one for GeoJSON, one for Shapefile
   - Uses default Config() for workspace paths

2. **Modified**: `pyproject.toml`
   - Added `persistent` marker to pytest configuration

3. **Modified**: `.github/workflows/ci.yml`
   - Added persistent test execution step
   - Enhanced map generation step with better error handling

## Verification

### Local Testing
```bash
# Run the new persistent test
poetry run pytest tests/test_downloaders/test_field_boundaries_persistent.py -v

# Verify files were created
ls -la data/raw/field_boundaries/
# Should show: fields.geojson and fields.shp
```

### Expected Workflow Behavior
1. **Tests run**: Standard tests + persistent test
2. **Data generated**: `data/raw/field_boundaries/fields.geojson` exists
3. **Map generation**: Finds the GeoJSON file successfully
4. **Artifact upload**: Map uploaded as GitHub Actions artifact
5. **PR comment**: Updated with map download link

## Recommendations for Future Maintenance

### 1. Test Data Management
- **Keep persistent tests minimal**: Only generate enough data for visualization (5-10 fields)
- **Monitor file size**: Ensure generated files don't bloat the repository
- **Consider cleanup**: Add workflow step to clean up old test data files

### 2. Test Organization
- **Marker usage**: Use `@pytest.mark.persistent` only for tests that must generate persistent data
- **Isolation**: Keep persistent tests separate from unit/integration tests
- **Documentation**: Document why each test needs to be persistent

### 3. Workflow Optimization
- **Conditional execution**: Consider running persistent tests only on specific triggers
- **Parallel execution**: Run persistent tests in parallel with other CI tasks if possible
- **Error handling**: The workflow now gracefully handles missing test data

### 4. Monitoring and Debugging
- **Check logs**: Monitor CI logs for persistent test output
- **File verification**: Periodically verify that test data files are being created
- **Map generation**: Ensure the visualization map is being generated and uploaded

### 5. Future Enhancements
- **Multiple data sources**: Consider generating test data from different regions/crops
- **Dynamic data**: Use different sample data for different PRs to show variety
- **Performance testing**: Add performance benchmarks using the persistent test data

## Troubleshooting Guide

### If persistent test fails:
1. Check if sample data exists: `tests/data/sample_field_boundaries.parquet`
2. Verify workspace permissions for writing to `data/raw/field_boundaries/`
3. Check pytest marker registration in `pyproject.toml`

### If workflow still can't find files:
1. Verify the persistent test actually ran in the workflow logs
2. Check that `data/raw/field_boundaries/` directory exists
3. Look for any file permission issues in the workflow

### If map generation fails:
1. Verify the GeoJSON file is valid: `python -c "import geopandas as gpd; gpd.read_file('data/raw/field_boundaries/fields.geojson')"`
2. Check that `scripts/generate_test_map.py` exists and is executable
3. Review the map generation script for any dependencies

## Summary

This fix resolves the GitHub Actions workflow issue by ensuring that at least one test run produces persistent GeoJSON files in the expected location. The solution maintains test isolation for most tests while providing the necessary data for CI/CD visualization features.
