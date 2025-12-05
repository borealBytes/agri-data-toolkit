#!/usr/bin/env python3
"""Generate interactive test data visualization map.

This script creates a self-contained HTML map showing field boundaries
downloaded during testing. The map includes:
- OpenStreetMap background (selectable base maps)
- Field polygons with metadata
- Dropdown to select and zoom to specific fields
- All field attributes displayed on click

Usage:
    python scripts/generate_test_map.py <geojson_file> <output_html>
"""

import json
import sys
from pathlib import Path


def generate_map_html(geojson_path: Path, output_path: Path) -> None:
    """Generate self-contained interactive HTML map.

    Args:
        geojson_path: Path to GeoJSON file with test data
        output_path: Path to output HTML file
    """
    # Load GeoJSON data
    with open(geojson_path) as f:
        geojson_data = json.load(f)

    # Extract features for dropdown
    features = geojson_data.get("features", [])

    if not features:
        raise ValueError("No features found in GeoJSON file")

    # Build field dropdown options
    field_options = []
    for i, feature in enumerate(features):
        props = feature.get("properties", {})
        field_id = props.get("field_id", f"Field {i+1}")
        state = props.get("state", "")
        crop = props.get("crop_2023", "")
        acres = props.get("area_acres", 0)
        label = f"{field_id} - {state} - {crop} ({acres:.1f} ac)"
        field_options.append({"index": i, "label": label})

    # Create HTML with embedded GeoJSON
    html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Field Boundary Test Data Preview</title>
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: #f5f5f5;
        }}
        #map {{
            width: 100%;
            height: 100vh;
        }}
        .controls {{
            position: absolute;
            top: 10px;
            right: 10px;
            z-index: 1000;
            background: white;
            padding: 15px;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.15);
            max-width: 350px;
        }}
        .control-group {{
            margin-bottom: 12px;
        }}
        .control-group:last-child {{
            margin-bottom: 0;
        }}
        label {{
            display: block;
            font-size: 12px;
            font-weight: 600;
            margin-bottom: 4px;
            color: #333;
        }}
        select {{
            width: 100%;
            padding: 8px;
            border: 1px solid #ddd;
            border-radius: 4px;
            font-size: 13px;
            background: white;
            cursor: pointer;
        }}
        select:focus {{
            outline: none;
            border-color: #4A90E2;
        }}
        .stats {{
            margin-top: 12px;
            padding-top: 12px;
            border-top: 1px solid #eee;
            font-size: 11px;
            color: #666;
        }}
        .stats div {{
            margin-bottom: 4px;
        }}
        .stats strong {{
            color: #333;
        }}
        h3 {{
            font-size: 14px;
            margin-bottom: 10px;
            color: #333;
        }}
        .legend {{
            position: absolute;
            bottom: 30px;
            left: 10px;
            z-index: 1000;
            background: white;
            padding: 10px;
            border-radius: 6px;
            box-shadow: 0 2px 6px rgba(0,0,0,0.15);
            font-size: 11px;
        }}
        .legend-title {{
            font-weight: 600;
            margin-bottom: 6px;
            font-size: 12px;
        }}
        .legend-item {{
            margin-bottom: 4px;
        }}
        .legend-color {{
            display: inline-block;
            width: 16px;
            height: 16px;
            margin-right: 6px;
            border: 2px solid #333;
            border-radius: 3px;
            vertical-align: middle;
        }}
    </style>
