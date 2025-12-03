# 🌾 Agricultural Data Toolkit

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.13](https://img.shields.io/badge/python-3.13-blue.svg)](https://www.python.org/downloads/)
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