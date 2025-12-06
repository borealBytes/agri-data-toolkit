"""Persistent integration test for field boundary downloader.

This test generates test data that persists in the workspace for CI/CD visualization.
Unlike other tests that use temporary directories, this test writes to the actual
workspace paths so the GitHub Actions workflow can find the generated GeoJSON files.

This test is specifically designed to run in CI/CD environments and should be
invoked with: pytest tests/test_downloaders/test_field_boundaries_persistent.py -v
"""

from pathlib import Path

import geopandas as gpd
import pytest

from agri_toolkit.core.config import Config
from agri_toolkit.downloaders.field_boundaries import FieldBoundaryDownloader


class TestFieldBoundaryDownloaderPersistent:
    """Persistent integration test for CI/CD test data generation."""

    @pytest.mark.persistent
    @pytest.mark.integration
    def test_generate_persistent_test_data(self):
        """Generate test data that persists in workspace for CI/CD visualization.

        This test creates GeoJSON files in the expected workspace location
        (data/raw/field_boundaries/) so the GitHub Actions workflow can find them.

        The test uses the default Config() which points to actual workspace paths,
        ensuring files persist after test completion.
        """
        # Use default config (points to workspace paths, not tmp_path)
        config = Config()

        # Create downloader with sample data for reliability
        sample_path = Path(__file__).parent.parent / "data" / "sample_field_boundaries.parquet"
        if not sample_path.exists():
            pytest.skip(
                f"Sample data not found at {sample_path}. "
                "Run: python scripts/generate_sample_field_boundaries.py"
            )

        downloader = FieldBoundaryDownloader(config=config, data_source_url=str(sample_path))

        # Download a small number of fields for CI/CD
        fields = downloader.download(
            count=5, regions=["corn_belt"], crops=["corn", "soybeans"], output_format="geojson"
        )

        # Verify we got data
        assert len(fields) > 0, "Should download at least some fields"
        assert isinstance(fields, gpd.GeoDataFrame), "Should return GeoDataFrame"

        # Verify file was created in expected location
        expected_path = Path("data/raw/field_boundaries/fields.geojson")
        assert expected_path.exists(), f"GeoJSON file should exist at {expected_path}"

        # Verify file can be read back
        loaded_fields = gpd.read_file(expected_path)
        assert len(loaded_fields) > 0, "Saved file should contain field data"

        # Log success for CI/CD visibility
        print(f"✅ Generated persistent test data: {expected_path}")
        print(f"📊 Fields in dataset: {len(loaded_fields)}")
        print(f"🗺️  CRS: {loaded_fields.crs}")
        print(f"📍 Regions: {loaded_fields['region'].unique().tolist()}")

    @pytest.mark.persistent
    @pytest.mark.integration
    def test_generate_persistent_test_data_shapefile(self):
        """Generate test data in shapefile format for additional CI/CD testing.

        This creates a secondary test data file to ensure the workflow
        can handle different output formats.
        """
        # Use default config (points to workspace paths, not tmp_path)
        config = Config()

        # Create downloader with sample data for reliability
        sample_path = Path(__file__).parent.parent / "data" / "sample_field_boundaries.parquet"
        if not sample_path.exists():
            pytest.skip(
                f"Sample data not found at {sample_path}. "
                "Run: python scripts/generate_sample_field_boundaries.py"
            )

        downloader = FieldBoundaryDownloader(config=config, data_source_url=str(sample_path))

        # Download fields in shapefile format
        fields = downloader.download(
            count=3, regions=["corn_belt"], crops=["corn"], output_format="shapefile"
        )

        # Verify we got data
        assert len(fields) > 0, "Should download at least some fields"

        # Verify shapefile was created
        expected_path = Path("data/raw/field_boundaries/fields.shp")
        assert expected_path.exists(), f"Shapefile should exist at {expected_path}"

        # Verify file can be read back
        loaded_fields = gpd.read_file(expected_path)
        assert len(loaded_fields) > 0, "Saved shapefile should contain field data"

        # Log success for CI/CD visibility
        print(f"✅ Generated persistent shapefile: {expected_path}")
        print(f"📊 Fields in shapefile: {len(loaded_fields)}")
