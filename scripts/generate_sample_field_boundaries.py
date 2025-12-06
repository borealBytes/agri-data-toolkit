#!/usr/bin/env python3
"""Generate sample field boundaries data for testing.

This script generates synthetic field boundaries and saves them as a local
Parquet file for use in unit tests.
"""

import argparse
from pathlib import Path

import geopandas as gpd
from shapely.geometry import Polygon


def generate_sample_data(output_path: Path, count: int = 5) -> None:
    """Generate sample field boundaries data.

    Args:
        output_path: Path to save the sample Parquet file.
        count: Number of fields to sample (default: 5).
    """
    print(f"Generating synthetic data with {count} fields...")

    # Synthetic data generation parameters
    start_lon = -93.0
    start_lat = 42.0
    size = 0.003  # degrees, approx 330m
    offset = 0.01  # degrees

    data = []
    for i in range(count):
        # Calculate coordinates for this field
        lon = start_lon + (i * offset)
        lat = start_lat + (i * offset)

        # Create square polygon
        # (lon, lat), (lon+size, lat), (lon+size, lat+size), (lon, lat+size), (lon, lat)
        poly = Polygon(
            [(lon, lat), (lon + size, lat), (lon + size, lat + size), (lon, lat + size), (lon, lat)]
        )

        # Alternate crops
        is_corn = i % 2 == 0
        crop_code = "1" if is_corn else "5"
        crop_name = "Corn" if is_corn else "Soybeans"

        # Use Illinois FIPS (17) prefix for ID to match corn_belt region
        data.append(
            {
                "id": f"17{i+1:05d}",
                "crop:code": crop_code,
                "crop:name": crop_name,
                "crop:code_list": "USDA_CDL",
                "administrative_area_level_2": "Story",
                "geometry": poly,
            }
        )

    # Create GeoDataFrame
    gdf = gpd.GeoDataFrame(data, crs="EPSG:4326")

    # Calculate area in acres
    # Project to equal area projection for accurate area calculation
    # EPSG:5070 (NAD83 / Conus Albers) is good for US
    gdf_projected = gdf.to_crs("EPSG:5070")
    gdf["area_acres"] = gdf_projected.area / 4046.86  # Convert sq meters to acres

    # Save as Parquet
    gdf.to_parquet(output_path, index=False)
    print(f"Sample data saved to: {output_path}")

    # Verify the file
    verify_sample_data(output_path)


def verify_sample_data(parquet_path: Path) -> None:
    """Verify the generated sample data has correct schema."""
    print(f"Verifying sample data at {parquet_path}...")

    # Read back the data
    df = gpd.read_parquet(parquet_path)

    print(f"Sample data contains {len(df)} fields")
    print(f"Columns: {list(df.columns)}")
    print(f"CRS: {df.crs}")
    print(f"Sample crop codes: {df['crop:code'].unique()}")
    print(f"Sample areas (acres): {df['area_acres'].tolist()}")

    # Verify required columns
    required_columns = [
        "id",
        "crop:code",
        "crop:name",
        "crop:code_list",
        "administrative_area_level_2",
        "geometry",
        "area_acres",
    ]
    missing_columns = [col for col in required_columns if col not in df.columns]

    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")

    print("Sample data verification passed!")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Generate sample field boundaries data")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("tests/data/sample_field_boundaries.parquet"),
        help="Output path for sample Parquet file",
    )
    parser.add_argument("--count", type=int, default=5, help="Number of fields to sample")

    args = parser.parse_args()

    # Create output directory
    args.output.parent.mkdir(parents=True, exist_ok=True)

    # Generate sample data
    generate_sample_data(args.output, args.count)


if __name__ == "__main__":
    main()