</head>
<body>
    <div id="map"></div>
    
    <div class="controls">
        <h3>🌾 Field Boundary Test Data</h3>
        
        <div class="control-group">
            <label for="basemap">Base Map:</label>
            <select id="basemap">
                <option value="osm">OpenStreetMap</option>
                <option value="topo">OpenTopoMap</option>
                <option value="satellite">Satellite (ESRI)</option>
                <option value="terrain">Terrain (Stamen)</option>
            </select>
        </div>
        
        <div class="control-group">
            <label for="field-select">Select Field:</label>
            <select id="field-select">
                <option value="all">All Fields (Fit Bounds)</option>
                {"\n                ".join([f'<option value="{opt["index"]}">{opt["label"]}</option>' for opt in field_options])}
            </select>
        </div>
        
        <div class="stats">
            <div><strong>Total Fields:</strong> {len(features)}</div>
            <div><strong>Python Version:</strong> {sys.version.split()[0]}</div>
            <div><strong>Test Run:</strong> CI/CD Pipeline</div>
        </div>
    </div>
    
    <div class="legend">
        <div class="legend-title">Field Boundaries</div>
        <div class="legend-item">
            <span class="legend-color" style="background: rgba(66, 135, 245, 0.3);"></span>
            Agricultural Fields
        </div>
    </div>

    <script>
        // Embedded GeoJSON data
        const geojsonData = {json.dumps(geojson_data)};
        
        // Initialize map
        const map = L.map('map').setView([41.5, -93.5], 7);
        
        // Base layer definitions
        const baseLayers = {{
            'osm': L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
                attribution: '© OpenStreetMap contributors',
                maxZoom: 19
            }}),
            'topo': L.tileLayer('https://{{s}}.tile.opentopomap.org/{{z}}/{{x}}/{{y}}.png', {{
                attribution: '© OpenTopoMap contributors',
                maxZoom: 17
            }}),
            'satellite': L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{{z}}/{{y}}/{{x}}', {{
                attribution: '© ESRI',
                maxZoom: 19
            }}),
            'terrain': L.tileLayer('https://stamen-tiles.a.ssl.fastly.net/terrain/{{z}}/{{x}}/{{y}}.jpg', {{
                attribution: '© Stamen Design, © OpenStreetMap contributors',
                maxZoom: 18
            }})
        }};
        
        // Add default base layer
        let currentBaseLayer = baseLayers['osm'].addTo(map);
        
        // Style function for fields
        function fieldStyle(feature) {{
            return {{
                fillColor: '#4287f5',
                weight: 2,
                opacity: 1,
                color: '#1a5490',
                fillOpacity: 0.3
            }};
        }}
        
        // Popup function
        function onEachFeature(feature, layer) {{
            if (feature.properties) {{
                const props = feature.properties;
                const popupContent = `
                    <div style="font-family: sans-serif; font-size: 13px;">
                        <h4 style="margin: 0 0 8px 0; font-size: 14px;">${{props.field_id || 'N/A'}}</h4>
                        <table style="width: 100%; font-size: 12px;">
                            <tr><td><strong>State:</strong></td><td>${{props.state || 'N/A'}}</td></tr>
                            <tr><td><strong>County:</strong></td><td>${{props.county || 'N/A'}}</td></tr>
                            <tr><td><strong>Region:</strong></td><td>${{props.region || 'N/A'}}</td></tr>
                            <tr><td><strong>Crop (2023):</strong></td><td>${{props.crop_2023 || 'N/A'}}</td></tr>
                            <tr><td><strong>Area:</strong></td><td>${{props.area_acres ? props.area_acres.toFixed(1) + ' acres' : 'N/A'}}</td></tr>
                        </table>
                    </div>
                `;
                layer.bindPopup(popupContent);
            }}
        }}
        
        // Add GeoJSON layer
        const geojsonLayer = L.geoJSON(geojsonData, {{
            style: fieldStyle,
            onEachFeature: onEachFeature
        }}).addTo(map);
        
        // Fit bounds to all fields initially
        map.fitBounds(geojsonLayer.getBounds(), {{ padding: [50, 50] }});
        
        // Base map selector
        document.getElementById('basemap').addEventListener('change', function(e) {{
            map.removeLayer(currentBaseLayer);
            currentBaseLayer = baseLayers[e.target.value].addTo(map);
        }});
        
        // Field selector
        document.getElementById('field-select').addEventListener('change', function(e) {{
            const value = e.target.value;
            
            if (value === 'all') {{
                // Fit all fields
                map.fitBounds(geojsonLayer.getBounds(), {{ padding: [50, 50] }});
            }} else {{
                // Zoom to specific field
                const featureIndex = parseInt(value);
                const layers = [];
                geojsonLayer.eachLayer(layer => layers.push(layer));
                
                if (layers[featureIndex]) {{
                    const bounds = layers[featureIndex].getBounds();
                    map.fitBounds(bounds, {{ padding: [100, 100] }});
                    
                    // Open popup
                    setTimeout(() => {{
                        layers[featureIndex].openPopup();
                    }}, 500);
                }}
            }}
        }});
    </script>
</body>
</html>
"""

    # Write HTML file
    with open(output_path, "w") as f:
        f.write(html_content)

    print(f"✅ Generated interactive map: {output_path}")
    print(f"   - {len(features)} fields")
    print(f"   - {output_path.stat().st_size / 1024:.1f} KB")


def main():
    """Main entry point."""
    if len(sys.argv) != 3:
        print("Usage: python scripts/generate_test_map.py <geojson_file> <output_html>")
        sys.exit(1)

    geojson_path = Path(sys.argv[1])
    output_path = Path(sys.argv[2])

    if not geojson_path.exists():
        print(f"❌ Error: GeoJSON file not found: {geojson_path}")
        sys.exit(1)

    try:
        generate_map_html(geojson_path, output_path)
    except Exception as e:
        print(f"❌ Error generating map: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
