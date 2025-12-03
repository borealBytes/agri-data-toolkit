# Data Sources Reference

Comprehensive guide to all agricultural data sources integrated in this toolkit.

## Overview

This toolkit integrates 7 major data sources covering field boundaries, soil properties, weather/climate, satellite imagery, and crop classification. Each source is accessed via APIs, web services, or bulk download portals.

## Core Data Sources (Required)

### 1. Field Boundaries

#### Description
Vector polygons representing individual agricultural fields used for row crop production (corn, soybeans, wheat, cotton) across diverse US regions.

#### Specifications
- **Count**: ~200 fields
- **Geographic Coverage**: 
  - Corn Belt (IL, IA, IN, OH, MN)
  - Great Plains (KS, NE, SD, ND, TX)
  - Southeast (AR, MS, LA, GA)
- **Crop Types**: Corn, soybeans, winter wheat, cotton
- **Field Size Range**: 40-640 acres (typical: 80-160 acres)

#### Data Format
- **Primary**: GeoJSON (EPSG:4326)
- **Alternative**: Shapefile, GeoParquet
- **Attributes**:
  - `field_id`: Unique identifier
  - `region`: Agricultural region
  - `area_acres`: Field area in acres
  - `centroid_lat`: Latitude of field center
  - `centroid_lon`: Longitude of field center
  - `state`: US state abbreviation
  - `county`: County name

#### Data Source
- **Method 1**: Generated from USDA Common Land Unit (CLU) boundaries (restricted access)
- **Method 2**: Digitized from high-resolution imagery (Esri World Imagery)
- **Method 3**: Sample dataset provided with course materials

#### API/Access
```python
from agri_toolkit.downloaders import FieldBoundaryDownloader

downloader = FieldBoundaryDownloader()
fields = downloader.download(
    count=200,
    regions=['corn_belt', 'great_plains', 'southeast'],
    crop_types=['corn', 'soybeans', 'wheat', 'cotton'],
    output_path='data/raw/field_boundaries'
)
```

#### Update Frequency
Static for course; fields represent typical field boundaries that change infrequently (every 3-5 years).

#### License
Depends on source; course sample data provided under CC-BY-4.0.

---

### 2. NRCS SSURGO Soil Data

#### Description
Soil Survey Geographic Database from USDA Natural Resources Conservation Service, providing detailed soil property data at the map unit level.

#### Specifications
- **Spatial Resolution**: Polygon-based (typically 1:12,000 to 1:24,000 scale)
- **Coverage**: All US agricultural areas
- **Attributes** (selected for agriculture):
  - **Organic Matter** (`om_pct`): Percentage, 0-20%
  - **pH** (`ph_water`): pH in water, 3.5-10.0
  - **Texture**: Sand/Silt/Clay percentages
  - **Drainage Class**: Well drained, moderately well drained, etc.
  - **Available Water Capacity** (`awc`): inches/inch, 0-0.25
  - **Bulk Density**: g/cm³
  - **Cation Exchange Capacity**: meq/100g
  - **Electrical Conductivity**: mmhos/cm

#### Data Format
- **Primary**: CSV with join keys to field boundaries
- **Spatial**: Shapefile (original SSURGO polygons)
- **Join Key**: `mukey` (map unit key)

#### Data Source
- **Official Portal**: https://websoilsurvey.sc.egov.usda.gov/
- **Bulk Download**: https://nrcs.app.box.com/v/soils
- **Web Soil Survey API**: SOAP/REST endpoints

#### API/Access
```python
from agri_toolkit.downloaders import SSURGODownloader

downloader = SSURGODownloader()
soil_data = downloader.download_for_fields(
    fields_geojson='data/raw/field_boundaries/fields.geojson',
    attributes=['om_pct', 'ph_water', 'awc', 'drainage_class'],
    output_path='data/raw/soil'
)
```

#### Processing Notes
- Multiple soil map units may intersect a single field
- Use area-weighted averaging for field-level values
- Depth-weighted averaging for multi-horizon properties
- Handle missing values (some properties may be null)

#### Update Frequency
SSURGO is updated annually (October) but soil properties change slowly over time.

#### License
Public domain (US Government work)

---

### 3. NASA POWER Weather Data

