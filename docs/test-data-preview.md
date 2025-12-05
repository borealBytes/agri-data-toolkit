# Test Data Visualization

The CI/CD pipeline automatically generates an interactive map of test data and posts it as a comment on pull requests.

## Features

- 🗺️ Interactive map with OpenStreetMap, Satellite, Terrain backgrounds
- 🔍 Field dropdown to zoom to specific polygons
- 📊 Metadata popups (Field ID, state, county, crop, acreage)
- 📦 Self-contained HTML (no server required)
- 💬 Auto-updating PR comments (one per Python version)

## How It Works

1. Tests run and download field boundaries
2. `scripts/generate_test_map.py` creates interactive HTML
3. Map uploaded as GitHub Actions artifact
4. Comment posted/updated on PR with download link

## Using the Map

### Download

1. Go to workflow run (link in PR comment)
2. Download `test-data-map-py3.13.zip` from artifacts
3. Extract and open `test_data_map.html`

### Controls

- **Base Map**: Dropdown to switch backgrounds
- **Field Select**: Choose field to zoom and inspect
- **Click Fields**: View metadata popup

## Comment States

### Success
```
✅ Test Data Preview (Python 3.13)
Tests Passed - Map generated with download link
```

### No Data
```
⚠️ Test Data Preview (Python 3.13)
No test data found
```

### Failed
```
❌ Test Data Preview (Python 3.13)
Tests failed - check logs
```

## Technical Details

**Script**: `scripts/generate_test_map.py`
**Tech**: Leaflet.js + embedded GeoJSON
**Size**: ~10-50 KB per field
**Retention**: 7 days

## Future Enhancements

- Multi-layer overlays (soil, weather, imagery)
- Summary statistics and charts
- Comparison mode (before/after)
- Export capabilities
