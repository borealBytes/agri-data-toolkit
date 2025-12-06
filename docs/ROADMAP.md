# Development Roadmap

Detailed implementation plan for the Agricultural Data Toolkit, aligned with the 8-week Agricultural Data Analytics course timeline.

## Timeline Overview

**Course Dates**: February 12 - March 31, 2026
**Development Start**: December 2025
**Production Ready**: February 10, 2026 (before Welcome Class)

## Phase 1: Foundation & Core Downloads
**Timeline**: Weeks 1-2 (December 2025)
**Status**: 🚧 In Progress

### Week 1: Project Setup

- [x] Repository initialization
- [x] Project structure definition
- [x] README and documentation framework
- [x] License and contribution guidelines
- [ ] Python package structure (`src/agri_toolkit/`)
- [ ] Configuration system (YAML-based)
- [ ] Logging framework
- [ ] Base downloader class
- [ ] Error handling patterns

### Week 2: Field Boundaries & Soil Data

**Priority: HIGH** (Required for Class 02, Assignment 1)

#### Field Boundary Downloader
- [ ] Data source identification (sample dataset vs CLU)
- [ ] Region-based sampling (Corn Belt, Great Plains, Southeast)
- [ ] Crop type filtering (corn, soy, wheat, cotton)
- [ ] Field size constraints (40-640 acres)
- [ ] Output formats: GeoJSON, Shapefile
- [ ] Metadata generation (field catalog)
- [ ] Unit tests for boundary validation

**Deliverable**: `python scripts/download_core.py --fields 200` works

#### SSURGO Soil Data Integration
- [ ] SSURGO API wrapper (Web Soil Survey)
- [ ] Spatial join with field boundaries
- [ ] Attribute selection (OM, pH, texture, drainage, AWC)
- [ ] Area-weighted averaging for multi-unit fields
- [ ] Missing value handling
- [ ] CSV output with field join keys
- [ ] Unit tests for soil data extraction

**Deliverable**: Fields have associated soil properties

**Milestone**: Students can download and explore fields + soil (Assignment 1)

---

## Phase 2: Weather & Climate Data
**Timeline**: Weeks 3-4 (January 2026)
**Status**: 📋 Planned

### Week 3: NASA POWER Integration

**Priority: HIGH** (Required for Class 03, Assignment 1)

- [ ] NASA POWER API client
- [ ] Field centroid extraction
- [ ] Parameter selection (temp, precip, solar, humidity, wind)
- [ ] Date range queries (2020-2024)
- [ ] Daily time series CSV output
- [ ] Rate limiting and retry logic
- [ ] Unit tests for weather download

**Deliverable**: Weather data for all fields (2020-2024)

### Week 4: NOAA Climate Data

**Priority: MEDIUM** (Complementary to NASA POWER)

- [ ] NOAA CDO API client
- [ ] Station search (nearest stations to fields)
- [ ] Inverse distance weighting interpolation
- [ ] Climate normals integration
- [ ] Quality flag handling
- [ ] Integration with NASA POWER data
- [ ] Unit tests for NOAA data

**Deliverable**: Enhanced weather dataset with station observations

**Milestone**: Complete weather/climate data package (Assignment 1, Class 08)

---

## Phase 3: Satellite Imagery
**Timeline**: Weeks 5-6 (January-February 2026)
**Status**: 📋 Planned

### Week 5: Sentinel-2 Downloader

**Priority: HIGH** (Required for Class 07, Assignment 5)

- [ ] Sentinel Hub API or Google Earth Engine integration
- [ ] Field boundary clipping
- [ ] Band selection (B4-Red, B8-NIR minimum)
- [ ] Cloud cover filtering (< 20%)
- [ ] Growing season focus (June-September)
- [ ] Cloud-Optimized GeoTIFF output
- [ ] Metadata (acquisition date, cloud cover, etc.)
- [ ] Unit tests for imagery download

**Deliverable**: Sentinel-2 imagery for all fields (summer 2024)

### Week 6: Landsat & NDVI Calculation

**Priority: MEDIUM** (Alternative to Sentinel-2)

#### Landsat Downloader
- [ ] USGS EarthExplorer API or Google Earth Engine
- [ ] Field boundary clipping
- [ ] Band selection (B4-Red, B5-NIR)
- [ ] Cloud masking using QA bands
- [ ] Temporal compositing (cloud-free)
- [ ] Unit tests for Landsat data

#### Vegetation Indices Processor
- [ ] NDVI calculation: (NIR - Red) / (NIR + Red)
- [ ] EVI calculation (Enhanced Vegetation Index)
- [ ] NDWI calculation (water stress)
- [ ] Per-field zonal statistics (mean, std, percentiles)
- [ ] Time series output (CSV)
- [ ] Unit tests for indices

**Deliverable**: NDVI time series for all fields