#### Description
Prediction Of Worldwide Energy Resources (POWER) project provides meteorological and solar data from NASA satellites and models, specifically designed for agricultural applications.

#### Specifications
- **Temporal Resolution**: Daily
- **Spatial Resolution**: 0.5° x 0.5° (~50km at mid-latitudes)
- **Temporal Coverage**: 1981-present (near real-time)
- **Parameters**:
  - **Temperature**: Daily min, max, average (°C)
  - **Precipitation**: Daily total (mm)
  - **Solar Radiation**: MJ/m²/day
  - **Relative Humidity**: % at 2m
  - **Wind Speed**: m/s at 10m
  - **Dew Point**: °C
  - **Pressure**: kPa

#### Data Format
- **Primary**: CSV with daily time series
- **Columns**: `date`, `field_id`, `temp_min`, `temp_max`, `precip`, `solar_rad`, `rh`, `wind_speed`

#### Data Source
- **API**: https://power.larc.nasa.gov/api/
- **Documentation**: https://power.larc.nasa.gov/docs/

#### API/Access
```python
from agri_toolkit.downloaders import NASAPowerDownloader
import pandas as pd

downloader = NASAPowerDownloader()
weather = downloader.download_for_fields(
    fields_geojson='data/raw/field_boundaries/fields.geojson',
    start_date='2020-01-01',
    end_date='2024-12-31',
    parameters=['T2M_MIN', 'T2M_MAX', 'PRECTOTCORR', 'ALLSKY_SFC_SW_DWN'],
    output_path='data/raw/weather'
)
```

#### Processing Notes
- Use field centroids for location queries
- Data point represents ~2500 km² area (suitable for field-scale analysis)
- Calculate derived variables:
  - Growing Degree Days (GDD)
  - Crop Heat Units
  - Evapotranspiration (via Penman-Monteith)

#### Update Frequency
Daily updates with ~1-2 day lag

#### License
Public domain (NASA data)

---

### 4. NOAA Climate Data

#### Description
National Oceanic and Atmospheric Administration provides weather station observations and climate normals for detailed local weather analysis.

#### Specifications
- **Network**: Global Historical Climatology Network Daily (GHCN-D)
- **Stations**: ~30,000 stations (US), ~100,000 globally
- **Temporal Coverage**: 1763-present (varies by station)
- **Parameters**:
  - Daily precipitation (mm)
  - Min/Max temperature (°C)
  - Snowfall and snow depth (cm)
  - Extreme weather flags

#### Data Format
- **Primary**: CSV with station metadata and observations
- **Structure**: Long format (one row per station-date-parameter)

#### Data Source
- **API**: https://www.ncei.noaa.gov/cdo-web/api/v2/
- **Bulk Download**: https://www.ncei.noaa.gov/data/
- **Climate Normals**: https://www.ncei.noaa.gov/products/land-based-station/us-climate-normals

#### API/Access
```python
from agri_toolkit.downloaders import NOAADownloader

downloader = NOAADownloader(api_token='YOUR_TOKEN')
weather = downloader.download_for_fields(
    fields_geojson='data/raw/field_boundaries/fields.geojson',
    start_date='2020-01-01',
    end_date='2024-12-31',
    max_distance_km=50,  # Find stations within 50km
    output_path='data/raw/weather'
)
```

#### Processing Notes
- Identify nearest weather stations to each field
- Use inverse distance weighting for multi-station interpolation
- Quality flags indicate observation reliability
- Missing data is common (especially for older records)

#### Update Frequency
Daily updates

#### API Key Required
Free registration at https://www.ncei.noaa.gov/cdo-web/token

#### License
Public domain (US Government work)

---

### 5. Satellite Imagery (Sentinel-2 & Landsat)

#### Sentinel-2 (ESA)

**Specifications**:
- **Satellites**: Sentinel-2A (launched 2015), Sentinel-2B (launched 2017)
- **Revisit Time**: 5 days (2-3 days at mid-latitudes with both satellites)
- **Spatial Resolution**: 
  - 10m: Blue (B2), Green (B3), Red (B4), NIR (B8)
  - 20m: Red Edge (B5, B6, B7), SWIR (B11, B12)
  - 60m: Aerosol, Water vapor, Cirrus
