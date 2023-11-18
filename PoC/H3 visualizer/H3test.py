import h3
import folium

# Create a Folium map
m = folium.Map(location=[0, 0], zoom_start=2)

# Get all cells at resolution 0
hexagonsRes0 = h3.get_res0_indexes()

# Add res0 hexagons to the map
for hexagonRes0 in hexagonsRes0:
    hex_coords_res0 = h3.h3_to_geo_boundary(hexagonRes0, geo_json=False)
    flattened_coords_res0 = [(lat, lng) for lat, lng in hex_coords_res0]
    folium.Polygon(locations=flattened_coords_res0, color='blue', fill=True, fill_color='blue', fill_opacity=0.4).add_to(m)

# Define JavaScript code to add hexagons for zoom level >= 5
js_code_add_hexagons = """
function addChildrenForVisibleHexagons() {
    console.log("Executing addChildrenForVisibleHexagons");

    var bounds = map.getBounds();
    var zoom = map.getZoom();
    
    // Log bounds and zoom level
    console.log("Bounds:", bounds);
    console.log("Zoom Level:", zoom);

    // Iterate over each res0 hexagon and check if it's visible
    for (var i = 0; i < hexagonsRes0.length; i++) {
        var hexagon = hexagonsRes0[i];
        var hexagonCoords = h3.h3ToGeoBoundary(hexagon, false);

        // Log hexagon and its coordinates
        console.log("Hexagon:", hexagon);
        console.log("Hexagon Coordinates:", hexagonCoords);

        // Check if at least one point of the hexagon is within the current bounds
        var isVisible = hexagonCoords.some(function(coord) {
            return bounds.contains([coord[0], coord[1]]);
        });

        if (isVisible && zoom >= 5) {
            console.log("Adding children for hexagon: " + hexagon);
            addChildren(hexagon);
        }
    }
}

function addChildren(hexagon) {
    console.log("Adding children for hexagon: " + hexagon);
    // Implement the logic to add children hexagons here
}

map.on('moveend', addChildrenForVisibleHexagons);
map.on('zoomend', addChildrenForVisibleHexagons);

// Initial call to add hexagons based on the initial map state
addChildrenForVisibleHexagons();
"""

# Embed JavaScript code directly in the HTML
m.get_root().script.add_child(folium.Element(js_code_add_hexagons))

# Display the map in Jupyter Notebook
m
