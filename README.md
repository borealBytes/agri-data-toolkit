# 🌾 Agricultural Data Toolkit

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.13](https://img.shields.io/badge/python-3.13-blue.svg)](https://www.python.org/downloads/)
[![Poetry](https://img.shields.io/badge/dependency%20manager-Poetry-blue)](https://python-poetry.org/)
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

See [docs/data_sources.md](docs/data_sources.md) for comprehensive documentation.

### Required Data Sources

1. **Field Boundaries** - ~200 row crop fields across US regions
2. **NRCS SSURGO Soil Data** - Organic matter, pH, texture, drainage
3. **NASA POWER Weather** - Daily meteorological time series (2020-2024)
4. **NOAA Climate** - Weather station observations
5. **Sentinel-2 & Landsat** - Multispectral satellite imagery
6. **USDA Cropland Data Layer** - Crop type classifications

### Optional Data Sources

7. **USDA NASS/ERS Statistics** - County-level aggregated data
8. **Precision Ag Equipment Data** - Planter/combine data (instructor demos)

## 📁 Project Structure

See full structure in [README](README.md) or browse the [repository](https://github.com/borealBytes/agri-data-toolkit).

## 🚀 Installation

### Prerequisites

- **Operating System**: Ubuntu LTS 20.04+ (or compatible Linux distribution)
- **Python**: 3.13
- **Poetry**: Python dependency manager
- **Git**: Version control system
- **Disk Space**: Minimum 50GB free (for full dataset)
- **Memory**: 8GB RAM recommended

### Install Poetry

```bash
# Install Poetry (if not already installed)
curl -sSL https://install.python-poetry.org | python3 -

# Add to PATH (add to ~/.bashrc for persistence)
export PATH="$HOME/.local/bin:$PATH"

# Verify installation
poetry --version
```

### Install Toolkit

```bash
# Clone the repository
git clone https://github.com/borealBytes/agri-data-toolkit.git
cd agri-data-toolkit

# Install dependencies
poetry install

# Activate Poetry shell
poetry shell

# Setup workspace
python scripts/setup_workspace.py
```

**That's it!** All dependencies are managed by Poetry.

Detailed installation instructions: [docs/installation.md](docs/installation.md)

## 🏃 Quick Start

### 1. Download Core Dataset Package

```bash
# Activate Poetry environment
poetry shell

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

See [docs/ROADMAP.md](docs/ROADMAP.md) for complete development timeline.

### Current Status: Phase 1 - Foundation

- [x] Repository setup with Poetry
- [x] Python 3.13 configuration
- [x] Project structure
- [x] Documentation framework
- [ ] Core downloaders (in progress)

**Target**: Production ready February 10, 2026

## 🎯 Key Design Principles

1. **Modern Python**: Python 3.13 with latest features
2. **Poetry First**: Professional dependency management
3. **Modularity**: Each data source is an independent module
4. **Configurability**: YAML-based configuration for all parameters
5. **Validation**: Built-in data quality checks at every stage
6. **Testing**: Unit and integration tests for reliability
7. **Ubuntu Compatibility**: Designed for command-line use on Ubuntu LTS
8. **Educational Focus**: Code is readable and well-commented for learning

## 🤝 Contributing

This project is part of an educational course, but contributions are welcome!

Please read [docs/contributing.md](docs/contributing.md) for details on:

- Code style guidelines (Black, isort, flake8)
- Commit message conventions
- Testing requirements
- Pull request process

### Development Setup

```bash
# Clone and setup
git clone https://github.com/borealBytes/agri-data-toolkit.git
cd agri-data-toolkit

# Install with development dependencies
poetry install --with dev

# Activate Poetry shell
poetry shell

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