- **Swath Width**: 290 km

**Key Bands for Agriculture**:
- **B2 (Blue)**: 490 nm - Water, soil moisture
- **B3 (Green)**: 560 nm - Vegetation vigor
- **B4 (Red)**: 665 nm - Chlorophyll absorption
- **B8 (NIR)**: 842 nm - Vegetation biomass
- **B11 (SWIR)**: 1610 nm - Moisture content

**Data Source**:
- **Copernicus Open Access Hub**: https://scihub.copernicus.eu/
- **Google Earth Engine**: `COPERNICUS/S2_SR`
- **AWS Open Data**: `s3://sentinel-s2-l2a/`

#### Landsat 8/9 (USGS)

**Specifications**:
- **Satellites**: Landsat 8 (2013), Landsat 9 (2021)
- **Revisit Time**: 16 days (8 days combined)
- **Spatial Resolution**: 
  - 30m: Visible, NIR, SWIR
  - 100m: Thermal
  - 15m: Panchromatic

**Key Bands for Agriculture**:
- **B2 (Blue)**: 450-510 nm
- **B3 (Green)**: 530-590 nm
- **B4 (Red)**: 640-670 nm
- **B5 (NIR)**: 850-880 nm
- **B6 (SWIR1)**: 1570-1650 nm

**Data Source**:
- **USGS EarthExplorer**: https://earthexplorer.usgs.gov/
- **Google Earth Engine**: `LANDSAT/LC08/C02/T1_L2`
- **AWS Open Data**: `s3://usgs-landsat/`

#### Data Format
- **Primary**: Cloud-Optimized GeoTIFF (COG)
- **Clipped**: Individual GeoTIFFs per field per date
- **Bands**: Separate files or multi-band stack

#### API/Access
```python
from agri_toolkit.downloaders import Sentinel2Downloader, LandsatDownloader

# Sentinel-2
s2_downloader = Sentinel2Downloader()
s2_imagery = s2_downloader.download_for_fields(
    fields_geojson='data/raw/field_boundaries/fields.geojson',
    start_date='2024-06-01',
    end_date='2024-09-30',
    bands=['B4', 'B8'],  # Red and NIR for NDVI
    cloud_cover_max=20,
    output_path='data/raw/imagery/sentinel2'
)

# Landsat 8/9
landsat_downloader = LandsatDownloader()
landsat_imagery = landsat_downloader.download_for_fields(
    fields_geojson='data/raw/field_boundaries/fields.geojson',
    start_date='2024-06-01',
    end_date='2024-09-30',
    bands=['B4', 'B5'],  # Red and NIR
    cloud_cover_max=20,
    output_path='data/raw/imagery/landsat'
)
```

#### Processing Notes
- **Atmospheric Correction**: Use Surface Reflectance (SR) products
- **Cloud Masking**: Apply QA bands to filter clouds/shadows
- **Temporal Compositing**: Create cloud-free mosaics
- **Indices**: Calculate NDVI, EVI, NDWI, SAVI

#### Update Frequency
- Sentinel-2: Every 5 days
- Landsat: Every 16 days

#### License
- Sentinel-2: Free and open (Copernicus terms)
- Landsat: Public domain (USGS)

---

### 6. USDA Cropland Data Layer (CDL)

#### Description
Annual raster classification of crop types and land cover for the contiguous United States, produced by USDA National Agricultural Statistics Service.

#### Specifications
- **Spatial Resolution**: 30m
- **Temporal Coverage**: 2008-present (annual)
- **Classes**: 100+ crop types and land cover classes
- **Accuracy**: ~85% overall, varies by crop and region

**Major Crop Classes**:
- 1: Corn
- 5: Soybeans
- 24: Winter Wheat
- 27: Rye
- 36: Alfalfa
- 61: Fallow/Idle

#### Data Format
- **Primary**: GeoTIFF (Cloud-Optimized)
- **Clipped**: Per-field rasters
- **Values**: Integer crop codes

#### Data Source
- **USDA CropScape**: https://croplandcros.scinet.usda.gov/
- **Direct Download**: https://www.nass.usda.gov/Research_and_Science/Cropland/Release/

