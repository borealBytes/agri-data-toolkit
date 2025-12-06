# Quick Start Guide

Get up and running with the Agricultural Data Toolkit in 15 minutes.

## Prerequisites

✅ Ubuntu LTS 20.04+ (or compatible Linux)
✅ Python 3.9+ installed
✅ 50GB+ free disk space
✅ Broadband internet connection

## 1. Installation (5 minutes)

```bash
# Clone repository
git clone https://github.com/borealBytes/agri-data-toolkit.git
cd agri-data-toolkit

# Setup environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Setup workspace
python scripts/setup_workspace.py
```

Detailed installation: [installation.md](installation.md)

## 2. Your First Download (10 minutes)

### Option A: Quick Test (1 field, ~2 minutes)

```bash
# Download minimal test dataset
python scripts/download_core.py --fields 1 --test-mode

# Verify download
python scripts/validate_data.py
```

### Option B: Course Dataset (200 fields, ~10 minutes)

```bash
# Download full course dataset
python scripts/download_core.py --fields 200 --years 2020-2024

# This downloads:
# - 200 row crop field boundaries
# - SSURGO soil data for all fields
# - NASA POWER weather data (2020-2024)
# - Sentinel-2 imagery (growing season)
# - USDA Cropland Data Layer
```

### Monitor Progress

```bash
# In another terminal, watch progress
tail -f logs/download.log
```

## 3. Explore Your Data

### Generate Summary Report

```bash
# Create HTML summary
python scripts/generate_report.py --output reports/summary.html

# Open in browser
firefox reports/summary.html
```

### Quick Data Check

```python
# Python quick check
python3 << EOF
import geopandas as gpd
import pandas as pd
import json

# Load field boundaries
fields = gpd.read_file("data/processed/export/fields.geojson")
print(f"Total fields: {len(fields)}")
print(f"Total area: {fields.geometry.area.sum() / 4047:.0f} acres")
print(f"Crops: {fields['crop_type'].value_counts().to_dict()}")

# Load metadata
with open("data/metadata/data_summary.json") as f:
    meta = json.load(f)
print(f"\nDownload completed: {meta['download_date']}")
print(f"Data sources: {', '.join(meta['sources'])}")
EOF
```

## 4. Basic Analysis

### Example 1: Soil Analysis

```python
import geopandas as gpd
import matplotlib.pyplot as plt

# Load fields with soil data
fields = gpd.read_file("data/processed/integrated/fields_with_soil.geojson")

# Plot organic matter distribution
fig, ax = plt.subplots(figsize=(12, 8))
fields.plot(column='om_pct',
            cmap='YlOrBr',
            legend=True,
            ax=ax,
            edgecolor='black',
            linewidth=0.5)
ax.set_title('Soil Organic Matter (%)', fontsize=16)
plt.savefig('reports/soil_om_map.png', dpi=300, bbox_inches='tight')
print("Saved: reports/soil_om_map.png")
```

### Example 2: Weather Summary

```python
import pandas as pd
import matplotlib.pyplot as plt

# Load weather data
weather = pd.read_csv("data/raw/weather/all_fields_weather.csv",
                      parse_dates=['date'])

# Calculate growing degree days
weather['gdd'] = ((weather['temp_max'] + weather['temp_min']) / 2 - 50).clip(lower=0)

# Plot seasonal GDD
fig, ax = plt.subplots(figsize=(12, 6))
weather.groupby('date')['gdd'].sum().plot(ax=ax, linewidth=2)
ax.set_title('Cumulative Growing Degree Days (2024)', fontsize=16)
ax.set_ylabel('GDD (Base 50°F)')
ax.grid(True, alpha=0.3)
plt.savefig('reports/gdd_2024.png', dpi=300, bbox_inches='tight')
print("Saved: reports/gdd_2024.png")
```

### Example 3: NDVI Calculation

```python
from agri_toolkit.processors import IndicesCalculator
import rasterio
from rasterio.plot import show
import matplotlib.pyplot as plt

# Calculate NDVI for a field
calc = IndicesCalculator()
ndvi = calc.calculate_ndvi(
    red_path="data/raw/imagery/field_001_red.tif",
    nir_path="data/raw/imagery/field_001_nir.tif"
)

# Plot
fig, ax = plt.subplots(figsize=(10, 10))
show(ndvi, ax=ax, cmap='RdYlGn', vmin=-1, vmax=1)
ax.set_title('Field 001 - NDVI (July 2024)', fontsize=16)
plt.colorbar(ax.images[0], ax=ax, label='NDVI', shrink=0.6)
plt.savefig('reports/field_001_ndvi.png', dpi=300, bbox_inches='tight')
print("Saved: reports/field_001_ndvi.png")
```