**Milestone**: Complete satellite imagery package (Assignment 5, Class 07)

---

## Phase 4: Cropland Data & Integration
**Timeline**: Week 7 (February 2026)
**Status**: 📋 Planned

### Cropland Data Layer (CDL)

**Priority: MEDIUM** (Useful for field classification)

- [ ] USDA CropScape API or direct download
- [ ] Annual layers (2020-2024)
- [ ] Field-level crop extraction (modal value)
- [ ] Crop rotation analysis (year-to-year)
- [ ] Integration with field metadata
- [ ] Unit tests for CDL extraction

**Deliverable**: Crop type classification per field per year

### Multi-Source Integration

**Priority: HIGH** (Required for Final Project)

- [ ] Spatial join processor (fields + soil)
- [ ] Temporal alignment (weather + imagery)
- [ ] Zonal statistics (imagery -> field attributes)
- [ ] Master integrated dataset (GeoJSON + CSV)
- [ ] Data dictionary generation
- [ ] Export to multiple formats (Shapefile, GeoParquet, CSV)
- [ ] Unit tests for integration pipeline

**Deliverable**: Single integrated dataset ready for dashboard

**Milestone**: Full data package ready for analysis (Assignment 7, Final Project)

---

## Phase 5: Validation & Documentation
**Timeline**: Week 8 (February 1-10, 2026)
**Status**: 📋 Planned

### Data Validation Framework

**Priority: HIGH** (Critical for data quality)

- [ ] Completeness checks (all fields have all layers)
- [ ] Spatial validity (valid geometries, correct CRS)
- [ ] Temporal coverage (date ranges complete)
- [ ] Value range validation (realistic values)
- [ ] Cross-layer consistency (spatial alignment)
- [ ] Automated validation report generation
- [ ] Auto-fix common issues (re-projection, missing values)
- [ ] Unit tests for validators

**Deliverable**: `python scripts/validate_data.py --report`

### Comprehensive Documentation

- [ ] API reference (Sphinx auto-generated)
- [ ] Data sources guide (detailed)
- [ ] Usage examples (5+ complete workflows)
- [ ] Troubleshooting guide
- [ ] Course assignment alignment guide
- [ ] Video walkthrough (optional)
- [ ] FAQ document

**Deliverable**: Complete documentation site

**Milestone**: Production-ready toolkit for course start (Feb 12)

---

## Phase 6: Optional Datasets & Extensions
**Timeline**: Weeks 9-10 (Mid-course, March 2026)
**Status**: 💡 Future

### USDA NASS/ERS Statistics

**Priority: LOW** (Bonus feature for Class 06)

- [ ] USDA Quick Stats API client
- [ ] County-level yield data download
- [ ] State-level aggregates
- [ ] Economic indicators (optional)
- [ ] Join to field boundaries by county
- [ ] Unit tests

**Deliverable**: County-level context data for choropleth maps

### Precision Ag Equipment Data Parsers

**Priority: LOW** (Instructor demo only, Class 10)

- [ ] John Deere Operations Center export parser
- [ ] Climate FieldView export parser
- [ ] Shapefile standardization
- [ ] Planter data structure
- [ ] Yield monitor data structure
- [ ] Example datasets
- [ ] Documentation

**Deliverable**: Parsers for instructor demo data

---

## Phase 7: Advanced Features
**Timeline**: Post-course (April 2026+)
**Status**: 💡 Future

### Performance Optimization

- [ ] Parallel downloads (multi-threading)
- [ ] Batch processing (chunked downloads)
- [ ] Caching layer (avoid re-downloads)
- [ ] Incremental updates (only new data)
- [ ] Memory-efficient raster processing
- [ ] Streaming GeoJSON processing
- [ ] Performance benchmarks

**Target**: 10x faster downloads for large datasets

### Custom AOI Support

- [ ] User-defined field boundaries (upload)
- [ ] Draw AOI on web map interface
- [ ] State/county-level bulk downloads
- [ ] Custom crop type filtering
- [ ] Flexible date ranges
- [ ] Configuration presets

**Target**: Support any US agricultural area

### Production Features

- [ ] Docker containerization
- [ ] CI/CD pipeline (GitHub Actions)
- [ ] Automated testing (>80% coverage)
- [ ] Code coverage reporting
- [ ] Performance regression tests
- [ ] Security scanning
- [ ] Release automation

**Target**: Production-grade reliability

---

## Key Milestones

| Date | Milestone | Status |
|------|-----------|--------|
| Dec 31, 2025 | Phase 1 Complete (Fields + Soil) | 🚧 In Progress |
| Jan 15, 2026 | Phase 2 Complete (Weather) | 📋 Planned |
| Jan 31, 2026 | Phase 3 Complete (Imagery) | 📋 Planned |
| Feb 7, 2026 | Phase 4 Complete (Integration) | 📋 Planned |
| **Feb 10, 2026** | **Production Ready** | 📋 Planned |
| Feb 12, 2026 | Course Starts (Welcome Class) | 📅 Scheduled |
| Mar 31, 2026 | Course Ends | 📅 Scheduled |
| Apr 15, 2026 | Phase 6 Complete (Optional) | 💡 Future |

