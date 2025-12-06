"""Field boundary downloader using USDA Crop Sequence Boundaries.

This module downloads vector polygons representing row crop field boundaries
from the USDA NASS Crop Sequence Boundaries (CSB) dataset via Source Cooperative.

Data Source:
    USDA NASS Crop Sequence Boundaries (2023)
    https://source.coop/fiboa/us-usda-cropland

Format:
    GeoParquet (cloud-optimized columnar format following fiboa standard)

Coverage:
    Entire contiguous United States, 16+ million field boundaries

Attributes:
    - Field ID (fiboa 'id'), administrative area (state FIPS)
    - Crop type codes (fiboa 'crop:code_list' - CDL codes)
    - Crop name (fiboa 'crop:name')
    - Geometry (polygon boundaries in EPSG:4326)

Citation:
    USDA National Agricultural Statistics Service Cropland Data Layer.
    {YEAR}. Published crop-specific data layer [Online].
    Available at https://nassgeodata.gmu.edu/CropScape/
    (verified {date}). USDA-NASS, Washington, DC.
"""

from pathlib import Path
from typing import Any, List, Optional

import duckdb
import geopandas as gpd

from agri_toolkit.core.config import Config
from agri_toolkit.downloaders.base import BaseDownloader


class FieldBoundaryDownloader(BaseDownloader):
    """Download field boundary polygons from USDA Crop Sequence Boundaries.

    This downloader accesses USDA NASS Crop Sequence Boundaries (CSB) data
    hosted on Source Cooperative in cloud-optimized GeoParquet format.

    The CSB dataset provides algorithmically-delineated field boundaries
    derived from 8 years of Cropland Data Layer (CDL) historical data.
    Each boundary represents a continuous crop sequence area.

    Regions:
        - corn_belt: IL, IA, IN, OH, MN (major corn and soybean production)
        - great_plains: KS, NE, SD, ND, TX (wheat and diverse crops)
        - southeast: AR, MS, LA, GA (cotton, rice, soybeans)

    Crops:
        Corn (1), soybeans (5), wheat (various), cotton (2) - using CDL codes

    Data Access:
        Uses DuckDB with spatial extension for efficient cloud-native
        GeoParquet querying. Only downloads filtered subset of fields,
        reducing bandwidth and processing time.
    """

    # Source Cooperative URL for USDA CSB GeoParquet data
    # Actual filename is us_usda_cropland.parquet (verified at source.coop)
    SOURCE_COOP_BASE_URL = (
        "https://data.source.coop/fiboa/us-usda-cropland/us_usda_cropland.parquet"
    )

    # Mapping of regions to state FIPS codes
    # fiboa uses administrative_area_level_2 for state FIPS codes
    REGION_STATE_FIPS = {
        "corn_belt": ["17", "19", "18", "39", "27"],  # IL, IA, IN, OH, MN
        "great_plains": ["20", "31", "46", "38", "48"],  # KS, NE, SD, ND, TX
        "southeast": ["05", "28", "22", "13"],  # AR, MS, LA, GA
    }

    # Crop type mappings - using CDL (Cropland Data Layer) codes
    # These are standard USDA crop type codes
    CROP_TYPES = {
        "corn": ["1"],  # Corn
        "soybeans": ["5"],  # Soybeans
        "wheat": ["23", "24", "25", "26", "27"],  # Spring/Winter/Durum wheat varieties
        "cotton": ["2"],  # Cotton
    }

    def __init__(self, config: Optional[Config] = None) -> None:
        """Initialize field boundary downloader.

        Args:
            config: Configuration object. If None, uses default config.
        """
        super().__init__(config)
        self.output_subdir = "field_boundaries"
        self._duckdb_conn: Optional[duckdb.DuckDBPyConnection] = None

    def _get_duckdb_connection(self) -> duckdb.DuckDBPyConnection:
        """Get or create DuckDB connection with spatial extension.

        Returns:
            DuckDB connection with spatial and httpfs extensions loaded.
        """
        if self._duckdb_conn is None:
            self._duckdb_conn = duckdb.connect()
            # Install and load spatial extension for geometry handling
            self._duckdb_conn.execute("INSTALL spatial;")
            self._duckdb_conn.execute("LOAD spatial;")
            # Install and load httpfs for remote file access
            self._duckdb_conn.execute("INSTALL httpfs;")
            self._duckdb_conn.execute("LOAD httpfs;")
            self.logger.debug("DuckDB connection initialized with spatial extensions")
        return self._duckdb_conn

    def download(self, **kwargs: Any) -> gpd.GeoDataFrame:
        """Download field boundaries from Source Cooperative.

        This method queries the USDA Crop Sequence Boundaries dataset
        hosted on Source Cooperative, filtering by region and crop type.
        It uses DuckDB for efficient server-side filtering,
        downloading only the requested subset of data.

        Args:
            **kwargs: Keyword arguments:
                count (int): Number of fields to download (default: 200).
                    For testing, use small values (2-10) to minimize load.
                regions (Optional[List[str]]): Regions to sample from.
                    Options: 'corn_belt', 'great_plains', 'southeast'
                    Default: ['corn_belt']
                crops (Optional[List[str]]): Crop types to include.
                    Options: 'corn', 'soybeans', 'wheat', 'cotton'
                    Default: ['corn', 'soybeans']
                output_format (str): Output file format.
                    Options: 'geojson', 'shapefile'
                    Default: 'geojson'

        Returns:
            GeoDataFrame containing field boundaries with attributes:
                - field_id: Unique identifier (fiboa ID)
                - region: Region name (corn_belt, great_plains, southeast)
                - state_fips: State FIPS code
                - area_acres: Field size in acres (calculated from geometry)
                - crop_code_list: Crop type codes (CDL codes)
                - crop_name: Crop name
                - geometry: Polygon geometry (EPSG:4326)

        Raises:
            ValueError: If count < 1, regions is empty, or invalid parameters.
            RuntimeError: If data download fails.

        Example:
            >>> downloader = FieldBoundaryDownloader()
            >>> # Download 10 corn/soybean fields from Iowa (testing)
            >>> fields = downloader.download(
            ...     count=10,
            ...     regions=['corn_belt'],
            ...     crops=['corn', 'soybeans']
            ... )
            >>> print(f"Downloaded {len(fields)} fields")
            Downloaded 10 fields
        """
        # Parse arguments with defaults
        count: int = kwargs.get("count", 200)
        regions: Optional[List[str]] = kwargs.get("regions", None)
        crops: Optional[List[str]] = kwargs.get("crops", None)
        output_format: str = kwargs.get("output_format", "geojson")

        self.logger.info(
            "Starting field boundary download: %d fields from Source Cooperative", count
        )

        # Validate inputs
        if count < 1:
            raise ValueError("count must be at least 1")

        # Default regions
        if regions is None:
            regions = ["corn_belt"]

        if not regions:
            raise ValueError("regions cannot be empty")

        # Validate regions
        invalid_regions = [r for r in regions if r not in self.REGION_STATE_FIPS]
        if invalid_regions:
            raise ValueError(
                "Invalid regions: %s. Valid options: %s"
                % (invalid_regions, list(self.REGION_STATE_FIPS.keys()))
            )

        # Default crops
        if crops is None:
            crops = ["corn", "soybeans"]

        # Validate crops
        invalid_crops = [c for c in crops if c not in self.CROP_TYPES]
        if invalid_crops:
            raise ValueError(
                "Invalid crops: %s. Valid options: %s"
                % (invalid_crops, list(self.CROP_TYPES.keys()))
            )

        self.logger.info("Regions: %s", regions)
        self.logger.info("Crops: %s", crops)

        # Query CSB data from Source Cooperative
        fields_gdf = self._query_source_cooperative(
            count=count,
            regions=regions,
            crops=crops,
        )

        # Validate downloaded data
        if not self.validate(fields_gdf):
            raise RuntimeError("Downloaded field data failed validation")

        # Save to file
        output_path = self._save_fields(fields_gdf, output_format)
        self.logger.info("Fields saved to: %s", output_path)

        return fields_gdf

    def _query_source_cooperative(
        self,
        count: int,
        regions: List[str],
        crops: List[str],
    ) -> gpd.GeoDataFrame:
        """Query USDA CSB data from Source Cooperative using DuckDB.

        Uses DuckDB spatial extension to efficiently query cloud-hosted
        GeoParquet files with server-side filtering. Only downloads
        the filtered subset, not the entire dataset.

        DuckDB uses HTTP range requests to fetch only the needed row groups
        and columns, making this very efficient even for large datasets.

        Args:
            count: Number of fields to retrieve.
            regions: List of region names.
            crops: List of crop types.

        Returns:
            GeoDataFrame with downloaded field boundaries.

        Raises:
            RuntimeError: If query fails or no data returned.
        """
        try:
            # Get DuckDB connection
            con = self._get_duckdb_connection()

            # Collect state FIPS codes from regions
            state_fips = []
            for region in regions:
                state_fips.extend(self.REGION_STATE_FIPS[region])

            # Build state filter for SQL
            state_filter = ", ".join(["'%s'" % fips for fips in state_fips])

            # Build crop filter for SQL - collect all CDL codes for requested crops
            crop_codes = []
            for crop in crops:
                crop_codes.extend(self.CROP_TYPES[crop])
            crop_filter = ", ".join(["%s" % code for code in crop_codes])

            # Use actual parquet filename from Source Cooperative
            # Filename is us_usda_cropland.parquet (verified at source.coop)
            parquet_url = self.SOURCE_COOP_BASE_URL

            # Build DuckDB query with filters
            # DuckDB pushes down these filters for efficient remote querying
            # Note: fiboa schema uses:
            #   - 'administrative_area_level_2' for state FIPS codes
            #   - 'crop:code_list' for crop codes (string with comma-separated CDL codes)
            #   - 'crop:name' for crop name
            #   - 'id' for unique field identifier
            # Column names with special chars need double quotes in DuckDB
            # 
            # crop:code_list contains strings like "1,1,1,1,1,1,1,1" (8 years of crop codes)
            # We check if any of our target crop codes appear in this list
            query = f"""
            SELECT
                id as field_id,
                administrative_area_level_2 as state_fips,
                "crop:code_list" as crop_code_list,
                "crop:name" as crop_name,
                geometry
            FROM read_parquet('{parquet_url}')
            WHERE administrative_area_level_2 IN ({state_filter})
              AND (
                {' OR '.join([f'"crop:code_list" LIKE \'%{code}%\'' for code in crop_codes])}
              )
            ORDER BY random()
            LIMIT {count}
            """

            self.logger.debug("Executing DuckDB query: %s", query)
            self.logger.info("Querying Source Cooperative (this may take 10-30 seconds)...")

            # Execute query and get result as DataFrame
            result_df = con.execute(query).df()

            if len(result_df) == 0:
                raise RuntimeError(
                    "No fields found matching criteria. "
                    "Try different regions/crops or adjust filters."
                )

            self.logger.info("Retrieved %d fields from Source Cooperative", len(result_df))

            # Convert to GeoDataFrame
            # DuckDB spatial extension returns geometry as WKB binary
            gdf = gpd.GeoDataFrame(result_df, geometry="geometry", crs="EPSG:4326")

            # Calculate area from geometry
            # Need to project to equal-area coordinate system for accurate area calculation
            # EPSG:5070 is Albers Equal Area (used by USDA for cropland data)
            gdf_projected = gdf.to_crs("EPSG:5070")
            # Calculate area in square meters, convert to acres
            # 1 acre = 4046.86 square meters
            gdf["area_acres"] = gdf_projected.geometry.area / 4046.86

            # Add region mapping back to data
            # Map state FIPS to region for user convenience
            state_to_region = {}
            for region, fips_list in self.REGION_STATE_FIPS.items():
                for fips in fips_list:
                    state_to_region[fips] = region

            # Map state FIPS to region
            gdf["region"] = gdf["state_fips"].map(state_to_region)
            # If multiple regions, mark as mixed where region is null
            if len(regions) > 1:
                gdf["region"] = gdf["region"].fillna("mixed")
            elif len(regions) == 1:
                gdf["region"] = gdf["region"].fillna(regions[0])

            # Reorder columns for better readability
            column_order = [
                "field_id",
                "region",
                "state_fips",
                "area_acres",
                "crop_code_list",
                "crop_name",
                "geometry",
            ]
            gdf = gdf[column_order]

            return gdf

        except Exception as e:
            self.logger.error("Failed to query Source Cooperative: %s", e)
            raise RuntimeError("Data download failed: %s" % e) from e

    def _save_fields(self, gdf: gpd.GeoDataFrame, output_format: str) -> Path:
        """Save field boundaries to file.

        Args:
            gdf: GeoDataFrame to save.
            output_format: Output format (geojson or shapefile).

        Returns:
            Path to saved file.

        Raises:
            ValueError: If output format is unsupported.
        """
        if output_format == "geojson":
            output_path = self.get_output_path("fields.geojson", self.output_subdir)
            gdf.to_file(output_path, driver="GeoJSON")
        elif output_format == "shapefile":
            output_path = self.get_output_path("fields.shp", self.output_subdir)
            gdf.to_file(output_path, driver="ESRI Shapefile")
        else:
            raise ValueError(
                "Unsupported output format: %s. Use 'geojson' or 'shapefile'." % output_format
            )

        self.logger.info("Saved %d fields to %s", len(gdf), output_path)
        return output_path

    def validate(self, data: gpd.GeoDataFrame) -> bool:
        """Validate field boundary data.

        Checks for:
        - Non-empty dataset
        - Required columns present
        - Valid geometries
        - Coordinate reference system defined

        Args:
            data: GeoDataFrame to validate.

        Returns:
            True if valid, False otherwise.
        """
        if data is None or len(data) == 0:
            self.logger.error("No fields in dataset")
            return False

        # Check for required columns
        required_columns = ["field_id", "region", "geometry"]
        missing_columns = [col for col in required_columns if col not in data.columns]

        if missing_columns:
            self.logger.error("Missing required columns: %s", missing_columns)
            return False

        # Check geometry validity
        invalid_geoms = ~data.geometry.is_valid
        if invalid_geoms.any():
            self.logger.error("Found %d invalid geometries", invalid_geoms.sum())
            return False

        # Check CRS
        if data.crs is None:
            self.logger.error("GeoDataFrame has no CRS defined")
            return False

        self.logger.info("Field boundaries validation passed")
        return True

    def __del__(self) -> None:
        """Clean up DuckDB connection on deletion."""
        if self._duckdb_conn is not None:
            self._duckdb_conn.close()
