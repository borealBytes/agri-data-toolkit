"""Pytest configuration and shared fixtures."""

import shutil
import tempfile
from pathlib import Path

import geopandas as gpd
import pytest


@pytest.fixture(scope="session")
def test_data_dir():
    """Create a temporary directory for test data."""
    temp_dir = tempfile.mkdtemp(prefix="agri_toolkit_test_")
    yield Path(temp_dir)
    # Cleanup after all tests
    shutil.rmtree(temp_dir, ignore_errors=True)


@pytest.fixture(scope="function")
def clean_test_dir(tmp_path):
    """Provide a clean temporary directory for each test."""
    yield tmp_path
    # Cleanup happens automatically with tmp_path


@pytest.fixture(scope="session")
def sample_field_boundaries_parquet():
    """Load sample field boundaries data for testing.

    Returns:
        Path to sample Parquet file.
    """
    sample_path = Path(__file__).parent / "data" / "sample_field_boundaries.parquet"
    if not sample_path.exists():
        pytest.skip(
            f"Sample data not found at {sample_path}. "
            "Run: python scripts/generate_sample_field_boundaries.py"
        )
    return sample_path


@pytest.fixture
def sample_field_boundaries_gdf(sample_field_boundaries_parquet):
    """Load sample field boundaries as GeoDataFrame.

    Returns:
        GeoDataFrame with sample field boundaries data.
    """
    gdf = gpd.read_parquet(sample_field_boundaries_parquet)
    # Convert WKB geometry back to actual geometry if needed, but gpd.read_parquet should handle it
    # if it was saved as GeoParquet.
    # However, our sample generation script saves it as GeoParquet, so it should be fine.
    # But let's ensure CRS is correct as per our downloader logic which expects EPSG:5070 initially
    # The sample data we saved is in EPSG:4326 because we downloaded it using the downloader
    # which converts it.
    # Wait, the downloader converts to EPSG:4326 at the end.
    # The sample data generation script saves the result of downloader.download(),
    # so it is in EPSG:4326.
    return gdf
