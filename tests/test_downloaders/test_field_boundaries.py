"""Tests for field boundary downloader.

These tests verify the FieldBoundaryDownloader works correctly with
real USDA Crop Sequence Boundaries data from Source Cooperative.

Test Philosophy:
    - Use minimal download counts (2-10 fields) to avoid external API load
    - Test with real data to ensure integration works end-to-end
    - Validate data structure and quality from actual source
    - Keep tests fast for CI/CD (30-60 seconds total)
"""

import geopandas as gpd
import pytest
from shapely.geometry import Polygon

from agri_toolkit.core.config import Config
from agri_toolkit.downloaders.field_boundaries import FieldBoundaryDownloader


class TestFieldBoundaryDownloader:
    """Test suite for FieldBoundaryDownloader.

    Note: These tests make real HTTP requests to Source Cooperative.
    Download counts are kept minimal (2-10 fields) to:
    - Reduce CI/CD execution time
    - Minimize load on external data provider
    - Still validate full integration with real data
    """

    @pytest.fixture
    def downloader(self, tmp_path):
        """Create downloader instance with temporary output directory."""
        # Create a temporary config
        config = Config()
        # Override paths to use tmp_path
        config._config["paths"]["raw"] = str(tmp_path / "raw")
        config._config["paths"]["processed"] = str(tmp_path / "processed")

        return FieldBoundaryDownloader(config=config)

    def test_download_minimum_fields(self, downloader):
        """Test downloading minimum number of fields from real data.

        Downloads only 2 fields to minimize external API load during testing.
        """
        fields = downloader.download(count=2, regions=["corn_belt"])

        # Should return exactly 2 fields
        assert len(fields) == 2, f"Expected 2 fields, got {len(fields)}"

        # Should be a GeoDataFrame
        assert isinstance(fields, gpd.GeoDataFrame)

    def test_download_creates_valid_geometries(self, downloader):
        """Test that downloaded fields have valid geometries."""
        fields = downloader.download(count=2, regions=["corn_belt"])

        # All geometries should be valid
        assert fields.geometry.is_valid.all(), "Found invalid geometries"

        # All geometries should be Polygons (or MultiPolygons)
        assert all(
            geom.geom_type in ["Polygon", "MultiPolygon"] for geom in fields.geometry
        ), "Geometries must be Polygon or MultiPolygon types"

    def test_download_has_required_attributes(self, downloader):
        """Test that fields have all required attributes from Source Cooperative."""
        fields = downloader.download(count=2, regions=["corn_belt"])

        # Required columns from CSB dataset
        required_columns = [
            "field_id",  # CSB ID
            "region",  # Our region mapping
            "state",  # State abbreviation
            "county",  # County name
            "area_acres",  # Field size
            "crop_2023",  # 2023 crop type
            "geometry",  # Polygon geometry
        ]

        for col in required_columns:
            assert col in fields.columns, f"Missing required column: {col}"

        # Verify data types
        assert fields["area_acres"].dtype in ["float64", "float32"], "area_acres should be numeric"

    def test_download_has_crs(self, downloader):
        """Test that GeoDataFrame has correct coordinate reference system."""
        fields = downloader.download(count=2, regions=["corn_belt"])

        assert fields.crs is not None, "GeoDataFrame missing CRS"
        assert fields.crs.to_string() == "EPSG:4326", "CRS should be WGS84 (EPSG:4326)"

    def test_download_multiple_regions(self, downloader):
        """Test downloading from multiple regions."""
        regions = ["corn_belt", "great_plains"]
        fields = downloader.download(count=4, regions=regions)

        assert len(fields) == 4, f"Expected 4 fields, got {len(fields)}"

        # Should have at least one region represented
        # (may not have all regions if filtering reduces available fields)
        unique_regions = set(fields["region"].unique())
        assert len(unique_regions) >= 1, "Should have at least 1 region represented"

    def test_download_filters_by_crop(self, downloader):
        """Test crop type filtering works correctly."""
        fields = downloader.download(count=2, regions=["corn_belt"], crops=["corn", "soybeans"])

        # All fields should have crop_2023 in requested types
        assert all(
            crop in ["corn", "soybeans"] for crop in fields["crop_2023"]
        ), "Fields should only contain requested crop types"

    def test_download_filters_by_size(self, downloader):
        """Test field size filtering works correctly."""
        min_acres = 50.0
        max_acres = 200.0

        fields = downloader.download(
            count=2, regions=["corn_belt"], min_acres=min_acres, max_acres=max_acres
        )

        # All fields should be within size range
        assert all(
            min_acres <= acres <= max_acres for acres in fields["area_acres"]
        ), f"All fields should be between {min_acres} and {max_acres} acres"

    def test_download_saves_to_file(self, downloader, tmp_path):
        """Test that download saves fields to file."""
        downloader.download(count=2, regions=["corn_belt"], output_format="geojson")

        # Check that file was created
        expected_path = tmp_path / "raw" / "field_boundaries" / "fields.geojson"
        assert expected_path.exists(), f"Output file not created at {expected_path}"

        # Verify file can be read back
        loaded_fields = gpd.read_file(expected_path)
        assert len(loaded_fields) == 2

    def test_download_shapefile_format(self, downloader, tmp_path):
        """Test saving to shapefile format."""
        downloader.download(count=2, regions=["corn_belt"], output_format="shapefile")

        # Check that shapefile was created
        expected_path = tmp_path / "raw" / "field_boundaries" / "fields.shp"
        assert expected_path.exists(), f"Shapefile not created at {expected_path}"

        # Verify file can be read back
        loaded_fields = gpd.read_file(expected_path)
        assert len(loaded_fields) == 2

    def test_validate_method(self, downloader):
        """Test the validate method with real data."""
        fields = downloader.download(count=2, regions=["corn_belt"])

        # Valid data should pass validation
        assert downloader.validate(fields) is True

    def test_validate_rejects_empty_data(self, downloader):
        """Test that validation fails for empty data."""
        empty_gdf = gpd.GeoDataFrame()

        assert downloader.validate(empty_gdf) is False

    def test_validate_rejects_missing_columns(self, downloader):
        """Test that validation fails when required columns are missing."""
        # Create GeoDataFrame missing required columns
        gdf = gpd.GeoDataFrame(
            {
                "field_id": ["TEST_001"],
                # Missing 'region' column
                "geometry": [Polygon([(0, 0), (1, 0), (1, 1), (0, 1), (0, 0)])],
            },
            crs="EPSG:4326",
        )

        assert downloader.validate(gdf) is False

    def test_download_raises_on_invalid_count(self, downloader):
        """Test that download raises ValueError for invalid count."""
        with pytest.raises(ValueError, match="count must be at least 1"):
            downloader.download(count=0)

        with pytest.raises(ValueError, match="count must be at least 1"):
            downloader.download(count=-1)

    def test_download_raises_on_empty_regions(self, downloader):
        """Test that download raises ValueError for empty regions list."""
        with pytest.raises(ValueError, match="regions cannot be empty"):
            downloader.download(count=2, regions=[])

    def test_download_raises_on_invalid_region(self, downloader):
        """Test that download raises ValueError for invalid region name."""
        with pytest.raises(ValueError, match="Invalid regions"):
            downloader.download(count=2, regions=["invalid_region"])

    def test_download_raises_on_invalid_crop(self, downloader):
        """Test that download raises ValueError for invalid crop type."""
        with pytest.raises(ValueError, match="Invalid crops"):
            downloader.download(count=2, regions=["corn_belt"], crops=["invalid_crop"])

    def test_download_raises_on_invalid_format(self, downloader):
        """Test that download raises ValueError for invalid output format."""
        with pytest.raises(ValueError, match="Unsupported output format"):
            downloader.download(count=2, regions=["corn_belt"], output_format="invalid")

    def test_download_real_data_structure(self, downloader):
        """Integration test: Verify complete data structure from Source Cooperative.

        This test validates that we're getting properly structured real data
        from the USDA Crop Sequence Boundaries dataset.
        """
        fields = downloader.download(count=5, regions=["corn_belt"], crops=["corn", "soybeans"])

        # Should get exactly 5 fields
        assert len(fields) == 5

        # Verify all expected columns exist
        expected_cols = [
            "field_id",
            "region",
            "state",
            "county",
            "area_acres",
            "crop_2023",
            "geometry",
        ]
        for col in expected_cols:
            assert col in fields.columns

        # Verify data types
        assert fields["field_id"].dtype == "object"  # String field IDs
        assert fields["area_acres"].dtype in ["float64", "float32"]  # Numeric acres

        # Verify geometries are valid
        assert fields.geometry.is_valid.all()

        # Verify CRS
        assert fields.crs.to_string() == "EPSG:4326"

        # Verify fields are within corn belt states
        corn_belt_states = ["IL", "IA", "IN", "OH", "MN"]
        assert all(
            state in corn_belt_states for state in fields["state"]
        ), "All fields should be in corn belt states"

        # Verify reasonable field sizes (40-500 acres is our default range)
        assert all(
            40 <= acres <= 500 for acres in fields["area_acres"]
        ), "Field sizes should be within expected range"
