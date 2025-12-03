"""Field boundary downloader.

This module downloads vector polygons representing row crop field boundaries
across diverse US agricultural regions.
"""

from pathlib import Path
from typing import List, Optional

import geopandas as gpd
from shapely.geometry import Polygon

from agri_toolkit.downloaders.base import BaseDownloader


class FieldBoundaryDownloader(BaseDownloader):
    """Download field boundary polygons for row crop fields.

    This downloader acquires ~200 field boundaries across:
    - Corn Belt (IL, IA, IN, OH, MN)
    - Great Plains (KS, NE, SD, ND, TX)
    - Southeast (AR, MS, LA, GA)

    Crops: corn, soybeans, wheat, cotton
    """

    def __init__(self, config=None):
        """Initialize field boundary downloader.

        Args:
            config: Configuration object.
        """
        super().__init__(config)
        self.output_subdir = "field_boundaries"

    def download(
        self,
        count: int = 200,
        regions: Optional[List[str]] = None,
        output_format: str = "geojson",
    ) -> gpd.GeoDataFrame:
        """Download field boundaries.

        Args:
            count: Number of fields to download (default: 200).
            regions: List of regions to sample from. If None, uses all regions
                    from config (corn_belt, great_plains, southeast).
            output_format: Output format (geojson or shapefile).

        Returns:
            GeoDataFrame containing field boundaries with attributes.

        Raises:
            ValueError: If count < 1 or regions is empty.

        Example:
            >>> downloader = FieldBoundaryDownloader()
            >>> fields = downloader.download(count=10, regions=["corn_belt"])
            >>> print(len(fields))
            10
        """
        self.logger.info(f"Starting field boundary download: {count} fields")

        # Validate inputs
        if count < 1:
            raise ValueError("count must be at least 1")

        if regions is None:
            regions = self.config.get("fields.regions", ["corn_belt", "great_plains", "southeast"])

        if not regions:
            raise ValueError("regions cannot be empty")

        self.logger.info(f"Regions: {regions}")

        # PLACEHOLDER: Actual implementation will call external API or data source
        # For now, generate sample data for testing
        fields_gdf = self._generate_sample_fields(count, regions)

        # Save to file
        output_path = self._save_fields(fields_gdf, output_format)
        self.logger.info(f"Fields saved to: {output_path}")

        return fields_gdf

    def _generate_sample_fields(self, count: int, regions: List[str]) -> gpd.GeoDataFrame:
        """Generate sample field boundaries for testing.

        PLACEHOLDER: This will be replaced with actual data source integration.

        Args:
            count: Number of fields to generate.
            regions: Regions to generate fields for.

        Returns:
            GeoDataFrame with sample field boundaries.
        """
        self.logger.warning(
            "Using placeholder field generation. "
            "Actual implementation will download real field data."
        )

        # Generate simple rectangular fields as placeholders
        fields = []

        # Region coordinates (approximate centers)
        region_coords = {
            "corn_belt": (-93.0, 42.0),  # Iowa center
            "great_plains": (-98.0, 39.0),  # Kansas center
            "southeast": (-91.0, 34.0),  # Arkansas center
        }

        fields_per_region = count // len(regions)
        remainder = count % len(regions)

        field_id = 1
        for i, region in enumerate(regions):
            # Distribute fields across regions
            region_count = fields_per_region + (1 if i < remainder else 0)
            base_lon, base_lat = region_coords.get(region, (-95.0, 40.0))

            for j in range(region_count):
                # Create a simple rectangular polygon
                # Field size: ~0.01 degrees (~1km at mid-latitudes)
                lon_offset = (j % 10) * 0.015
                lat_offset = (j // 10) * 0.015

                lon = base_lon + lon_offset
                lat = base_lat + lat_offset

                # Create rectangle (approximately 80-160 acres)
                polygon = Polygon(
                    [
                        (lon, lat),
                        (lon + 0.01, lat),
                        (lon + 0.01, lat + 0.01),
                        (lon, lat + 0.01),
                        (lon, lat),
                    ]
                )

                fields.append(
                    {
                        "field_id": f"FIELD_{field_id:04d}",
                        "region": region,
                        "area_acres": 80 + (j % 80),  # Vary between 80-160 acres
                        "centroid_lat": lat + 0.005,
                        "centroid_lon": lon + 0.005,
                        "crop_type": ["corn", "soybeans", "wheat", "cotton"][j % 4],
                        "geometry": polygon,
                    }
                )
                field_id += 1

        # Create GeoDataFrame
        gdf = gpd.GeoDataFrame(fields, crs="EPSG:4326")

        self.logger.info(f"Generated {len(gdf)} placeholder fields")
        return gdf

    def _save_fields(self, gdf: gpd.GeoDataFrame, output_format: str) -> Path:
        """Save field boundaries to file.

        Args:
            gdf: GeoDataFrame to save.
            output_format: Output format (geojson or shapefile).

        Returns:
            Path to saved file.
        """
        if output_format == "geojson":
            output_path = self.get_output_path("fields.geojson", self.output_subdir)
            gdf.to_file(output_path, driver="GeoJSON")
        elif output_format == "shapefile":
            output_path = self.get_output_path("fields.shp", self.output_subdir)
            gdf.to_file(output_path, driver="ESRI Shapefile")
        else:
            raise ValueError(f"Unsupported output format: {output_format}")

        return output_path

    def validate(self, data: gpd.GeoDataFrame) -> bool:
        """Validate field boundary data.

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
            self.logger.error(f"Missing required columns: {missing_columns}")
            return False

        # Check geometry validity
        invalid_geoms = ~data.geometry.is_valid
        if invalid_geoms.any():
            self.logger.error(f"Found {invalid_geoms.sum()} invalid geometries")
            return False

        # Check CRS
        if data.crs is None:
            self.logger.error("GeoDataFrame has no CRS defined")
            return False

        self.logger.info("Field boundaries validation passed")
        return True
