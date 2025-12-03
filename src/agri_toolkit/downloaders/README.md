# Field Boundary Downloader

## Overview

The Field Boundary Downloader provides access to **USDA NASS Crop Sequence Boundaries (CSB)** - a comprehensive dataset of agricultural field boundaries across the contiguous United States.

## Data Source

### USDA Crop Sequence Boundaries (CSB)

- **Provider**: USDA National Agricultural Statistics Service (NASS)
- **Hosting**: Source Cooperative (cloud-optimized GeoParquet)
- **Format**: Vector polygons (EPSG:4326)
- **Coverage**: Entire contiguous US, 16+ million field boundaries
- **Update Frequency**: Annual
- **Latest Version**: 2023

**Source Cooperative URL**: https://source.coop/fiboa/us-usda-cropland

### What is CSB?

Crop Sequence Boundaries are algorithmically-delineated field polygons created by:
1. Stacking 8 years of Cropland Data Layer (CDL) raster data
2. Identifying contiguous areas with similar crop rotation patterns
3. Using road/rail networks to prevent field overlaps
4. Filtering to fields >1 hectare (~2.5 acres)
5. Dissolving adjacent fields with matching 2023 crop types

The result is a **realistic representation of agricultural field boundaries** used for crop production, not legal parcels.

## Key Features

✅ **Zero Setup** - No API keys, accounts, or authentication required  
✅ **Cloud-Native** - GeoParquet format with DuckDB for efficient querying  
✅ **Filtered Downloads** - Server-side filtering reduces bandwidth  
✅ **Regional Sampling** - Target specific agricultural regions  
✅ **Crop Filtering** - Select specific crop types  
✅ **Size Filtering** - Control min/max field sizes  
✅ **Multiple Formats** - Export as GeoJSON or Shapefile  

## Quick Start

### Installation

```bash
# Clone repository
git clone https://github.com/borealBytes/agri-data-toolkit.git
cd agri-data-toolkit

# Install dependencies
poetry install
```

### Basic Usage

```python
from agri_toolkit.downloaders import FieldBoundaryDownloader

# Initialize downloader
downloader = FieldBoundaryDownloader()

# Download 50 corn/soybean fields from Iowa/Illinois
fields = downloader.download(
    count=50,
    regions=['corn_belt'],
    crops=['corn', 'soybeans']
)

print(f"Downloaded {len(fields)} fields")
print(fields.head())
```

### Output Structure

The returned `GeoDataFrame` includes:

| Column | Type | Description |
|--------|------|-------------|
| `field_id` | str | Unique CSB identifier |
| `region` | str | Agricultural region (corn_belt, great_plains, southeast) |
| `state` | str | State abbreviation (IA, IL, KS, etc.) |
| `county` | str | County name |
| `area_acres` | float | Field size in acres |
| `crop_2023` | str | Crop type in 2023 |
| `geometry` | Polygon | Field boundary (EPSG:4326) |

## Advanced Usage

### Region Selection

Three predefined agricultural regions:

```python
# Corn Belt: IL, IA, IN, OH, MN
fields = downloader.download(count=100, regions=['corn_belt'])

# Great Plains: KS, NE, SD, ND, TX
fields = downloader.download(count=100, regions=['great_plains'])

# Southeast: AR, MS, LA, GA
fields = downloader.download(count=100, regions=['southeast'])

# Multiple regions
fields = downloader.download(
    count=150,
    regions=['corn_belt', 'great_plains']
)
```

### Crop Type Filtering

```python
# Single crop type
fields = downloader.download(
    count=50,
    regions=['corn_belt'],
    crops=['corn']
)

# Multiple crop types
fields = downloader.download(
    count=100,
    regions=['southeast'],
    crops=['cotton', 'soybeans']
)

# All major row crops
fields = downloader.download(
    count=200,
    regions=['corn_belt', 'great_plains', 'southeast'],
    crops=['corn', 'soybeans', 'wheat', 'cotton']
)
```

### Field Size Filtering

