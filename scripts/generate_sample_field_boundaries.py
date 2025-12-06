#!/usr/bin/env python3
"""Generate sample field boundaries data for testing.

This script downloads a small sample of field boundaries from the live
Source Cooperative endpoint and saves it as a local Parquet file for
use in unit tests.
"""

import argparse
from pathlib import Path

import geopandas as gpd

from agri_toolkit.downloaders.field_boundaries import FieldBoundaryDownloader


def generate_sample_data(output_path: Path, count: int = 10) -> None:
    """Generate sample field boundaries data.

    Args:
        output_path: Path to save the sample Parquet file.
        count: Number of fields to sample (default: 10).
    """
    print(f"Generating sample data with {count} fields...")

    # Create temporary downloader to get real data
    downloader = FieldBoundaryDownloader()

    # Download small sample from corn belt
    fields_gdf = downloader.download(count=count, regions=["corn_belt"], crops=["corn", "soybeans"])

    print(f"Downloaded {len(fields_gdf)} fields")

    # Convert to fiboa format for storage
    # The original data has fiboa column names, so we need to preserve those
    sample_data = fields_gdf.copy()

    # Rename columns to match fiboa schema
    sample_data = sample_data.rename(
        columns={
            "field_id": "id",
            "crop_code": "crop:code",
            "crop_name": "crop:name",
            "crop_code_list": "crop:code_list",
        }
    )

    # Select only fiboa columns
    fiboa_columns = [
        "id",
        "crop:code",
        "crop:name",
        "crop:code_list",
        "administrative_area_level_2",  # County name
        "geometry",
    ]

    # Ensure we have the county column (use state_fips as placeholder)
    if "administrative_area_level_2" not in sample_data.columns:
        sample_data["administrative_area_level_2"] = sample_data["state_fips"]

    sample_data = sample_data[fiboa_columns]

    # Save as Parquet
    # Use geopandas to_parquet to ensure GeoParquet metadata is written
    sample_data.to_parquet(output_path, index=False)
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
    print(f"Sample crop codes: {df['crop:code'].unique()[:5]}")

    # Verify required columns
    required_columns = ["id", "crop:code", "crop:name", "crop:code_list", "geometry"]
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
    parser.add_argument("--count", type=int, default=10, help="Number of fields to sample")

    args = parser.parse_args()

    # Create output directory
    args.output.parent.mkdir(parents=True, exist_ok=True)

    # Generate sample data
    generate_sample_data(args.output, args.count)


if __name__ == "__main__":
    main()
