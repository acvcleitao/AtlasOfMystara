function addChildrenForVisibleHexagons(map, hexagonsRes0) {
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
