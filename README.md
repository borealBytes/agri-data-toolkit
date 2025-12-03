# 🌾 Agricultural Data Toolkit

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

> A comprehensive Python toolkit for acquiring, processing, and analyzing US agricultural datasets for row crop intelligence and precision agriculture applications.

## 📋 Table of Contents

- [Overview](#overview)
- [Course Context](#course-context)
- [Features](#features)
- [Core Data Sources](#core-data-sources)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage Examples](#usage-examples)
- [Development Roadmap](#development-roadmap)
- [Contributing](#contributing)
- [License](#license)
- [Support](#support)

## 🎯 Overview

The **Agricultural Data Toolkit** is designed to streamline the acquisition and integration of diverse US agricultural data sources for row crop analysis. This toolkit automates the download, preprocessing, and integration of:

- 🗺️ **Field Boundaries**: Vector polygons for ~200 row-crop fields (corn, soy, wheat, cotton) across the US
- 🌱 **Soil Data**: NRCS SSURGO soil survey attributes (organic matter, pH, texture, drainage)
- 🌤️ **Weather & Climate**: Time-series data from NASA POWER and NOAA stations
- 🛰️ **Satellite Imagery**: Multispectral imagery from Sentinel-2 and Landsat for vegetation analysis
- 🌽 **Crop Classification**: USDA Cropland Data Layer for crop type identification

### Why This Toolkit?

Agricultural data analysis requires integrating multiple heterogeneous data sources with different formats, spatial resolutions, and temporal scales. This toolkit:

✅ **Automates** tedious data acquisition workflows  
✅ **Standardizes** data formats and coordinate systems  
✅ **Integrates** multiple data layers for field-level analysis  
✅ **Validates** data quality and completeness  
✅ **Exports** analysis-ready datasets for visualization and modeling  

## 🎓 Course Context

**Course**: Agricultural Data Analytics  
**Instructor**: Clayton Young (ex-Bayer, ex-Monsanto, ex-Climate Corporation)  
**Duration**: 8 weeks, 14 lessons  
**Target**: Data analysts, GIS specialists, agronomists, and ag-tech professionals  

This toolkit serves as the **foundation data package** for all course assignments and the final project: a **Row Crop Intelligence Data Dashboard**.

### Learning Objectives

By using this toolkit, students will:

1. ✅ Collect and organize agricultural datasets from major US sources (USDA, NASA, NOAA)
2. ✅ Analyze and visualize spatial and temporal patterns in yield, soil, and climate
3. ✅ Develop geospatial dashboards that communicate farm performance insights
4. ✅ Evaluate precision agriculture technologies' impact on efficiency and sustainability
5. ✅ Apply ethical practices in farm data management and ownership

## ✨ Features

### Core Capabilities

- **🔄 Automated Data Download**: One-command acquisition of all required datasets
- **📊 Field-Level Integration**: Automatic spatial joins and attribute linking
- **🗺️ CRS Standardization**: Consistent coordinate reference systems across layers
- **✅ Data Validation**: Built-in checks for completeness and quality
- **📦 Export Formats**: Multiple output formats (GeoJSON, Shapefile, GeoParquet, CSV)
- **🔧 Ubuntu LTS Compatible**: Designed for command-line execution on Ubuntu systems
- **📝 Comprehensive Logging**: Detailed execution logs for debugging and auditing

### Advanced Features (Planned)

- **⚡ Parallel Processing**: Multi-threaded downloads for large datasets
- **🔄 Incremental Updates**: Refresh only changed data
- **🎯 Custom AOI Support**: User-defined areas of interest
- **📈 Metadata Catalogs**: Automatic dataset documentation
- **🧪 Unit Testing**: Comprehensive test coverage for reliability

## 🗃️ Core Data Sources

### 1. Field Boundaries (REQUIRED)

**Description**: Vector polygons representing individual row-crop fields  
**Count**: ~200 fields across diverse US regions (Corn Belt, Great Plains, Southeast)  
**Crops**: Corn, soybeans, wheat, cotton  
**Format**: Shapefile, GeoJSON  
**CRS**: EPSG:4326 (WGS84) and EPSG:5070 (Albers Equal Area)  
**First Use**: Class 02, Assignment 1  

### 2. NRCS SSURGO Soil Data (REQUIRED)

**Description**: Soil survey attributes from USDA Natural Resources Conservation Service  
**Attributes**:
- Organic matter content (%)
- Soil pH
- Texture class (sand, silt, clay percentages)
- Drainage class
- Available water capacity
- Soil depth

**Format**: CSV with spatial join keys  
**First Use**: Class 03, Assignment 1  
**Primary Use**: Class 06 (geospatial joins), Assignment 8 (soil health metrics)  

### 3. Weather & Climate Data (REQUIRED)

**NASA POWER API**:
- Daily temperature (min, max, mean)
- Precipitation
- Solar radiation
- Relative humidity
- Wind speed

**NOAA Climate Data**:
- Historical weather station data
- Climate normals (30-year averages)
- Growing degree days (GDD)
- Extreme weather events

**Temporal Coverage**: 2015-2024 (minimum 5 years)  
**Format**: CSV with daily time series  
**First Use**: Class 03, Assignment 1  
**Primary Use**: Class 08 (climate analysis), Assignment 6 (weather trends)  

### 4. Satellite Imagery (REQUIRED)

**Sentinel-2 (ESA)**:
- Multispectral bands (10-20m resolution)
- 5-day revisit time
- Bands: Blue, Green, Red, NIR, SWIR

**Landsat 8/9 (USGS)**:
- Multispectral bands (30m resolution)
- 16-day revisit time
- Bands: Blue, Green, Red, NIR, SWIR, Thermal

**Derived Products**:
- NDVI (Normalized Difference Vegetation Index)
- EVI (Enhanced Vegetation Index)
- NDWI (Normalized Difference Water Index)

**Temporal Coverage**: Peak growing season (June-September) for years 2020-2024  
**Format**: GeoTIFF (Cloud-Optimized)  
**First Use**: Assignment 1  
**Primary Use**: Class 07 (remote sensing), Assignment 5 (NDVI calculation)  

### 5. USDA Cropland Data Layer (REQUIRED)

**Description**: Raster classification of crop types and land cover  
**Resolution**: 30m  
**Classes**: 100+ crop and land cover types  
**Temporal Coverage**: Annual layers (2018-2024)  
**Format**: GeoTIFF  
**Primary Use**: Crop type verification and land use context  

### 6. USDA NASS / ERS Statistics (OPTIONAL)

**Description**: County and state-level aggregated statistics  
**Metrics**:
- Crop yield (bu/acre)
- Planted and harvested acreage
- Farm economic indicators
- Conservation practice adoption rates

**Spatial Scale**: County, Agricultural District, State  
**Format**: CSV  
**Primary Use**: Class 06 (county-level choropleth maps)  

### 7. Precision Agriculture Equipment Data (OPTIONAL - Instructor Demo)

**Description**: As-applied and as-harvested data from farm equipment  
**Sources**: John Deere Operations Center, Climate FieldView  
**Data Types**:
- Planter data (seed population, depth, singulation)
- Combine yield monitor data (yield, moisture, elevation)

**Format**: Proprietary formats (Shapefile exports available)  
**Primary Use**: Class 10 demonstration only (not required for student package)  

## 📁 Project Structure

```
agri-data-toolkit/
│
├── README.md                      # This file
├── LICENSE                        # MIT License
├── .gitignore                    # Python, data files, credentials
├── pyproject.toml                # Poetry dependency management
├── setup.py                      # Alternative pip installation
├── requirements.txt              # Pip dependencies
│
├── docs/                         # Comprehensive documentation
│   ├── installation.md          # Installation instructions
│   ├── quickstart.md            # Quick start guide
│   ├── api_reference.md         # API documentation
│   ├── data_sources.md          # Detailed data source documentation
│   ├── contributing.md          # Contribution guidelines
│   └── examples/                # Usage examples and tutorials
│       ├── basic_usage.md
│       ├── field_analysis.md
│       └── dashboard_integration.md
│
├── src/                          # Source code
│   └── agri_toolkit/
│       ├── __init__.py
│       ├── core/                 # Core functionality
│       │   ├── __init__.py
│       │   ├── config.py        # Configuration management
│       │   ├── logger.py        # Logging setup
│       │   └── validators.py    # Data validation
│       │
│       ├── downloaders/          # Data acquisition modules
│       │   ├── __init__.py
│       │   ├── base.py          # Base downloader class
│       │   ├── field_boundaries.py
│       │   ├── ssurgo_soil.py
│       │   ├── nasa_power.py
│       │   ├── noaa_climate.py
│       │   ├── sentinel2.py
│       │   ├── landsat.py
│       │   ├── cropland_data_layer.py
│       │   └── usda_nass.py
│       │
│       ├── processors/           # Data processing modules
│       │   ├── __init__.py
│       │   ├── spatial.py       # Spatial operations
│       │   ├── temporal.py      # Time series processing
│       │   ├── integration.py   # Multi-source integration
│       │   └── indices.py       # Vegetation indices (NDVI, EVI)
│       │
│       ├── exporters/            # Data export modules
│       │   ├── __init__.py
│       │   ├── geojson.py
│       │   ├── shapefile.py
│       │   ├── geoparquet.py
│       │   └── csv.py
│       │
│       └── utils/                # Utility functions
│           ├── __init__.py
│           ├── crs.py           # Coordinate system utilities
│           ├── file_io.py       # File operations
│           └── geometry.py      # Geometric operations
│
├── scripts/                      # Command-line scripts
│   ├── download_all.py          # Main download script
│   ├── download_core.py         # Core data only (fields, soil, weather, imagery)
│   ├── download_optional.py     # Optional datasets (NASS, equipment)
│   ├── validate_data.py         # Data validation script
│   ├── generate_report.py       # Data summary report
│   └── setup_workspace.py       # Initial workspace setup
│
├── tests/                        # Unit and integration tests
│   ├── __init__.py
│   ├── test_downloaders/
│   ├── test_processors/
│   ├── test_exporters/
│   └── test_integration.py
│
├── config/                       # Configuration files
│   ├── default_config.yaml      # Default configuration
│   ├── dev_config.yaml          # Development settings
│   └── regions.json             # US agricultural regions
│
├── data/                         # Data directory (git-ignored)
│   ├── raw/                     # Raw downloaded data
│   │   ├── field_boundaries/
│   │   ├── soil/
│   │   ├── weather/
│   │   ├── imagery/
│   │   └── cropland/
│   │
│   ├── processed/               # Processed data
│   │   ├── integrated/         # Multi-source integrated datasets
│   │   └── export/             # Export-ready files
│   │
│   └── metadata/                # Dataset metadata
│       ├── download_log.json
│       ├── field_catalog.csv
│       └── data_summary.json
│
├── notebooks/                    # Jupyter notebooks
│   ├── 01_data_exploration.ipynb
│   ├── 02_soil_analysis.ipynb
│   ├── 03_weather_patterns.ipynb
│   ├── 04_ndvi_calculation.ipynb
│   └── 05_integrated_analysis.ipynb
│
└── examples/                     # Example workflows
    ├── basic_download.py
    ├── field_analysis.py
    ├── soil_health_metrics.py
    └── dashboard_data_prep.py
```

## 🚀 Installation

### Prerequisites

- **Operating System**: Ubuntu LTS 20.04+ (or compatible Linux distribution)
- **Python**: 3.9 or higher
- **Git**: Version control system
- **Disk Space**: Minimum 50GB free (for full dataset)
- **Memory**: 8GB RAM recommended

### Quick Install

```bash
# Clone the repository
git clone https://github.com/borealBytes/agri-data-toolkit.git
cd agri-data-toolkit

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Or use Poetry (recommended)
poetry install

# Setup workspace
python scripts/setup_workspace.py
```

Detailed installation instructions: [docs/installation.md](docs/installation.md)

## 🏃 Quick Start

### 1. Download Core Dataset Package

```bash
# Download all required data sources (~200 fields)
python scripts/download_core.py --fields 200 --years 2020-2024

# With specific region focus
python scripts/download_core.py --region "corn_belt" --fields 200

# Download with validation
python scripts/download_core.py --fields 200 --validate
```

### 2. Validate Downloaded Data

```bash
# Check data completeness and quality
python scripts/validate_data.py --report
```

### 3. Generate Data Summary

```bash
# Create summary report
python scripts/generate_report.py --output reports/data_summary.html
```

### 4. Use in Python

```python
from agri_toolkit.downloaders import FieldBoundaryDownloader
from agri_toolkit.processors import SpatialProcessor

# Download field boundaries
downloader = FieldBoundaryDownloader(config="config/default_config.yaml")
fields = downloader.download(count=200, regions=["corn_belt", "great_plains"])

# Process and integrate soil data
processor = SpatialProcessor()
fields_with_soil = processor.join_soil_data(fields, soil_source="ssurgo")

# Export for analysis
processor.export(fields_with_soil, format="geojson", output="data/processed/fields_with_soil.geojson")
```

Detailed usage guide: [docs/quickstart.md](docs/quickstart.md)

## 📚 Usage Examples

See the [examples/](examples/) directory for complete workflows:

- **Basic Download**: Acquire all core datasets
- **Field Analysis**: Field-level soil and weather integration
- **Soil Health Metrics**: Calculate sustainability indicators
- **NDVI Time Series**: Vegetation index calculation and analysis
- **Dashboard Data Prep**: Prepare integrated datasets for visualization

## 🗺️ Development Roadmap

### Phase 1: Core Data Download (Current)
**Status**: 🚧 In Development

- [x] Project structure setup
- [x] Repository initialization
- [ ] Field boundary downloader
- [ ] SSURGO soil data integration
- [ ] NASA POWER weather API
- [ ] NOAA climate data integration
- [ ] Sentinel-2 imagery downloader
- [ ] Landsat imagery downloader
- [ ] USDA CDL integration
- [ ] Basic validation framework

**Target**: Week 1 of course

### Phase 2: Data Processing & Integration
**Status**: 📋 Planned

- [ ] Spatial join operations
- [ ] Temporal alignment
- [ ] NDVI calculation
- [ ] Multi-layer integration
- [ ] Export pipeline
- [ ] Metadata generation

**Target**: Week 2-3 of course

### Phase 3: Advanced Features
**Status**: 📋 Planned

- [ ] Parallel processing
- [ ] Incremental updates
- [ ] Custom AOI support
- [ ] Advanced validation
- [ ] Performance optimization

**Target**: Week 4-5 of course

### Phase 4: Optional Datasets & Extensions
**Status**: 📋 Planned

- [ ] USDA NASS statistics
- [ ] USDA ERS data
- [ ] Precision ag equipment data parsers
- [ ] Additional satellite sources
- [ ] Soil moisture products

**Target**: Week 6-8 of course (bonus features)

### Phase 5: Production Readiness
**Status**: 💡 Future

- [ ] Comprehensive unit tests (>80% coverage)
- [ ] Integration tests
- [ ] CI/CD pipeline
- [ ] Docker containerization
- [ ] API documentation (Sphinx)
- [ ] Performance benchmarks

**Target**: Post-course maintenance

## 🎯 Key Design Principles

1. **Modularity**: Each data source is an independent module
2. **Configurability**: YAML-based configuration for all parameters
3. **Validation**: Built-in data quality checks at every stage
4. **Logging**: Comprehensive logging for debugging and auditing
5. **Documentation**: Clear documentation for all functions and classes
6. **Testing**: Unit and integration tests for reliability
7. **Ubuntu Compatibility**: Designed for command-line use on Ubuntu LTS
8. **Educational Focus**: Code is readable and well-commented for learning

## 🤝 Contributing

This project is part of an educational course, but contributions are welcome!

Please read [CONTRIBUTING.md](docs/contributing.md) for details on:

- Code style guidelines (Black, isort, flake8)
- Commit message conventions
- Testing requirements
- Pull request process

### Development Setup

```bash
# Clone and setup
git clone https://github.com/borealBytes/agri-data-toolkit.git
cd agri-data-toolkit

# Install development dependencies
poetry install --with dev

# Run tests
pytest tests/

# Run linters
black src/
flake8 src/
isort src/
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

### Course Students

- **Office Hours**: 30 minutes before Classes 2-14
- **Teaching Assistant**: Available during course run (Feb 12 - Mar 31, 2026)
- **GitHub Issues**: Use the issue tracker for bug reports and feature requests

### General Users

- **Documentation**: [docs/](docs/)
- **GitHub Issues**: Bug reports and questions
- **Discussions**: Community Q&A and feature discussions

## 🙏 Acknowledgments

### Data Sources

- **USDA**: Field boundaries, NASS statistics, Cropland Data Layer
- **NRCS**: SSURGO soil survey data
- **NASA**: POWER weather API
- **NOAA**: Climate data
- **ESA**: Sentinel-2 imagery
- **USGS**: Landsat imagery

### Course Context

- **Instructor**: Clayton Young (ex-Bayer, ex-Monsanto, ex-Climate Corporation)
- **Institution**: ELVTR
- **Course**: Agricultural Data Analytics
- **Duration**: 8 weeks, 14 lessons

## 📞 Contact

**Instructor**: Clayton Young  
**GitHub**: [@borealBytes](https://github.com/borealBytes)  
**Course Platform**: ELVTR  

---

**Built with ❤️ for agricultural data science education and precision agriculture applications.**
