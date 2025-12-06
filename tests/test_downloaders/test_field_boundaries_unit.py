"""Unit tests for FieldBoundaryDownloader using local sample data.

These tests use a small local sample dataset to test the downloader logic
without hitting the live Source Cooperative endpoint.
"""

import geopandas as gpd
import pytest

from agri_toolkit.core.config import Config
from agri_toolkit.downloaders.field_boundaries import FieldBoundaryDownloader


class TestFieldBoundaryDownloaderUnit:
    """Unit tests for FieldBoundaryDownloader using local fixtures."""

    @pytest.fixture
    def downloader_with_sample_data(self, tmp_path, sample_field_boundaries_parquet):
        """Create downloader instance configured to use sample data."""
        config = Config()
        config._config["paths"]["raw"] = str(tmp_path / "raw")
        config._config["paths"]["processed"] = str(tmp_path / "processed")

        return FieldBoundaryDownloader(
            config=config, data_source_url=str(sample_field_boundaries_parquet)
        )

    @pytest.mark.unit
    def test_download_with_sample_data(self, downloader_with_sample_data):
        """Test downloading from sample data fixture."""
        fields = downloader_with_sample_data.download(count=5)

        # Should return up to 5 fields (or fewer if sample has less)
        assert len(fields) <= 5
        assert len(fields) > 0

        # Should be a GeoDataFrame
        assert isinstance(fields, gpd.GeoDataFrame)

    @pytest.mark.unit
    def test_download_creates_valid_geometries_sample(self, downloader_with_sample_data):
        """Test that downloaded fields have valid geometries."""
        fields = downloader_with_sample_data.download(count=5)

        # All geometries should be valid
        assert fields.geometry.is_valid.all(), "Found invalid geometries"

        # All geometries should be Polygons (or MultiPolygons)
        assert all(
            geom.geom_type in ["Polygon", "MultiPolygon"] for geom in fields.geometry
        ), "Geometries must be Polygon or MultiPolygon types"

    @pytest.mark.unit
    def test_download_has_required_attributes_sample(self, downloader_with_sample_data):
        """Test that fields have all required attributes."""
        fields = downloader_with_sample_data.download(count=5)

        # Required columns
        required_columns = [
            "field_id",
            "region",
            "state_fips",
            "area_acres",
            "crop_code",
            "crop_name",
            "crop_code_list",
            "geometry",
        ]

        for col in required_columns:
            assert col in fields.columns, f"Missing required column: {col}"

    @pytest.mark.unit
    def test_download_has_crs_sample(self, downloader_with_sample_data):
        """Test that GeoDataFrame has correct coordinate reference system."""
        fields = downloader_with_sample_data.download(count=5)

        assert fields.crs is not None, "GeoDataFrame missing CRS"
        assert fields.crs.to_string() == "EPSG:4326", "CRS should be WGS84 (EPSG:4326)"

    @pytest.mark.unit
    def test_validate_method_sample(self, downloader_with_sample_data):
        """Test the validate method with sample data."""
        fields = downloader_with_sample_data.download(count=5)

        # Valid data should pass validation
        assert downloader_with_sample_data.validate(fields) is True

    @pytest.mark.unit
    def test_validate_rejects_empty_data_sample(self, downloader_with_sample_data):
        """Test that validation fails for empty data."""
        empty_gdf = gpd.GeoDataFrame()

        assert downloader_with_sample_data.validate(empty_gdf) is False

    @pytest.mark.unit
    def test_download_raises_on_invalid_count_sample(self, downloader_with_sample_data):
        """Test that download raises ValueError for invalid count."""
        with pytest.raises(ValueError, match="count must be at least 1"):
            downloader_with_sample_data.download(count=0)

    @pytest.mark.unit
    def test_download_raises_on_empty_regions_sample(self, downloader_with_sample_data):
        """Test that download raises ValueError for empty regions list."""
        with pytest.raises(ValueError, match="regions cannot be empty"):
            downloader_with_sample_data.download(count=2, regions=[])

    @pytest.mark.unit
    def test_download_raises_on_invalid_region_sample(self, downloader_with_sample_data):
        """Test that download raises ValueError for invalid region name."""
        with pytest.raises(ValueError, match="Invalid regions"):
            downloader_with_sample_data.download(count=2, regions=["invalid_region"])

    @pytest.mark.unit
    def test_download_raises_on_invalid_crop_sample(self, downloader_with_sample_data):
        """Test that download raises ValueError for invalid crop type."""
        with pytest.raises(ValueError, match="Invalid crops"):
            downloader_with_sample_data.download(
                count=2, regions=["corn_belt"], crops=["invalid_crop"]
            )

    @pytest.mark.unit
    def test_download_raises_on_invalid_format_sample(self, downloader_with_sample_data):
        """Test that download raises ValueError for invalid output format."""
        with pytest.raises(ValueError, match="Unsupported output format"):
            downloader_with_sample_data.download(
                count=2, regions=["corn_belt"], output_format="invalid"
            )
