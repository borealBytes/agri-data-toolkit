# Installation Guide

## System Requirements

### Operating System
- **Primary**: Ubuntu LTS 20.04, 22.04, or 24.04
- **Compatible**: Debian 10+, other Linux distributions
- **Not Supported**: Windows (use WSL2), macOS (may work with modifications)

### Hardware Requirements
- **CPU**: 2+ cores (4+ recommended)
- **RAM**: 8GB minimum (16GB recommended for large datasets)
- **Storage**: 50GB free disk space (100GB+ recommended)
- **Network**: Broadband internet connection for data downloads

### Software Prerequisites
- **Python**: 3.9, 3.10, 3.11, or 3.12
- **Git**: 2.25+
- **GDAL**: 3.0+ (for geospatial operations)

## Installation Methods

### Method 1: Standard Installation (Recommended)

#### 1. Install System Dependencies

```bash
# Update package list
sudo apt update

# Install Python and development tools
sudo apt install -y python3 python3-pip python3-venv

# Install GDAL and geospatial libraries
sudo apt install -y gdal-bin libgdal-dev python3-gdal

# Install Git
sudo apt install -y git

# Verify installations
python3 --version  # Should be 3.9+
git --version      # Should be 2.25+
gdalinfo --version # Should be 3.0+
```

#### 2. Clone Repository

```bash
# Clone the repository
git clone https://github.com/borealBytes/agri-data-toolkit.git

# Navigate to directory
cd agri-data-toolkit
```

#### 3. Create Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip
```

#### 4. Install Python Dependencies

```bash
# Install all dependencies
pip install -r requirements.txt

# Verify installation
python -c "import geopandas; print('GeoPandas version:', geopandas.__version__)"
python -c "import rasterio; print('Rasterio version:', rasterio.__version__)"
```

#### 5. Setup Workspace

```bash
# Create necessary directories and initial configuration
python scripts/setup_workspace.py

# This will:
# - Create data directories
# - Copy default configuration
# - Validate system setup
# - Generate initial metadata files
```

### Method 2: Poetry Installation (Advanced)

Poetry provides better dependency management and isolation.

```bash
# Install Poetry
curl -sSL https://install.python-poetry.org | python3 -

# Add Poetry to PATH (add to ~/.bashrc for persistence)
export PATH="$HOME/.local/bin:$PATH"

# Clone repository
git clone https://github.com/borealBytes/agri-data-toolkit.git
cd agri-data-toolkit

# Install dependencies
poetry install

# Activate Poetry shell
poetry shell

# Setup workspace
python scripts/setup_workspace.py
```

### Method 3: Development Installation

For contributors and course instructors who need development tools.

```bash
# Clone repository
git clone https://github.com/borealBytes/agri-data-toolkit.git
cd agri-data-toolkit

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install with development dependencies
pip install -r requirements-dev.txt

# Install pre-commit hooks
pre-commit install

# Run tests to verify installation
pytest tests/
```

## Configuration

### 1. Copy Default Configuration

```bash
# Copy default config for customization
cp config/default_config.yaml config/user_config.yaml
```

### 2. Edit Configuration (Optional)

```bash
# Edit with your preferred editor
nano config/user_config.yaml
# or
code config/user_config.yaml
```

Key configuration options:

```yaml
# Number of fields to download
field_count: 200

# US agricultural regions to include
regions:
  - corn_belt
  - great_plains
  - southeast

# Years for temporal data
year_range:
  start: 2020
  end: 2024

# Output directory
output_dir: "data/raw"

# Coordinate reference systems
crs:
  wgs84: "EPSG:4326"
  albers: "EPSG:5070"
```

### 3. Set Up API Keys (If Required)

Some data sources may require API keys:

```bash
# Create .env file
cp .env.example .env

# Edit .env and add your API keys
nano .env
```

Example `.env` file:

```bash
# NASA POWER API (usually no key required)
NASA_POWER_API_KEY=

# Sentinel Hub (if using direct access)
SENTINEL_HUB_CLIENT_ID=
SENTINEL_HUB_CLIENT_SECRET=

# Google Earth Engine (optional)
GEE_SERVICE_ACCOUNT=
GEE_PRIVATE_KEY_PATH=
```

## Verification

### Quick System Check

```bash
# Run system verification
python scripts/verify_installation.py

# Expected output:
# ✓ Python 3.9+ detected
# ✓ GDAL installed
# ✓ All required packages installed
# ✓ Data directories created
# ✓ Configuration valid
# ✓ System ready for data download
```

### Test Download (Small Dataset)

```bash
# Download a single field as test
python scripts/download_core.py --fields 1 --test-mode

# This should download:
# - 1 field boundary
# - Associated soil data
# - Weather data for field location
# - One satellite image
```

## Troubleshooting

### GDAL Installation Issues

**Problem**: `ImportError: No module named 'osgeo'`

```bash
# Solution 1: Install GDAL Python bindings
pip install gdal==$(gdal-config --version)

# Solution 2: Use conda (if applicable)
conda install -c conda-forge gdal
```

### Memory Errors During Installation

**Problem**: `MemoryError` during pip install

```bash
# Solution: Install packages one at a time
pip install --no-cache-dir geopandas
pip install --no-cache-dir rasterio
pip install -r requirements.txt
```

### Permission Denied Errors

**Problem**: Cannot create directories

```bash
# Solution: Ensure you have write permissions
sudo chown -R $USER:$USER ~/agri-data-toolkit

# Or run setup with sudo (not recommended)
sudo python scripts/setup_workspace.py
```

### Python Version Issues

**Problem**: System has Python 2 or Python 3.8

```bash
# Install Python 3.11 via deadsnakes PPA
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install python3.11 python3.11-venv python3.11-dev

# Use specific Python version
python3.11 -m venv venv
```

## Uninstallation

### Remove Installation

```bash
# Deactivate virtual environment
deactivate

# Remove repository
cd ..
rm -rf agri-data-toolkit
```

### Clean Data Only

```bash
# Remove downloaded data but keep code
cd agri-data-toolkit
rm -rf data/raw/*
rm -rf data/processed/*
rm -rf data/metadata/*
```

## Next Steps

After successful installation:

1. Read the [Quick Start Guide](quickstart.md)
2. Review [Data Sources Documentation](data_sources.md)
3. Try [Basic Usage Examples](examples/basic_usage.md)
4. Download your first dataset: `python scripts/download_core.py --fields 200`

## Support

For installation issues:

1. Check [GitHub Issues](https://github.com/borealBytes/agri-data-toolkit/issues)
2. Review course office hours schedule
3. Post in course discussion forum
4. Contact teaching assistant