---

## Course Timeline Alignment

### Week 1 (Feb 12-16)
- **Class 02**: Requires fields + soil + basic download
- **Class 03**: Requires full core package
- **Assignment 1**: Field data acquisition

✅ **Phase 1 & 2 must be complete**

### Weeks 2-3 (Feb 19-27)
- **Class 04-05**: Data cleaning and EDA
- **Assignment 2**: Data integration
- **Assignment 3**: EDA

✅ **All core data available**

### Weeks 4-5 (Mar 4-13)
- **Class 06-07**: Geospatial analysis and satellite
- **Assignment 4**: Geospatial mapping
- **Assignment 5**: NDVI calculation

✅ **Phase 3 (imagery) must be complete**

### Weeks 6-7 (Mar 18-27)
- **Class 08-09**: Weather analysis, advanced spatial
- **Assignment 6**: Weather trends
- **Assignment 7**: Integrated spatial analysis

✅ **Phase 4 (integration) must be complete**

### Week 8 (Mar 31)
- **Class 13-14**: Ethics, future trends
- **Final Project**: Row Crop Intelligence Dashboard

✅ **Complete integrated dataset**

---

## Risk Management

### Critical Path Items

1. **Field Boundaries**:
   - Risk: Sample data may not be representative
   - Mitigation: Manual curation of diverse regions/crops

2. **SSURGO Complexity**:
   - Risk: Complex data structure, slow API
   - Mitigation: Pre-processed extracts, bulk download

3. **Satellite Imagery**:
   - Risk: Cloud cover, API rate limits, large file sizes
   - Mitigation: Pre-downloaded cache, cloud-optimized formats

4. **Timeline Pressure**:
   - Risk: Course starts Feb 12, tight deadline
   - Mitigation: Focus on core features first, optional later

### Contingency Plans

- **Plan A**: Full automated download (ideal)
- **Plan B**: Hybrid (some pre-processed, some automated)
- **Plan C**: Pre-packaged dataset (minimal automation)

**Decision Point**: January 20, 2026

---

## Success Criteria

### Minimum Viable Product (MVP)

By February 10, 2026:

✅ 200 field boundaries downloaded
✅ Soil data joined to all fields
✅ Weather data (2020-2024) for all fields
✅ Satellite imagery (summer 2024) for all fields
✅ Validation passing (>95% complete)
✅ Documentation complete
✅ Example workflows tested
✅ Ubuntu LTS compatible

### Stretch Goals

✅ NOAA station data integrated
✅ Cropland Data Layer included
✅ Automated validation with auto-fix
✅ Performance optimizations (parallel)
✅ Jupyter notebooks (5+ examples)
✅ Docker container available

---

## Resources Required

### Development Resources
- **Developer Time**: ~150 hours (Dec-Feb)
- **Testing Time**: ~40 hours
- **Documentation**: ~30 hours
- **Total**: ~220 hours (~28 days FTE)

### Compute Resources
- **Storage**: 100GB for full dataset
- **Bandwidth**: ~50GB downloads
- **API Credits**: $0 (all free/public data sources)

### Third-Party Services
- **GitHub**: Free (public repo)
- **NASA POWER**: Free API
- **NOAA**: Free API (registration required)
- **Sentinel Hub**: Free tier or Google Earth Engine
- **USGS**: Free

---

## Maintenance Plan

### During Course (Feb-Mar 2026)
- **Bug Fixes**: Priority response within 24 hours
- **Student Support**: Office hours and issue tracker
- **Data Updates**: As needed (re-run downloads)
- **Documentation Updates**: Based on student feedback

### Post-Course (Apr 2026+)
- **Quarterly Updates**: Data refresh
- **Annual Updates**: Dependency upgrades
- **Long-term**: Community-driven enhancements

---

## Version History

- **v0.1.0** (Dec 3, 2025): Repository initialized, project structure defined
- **v0.2.0** (Planned Jan 2026): Core downloaders (fields, soil, weather)
- **v0.3.0** (Planned Feb 2026): Imagery and integration
- **v1.0.0** (Target Feb 10, 2026): Production release for course
- **v1.1.0** (Planned Apr 2026): Optional features and optimizations

---

## Contact & Updates

**Project Lead**: Clayton Young (@borealBytes)
**Repository**: https://github.com/borealBytes/agri-data-toolkit
**Issues**: https://github.com/borealBytes/agri-data-toolkit/issues
**Discussions**: https://github.com/borealBytes/agri-data-toolkit/discussions

Updates will be posted weekly in the course portal during development.