```python
# Small fields (40-100 acres)
fields = downloader.download(
    count=50,
    regions=['corn_belt'],
    min_acres=40,
    max_acres=100
)

# Large fields (200-500 acres)
fields = downloader.download(
    count=50,
    regions=['great_plains'],
    min_acres=200,
    max_acres=500
)
```

### Output Formats

```python
# Save as GeoJSON (default)
fields = downloader.download(
    count=50,
    regions=['corn_belt'],
    output_format='geojson'
)
# Saves to: data/raw/field_boundaries/fields.geojson

# Save as Shapefile
fields = downloader.download(
    count=50,
    regions=['corn_belt'],
    output_format='shapefile'
)
# Saves to: data/raw/field_boundaries/fields.shp (+ .shx, .dbf, .prj)
```

## Configuration

### Custom Data Directory

```python
from agri_toolkit.core.config import Config
from agri_toolkit.downloaders import FieldBoundaryDownloader

# Create custom config
config = Config()
config._config['paths']['raw'] = '/custom/data/path'

# Use with downloader
downloader = FieldBoundaryDownloader(config=config)
fields = downloader.download(count=50, regions=['corn_belt'])
```

### Custom Config File

```yaml
# config/custom.yaml
paths:
  raw: /custom/data/raw
  processed: /custom/data/processed

fields:
  regions:
    - corn_belt
    - great_plains
  default_count: 200
```

```python
config = Config(config_path='config/custom.yaml')
downloader = FieldBoundaryDownloader(config=config)
```

## Performance Considerations

### Download Times

Typical download times (depends on network speed):

- **2-10 fields**: 10-30 seconds (testing)
- **50 fields**: 30-60 seconds
- **200 fields**: 60-120 seconds
- **500+ fields**: 2-5 minutes

### Bandwidth Usage

DuckDB's cloud-native querying only downloads filtered data:

- **Metadata overhead**: ~1-2 MB
- **Per field**: ~2-5 KB
- **50 fields**: ~100-250 KB total
- **200 fields**: ~400 KB - 1 MB total

This is **10-100x more efficient** than downloading entire state files!

### Caching Recommendations

For repeated use with same parameters:

```python
# Download once
fields = downloader.download(
    count=200,
    regions=['corn_belt'],
    output_format='geojson'
)

# Later sessions: Load from saved file
import geopandas as gpd
fields = gpd.read_file('data/raw/field_boundaries/fields.geojson')
```

## Testing

Tests use minimal download counts to reduce CI/CD time:

```bash
# Run all field boundary tests
poetry run pytest tests/test_downloaders/test_field_boundaries.py -v

# Run specific test
poetry run pytest tests/test_downloaders/test_field_boundaries.py::TestFieldBoundaryDownloader::test_download_minimum_fields -v
```

**Test Philosophy**:
- Download only 2-5 fields per test
- Validates real data integration
- Keeps CI/CD execution under 2 minutes
- Minimizes load on Source Cooperative

## Data License & Citation

### License

USDA NASS Cropland Data Layer and Crop Sequence Boundaries are **public domain**:

- No restrictions on use, modification, or distribution
- Free for commercial, educational, and research use
- No attribution legally required (but appreciated)

### Recommended Citation

```
USDA National Agricultural Statistics Service Cropland Data Layer. 
2023. Published crop-specific data layer [Online]. 
Available at https://nassgeodata.gmu.edu/CropScape/ 
USDA-NASS, Washington, DC.
```

### Source Cooperative Attribution

```
Data accessed via Source Cooperative (https://source.coop),
a free and open geospatial data platform by Radiant Earth Foundation.
```

## Technical Architecture

### How It Works

1. **DuckDB Connection** - Initialize with spatial + httpfs extensions
2. **SQL Query Building** - Generate filters for region, crop, size
3. **Cloud Query** - Execute against GeoParquet files on Source Cooperative
4. **Server-Side Filtering** - DuckDB reads only matching partitions
5. **Result Streaming** - Download filtered subset as DataFrame
6. **Geometry Parsing** - Convert WKB to Shapely geometries
7. **GeoDataFrame Creation** - Return as geopandas GeoDataFrame

### Dependencies

- **geopandas**: Geospatial data handling
- **duckdb**: Cloud-native query engine
- **shapely**: Geometry processing
- **pyarrow** (via geopandas): Parquet file reading