## 5. Common Workflows

### Download Specific Region

```bash
# Corn Belt only
python scripts/download_core.py --region "corn_belt" --fields 200

# Multiple regions
python scripts/download_core.py --regions corn_belt,great_plains --fields 150
```

### Custom Year Range

```bash
# Historical data
python scripts/download_core.py --fields 200 --years 2015-2020

# Recent years only
python scripts/download_core.py --fields 200 --years 2022-2024
```

### Download with Validation

```bash
# Automatic validation after download
python scripts/download_core.py --fields 200 --validate

# Generate report immediately
python scripts/download_core.py --fields 200 --validate --report
```

### Export to Different Formats

```bash
# Export to Shapefile
python scripts/export_data.py --format shapefile

# Export to GeoParquet (efficient)
python scripts/export_data.py --format geoparquet

# Export to CSV (tabular only)
python scripts/export_data.py --format csv --no-geometry
```

## 6. Jupyter Notebooks

Explore data interactively:

```bash
# Install Jupyter
pip install jupyter

# Launch notebook server
jupyter notebook notebooks/

# Open:
# - 01_data_exploration.ipynb (start here)
# - 02_soil_analysis.ipynb
# - 03_weather_patterns.ipynb
# - 04_ndvi_calculation.ipynb
```

## 7. Command Reference

### Download Commands

```bash
# Core dataset
python scripts/download_core.py --fields 200

# Optional datasets
python scripts/download_optional.py --nass --ers

# Everything
python scripts/download_all.py --fields 200 --include-optional
```

### Validation Commands

```bash
# Validate all data
python scripts/validate_data.py

# Validate specific layer
python scripts/validate_data.py --layer fields
python scripts/validate_data.py --layer soil
python scripts/validate_data.py --layer weather

# Strict mode (fail on warnings)
python scripts/validate_data.py --strict
```

### Report Commands

```bash
# HTML report
python scripts/generate_report.py --format html

# PDF report (requires wkhtmltopdf)
python scripts/generate_report.py --format pdf

# JSON metadata only
python scripts/generate_report.py --format json
```

## 8. Troubleshooting

### Download Fails

```bash
# Check network connectivity
ping -c 3 power.larc.nasa.gov

# Retry with verbose logging
python scripts/download_core.py --fields 200 --verbose

# Resume interrupted download
python scripts/download_core.py --fields 200 --resume
```

### Out of Memory

```bash
# Process fields in batches
python scripts/download_core.py --fields 200 --batch-size 50

# Reduce imagery resolution
python scripts/download_core.py --fields 200 --imagery-resolution 20
```

### Validation Errors

```bash
# Show detailed error report
python scripts/validate_data.py --verbose

# Automatically fix common issues
python scripts/validate_data.py --auto-fix
```

## 9. Next Steps

Now that you have data:

1. 📊 **Explore**: Open Jupyter notebooks in `notebooks/`
2. 🗺️ **Visualize**: Try examples in `examples/`
3. 🛠️ **Analyze**: Use processors in `src/agri_toolkit/processors/`
4. 📊 **Dashboard**: Build your Row Crop Intelligence Dashboard

### Course Assignments

- **Assignment 1**: Document your dataset (due Week 2)
- **Assignment 2**: Clean and integrate data (due Week 3)
- **Assignment 3**: Exploratory analysis (due Week 4)
- **Assignment 4**: Geospatial mapping (due Week 5)

### Useful Resources

- 📖 [API Reference](api_reference.md)
- 📊 [Data Sources Guide](data_sources.md)
- 👥 [Contributing Guide](contributing.md)
- 🐛 [Issue Tracker](https://github.com/borealBytes/agri-data-toolkit/issues)

## 10. Getting Help

### Course Students

- **Office Hours**: 30 min before Classes 2-14 (Tue/Thu 4:30 PM PT)
- **Teaching Assistant**: Available in course portal
- **Discussion Forum**: Post questions in course discussion

### General Users

- **Documentation**: Browse `docs/` directory
- **GitHub Issues**: Report bugs or request features
- **Discussions**: Ask questions in GitHub Discussions

---

**Ready to dive deeper?** Check out the [examples/](../examples/) directory for complete workflows and use cases.