#### API/Access
```python
from agri_toolkit.downloaders import CroplandDataLayerDownloader

downloader = CroplandDataLayerDownloader()
cdl = downloader.download_for_fields(
    fields_geojson='data/raw/field_boundaries/fields.geojson',
    years=[2020, 2021, 2022, 2023, 2024],
    output_path='data/raw/cropland'
)
```

#### Processing Notes
- Extract dominant crop type per field (mode)
- Calculate crop rotation patterns (year-to-year changes)
- Use for field classification validation

#### Update Frequency
Annual (typically released in following year)

#### License
Public domain (USDA)

---

## Optional Data Sources

### 7. USDA NASS Statistics

#### Description
Aggregated agricultural statistics at county, state, and national levels.

**Available Metrics**:
- Crop yield (bu/acre, tons/acre)
- Planted and harvested acreage
- Production volumes
- Crop prices
- Farm economics

#### Data Source
- **Quick Stats API**: https://quickstats.nass.usda.gov/api
- **Web Interface**: https://quickstats.nass.usda.gov/

#### API/Access
```python
from agri_toolkit.downloaders import NASSDownloader

downloader = NASSDownloader(api_key='YOUR_KEY')
yield_data = downloader.download_county_yields(
    commodity='CORN',
    years=range(2015, 2025),
    states=['IOWA', 'ILLINOIS', 'NEBRASKA'],
    output_path='data/raw/nass'
)
```

#### Update Frequency
Varies (monthly to annual depending on metric)

#### API Key Required
Free registration at https://quickstats.nass.usda.gov/api

---

### 8. USDA ERS Data

#### Description
Economic Research Service provides farm economics, policy, and sustainability data.

**Available Datasets**:
- Farm income and balance sheets
- Conservation practices adoption
- Irrigation surveys
- Commodity outlooks

#### Data Source
- **Data Portal**: https://www.ers.usda.gov/data-products/

---

## Data Integration Strategy

### Spatial Join Hierarchy

1. **Field Boundaries** (master layer)
2. **Soil Data** (spatial join or centroid query)
3. **Weather Data** (temporal join on field_id)
4. **Satellite Imagery** (raster extraction per field)
5. **Cropland Data** (raster extraction per field)

### Coordinate System Standardization

- **Input CRS**: Various (WGS84, Albers, State Plane)
- **Processing CRS**: EPSG:5070 (Albers Equal Area Conic) for US
- **Output CRS**: EPSG:4326 (WGS84) for web compatibility

### Temporal Alignment

- **Daily**: Weather data
- **5-16 days**: Satellite imagery
- **Annual**: Cropland Data Layer, yield statistics
- **Static**: Field boundaries, soil properties

---

## Data Quality Considerations

### Known Limitations

**Field Boundaries**:
- May not reflect current boundaries (fields change over time)
- Digitization errors possible

**Soil Data**:
- Based on soil surveys (may be decades old)
- Map unit composition can be complex
- Properties averaged over depth and area

**Weather Data**:
- NASA POWER: Coarse spatial resolution (50km)
- NOAA: Station coverage varies; interpolation required

**Satellite Imagery**:
- Cloud cover limits availability
- Atmospheric effects
- Mixed pixels at field edges

**Cropland Data**:
- Classification errors (~15% overall)
- Small fields may be misclassified
- Transition zones problematic

### Quality Assurance

The toolkit implements automatic validation:

```python
from agri_toolkit.core.validators import DataValidator

validator = DataValidator()
report = validator.validate_all(
    data_dir='data/raw',
    checks=['completeness', 'spatial_validity', 'temporal_coverage', 'value_ranges']
)
print(report.summary())
```

---

## References

1. NRCS SSURGO: https://www.nrcs.usda.gov/resources/data-and-reports/soil-survey-geographic-database-ssurgo
2. NASA POWER: https://power.larc.nasa.gov/
3. NOAA NCEI: https://www.ncei.noaa.gov/
4. Sentinel-2: https://sentinels.copernicus.eu/web/sentinel/missions/sentinel-2
5. Landsat: https://www.usgs.gov/landsat-missions
6. USDA CDL: https://www.nass.usda.gov/Research_and_Science/Cropland/SARS1a.php
7. USDA NASS: https://www.nass.usda.gov/
8. USDA ERS: https://www.ers.usda.gov/