### Why DuckDB?

DuckDB enables **cloud-native querying** of GeoParquet files:

✅ Read remote files via HTTPS (no download required)  
✅ Server-side filtering (only matching data transfers)  
✅ Columnar format (efficient for attribute filtering)  
✅ Spatial extension (geometry operations)  
✅ Partition pruning (skip irrelevant state files)  

Alternative (pure geopandas) would require downloading entire datasets.

## Troubleshooting

### No fields returned

**Problem**: Query returns 0 fields

**Solutions**:
```python
# 1. Relax size filters
fields = downloader.download(
    count=50,
    regions=['corn_belt'],
    min_acres=10,  # Lower minimum
    max_acres=1000  # Raise maximum
)

# 2. Try different crop types
fields = downloader.download(
    count=50,
    regions=['corn_belt'],
    crops=['corn', 'soybeans', 'wheat']  # More options
)

# 3. Try different region
fields = downloader.download(
    count=50,
    regions=['great_plains']  # Different region
)
```

### Slow downloads

**Problem**: Downloads taking >5 minutes

**Solutions**:
1. Reduce count (fewer fields)
2. Add stricter filters (limit data scanned)
3. Check network connection
4. Try downloading during off-peak hours

### DuckDB errors

**Problem**: `duckdb.Error: HTTP Error`

**Solutions**:
1. Check internet connection
2. Verify Source Cooperative is accessible
3. Retry after a few minutes (transient network issues)

## Examples

### Example 1: Classroom Dataset

Generate 200 diverse fields for class analysis:

```python
from agri_toolkit.downloaders import FieldBoundaryDownloader

downloader = FieldBoundaryDownloader()

# Mixed regions, crops, sizes
fields = downloader.download(
    count=200,
    regions=['corn_belt', 'great_plains', 'southeast'],
    crops=['corn', 'soybeans', 'wheat', 'cotton'],
    min_acres=40,
    max_acres=400
)

print(f"Downloaded {len(fields)} fields")
print(f"Regions: {fields['region'].value_counts().to_dict()}")
print(f"Crops: {fields['crop_2023'].value_counts().to_dict()}")
print(f"Size range: {fields['area_acres'].min():.1f} - {fields['area_acres'].max():.1f} acres")
```

### Example 2: Corn Belt Focus

Study corn-soybean rotation in Iowa:

```python
fields = downloader.download(
    count=100,
    regions=['corn_belt'],
    crops=['corn', 'soybeans'],
    min_acres=80,
    max_acres=160
)

# Analyze crop distribution
import matplotlib.pyplot as plt
fields['crop_2023'].value_counts().plot(kind='bar')
plt.title('Corn vs Soybeans in Iowa Fields')
plt.ylabel('Number of Fields')
plt.show()

# Map fields
fields.plot(column='crop_2023', legend=True, figsize=(12, 8))
plt.title('Field Boundaries by Crop Type')
plt.show()
```

### Example 3: Regional Comparison

Compare field sizes across regions:

```python
import pandas as pd

region_data = []

for region in ['corn_belt', 'great_plains', 'southeast']:
    fields = downloader.download(count=50, regions=[region])
    region_data.append({
        'region': region,
        'mean_acres': fields['area_acres'].mean(),
        'median_acres': fields['area_acres'].median(),
        'std_acres': fields['area_acres'].std()
    })

df = pd.DataFrame(region_data)
print(df)
```

## Further Reading

- [USDA NASS CSB Documentation](https://www.nass.usda.gov/Research_and_Science/Crop-Sequence-Boundaries/)
- [Source Cooperative Platform](https://source.coop)
- [GeoParquet Specification](https://geoparquet.org)
- [DuckDB Spatial Extension](https://duckdb.org/docs/extensions/spatial)
- [FIBOA Standard](https://fiboa.github.io/specification/)

## Support

For issues or questions:

- **GitHub Issues**: https://github.com/borealBytes/agri-data-toolkit/issues
- **Discussions**: https://github.com/borealBytes/agri-data-toolkit/discussions
- **Email**: claytoneyoung+github@gmail.com
