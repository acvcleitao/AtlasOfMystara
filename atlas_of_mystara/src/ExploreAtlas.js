import React, { useEffect } from 'react';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import './ExploreAtlas.css'; // Import your ExploreAtlas CSS file
import 'leaflet-search';
import 'leaflet-search/dist/leaflet-search.min.css';

const ExploreAtlas = () => {
  useEffect(() => {
    console.log("Map component is mounting...");

    // Image dimensions
    const imageWidth = 6425;
    const imageHeight = 3689;

    // Calculate aspect ratio
    const aspectRatio = imageWidth / imageHeight;

    // Set the map center
    const center = [0, 0]; // Adjust as needed

    // Calculate bounds based on aspect ratio
    const bounds = [
      [center[0] - 0.5 / aspectRatio, center[1] - 0.5], // Southwest
      [center[0] + 0.5 / aspectRatio, center[1] + 0.5], // Northeast
    ];

    // Create a Leaflet map
    const map = L.map('map').setView(center, 1);

    console.log("Map created successfully:", map);

    // Add the image layer to the map
    const imageLayer = L.imageOverlay(
      process.env.PUBLIC_URL + "/AtlasBaseMaps/outer-world-1985.png",
      bounds
    ).addTo(map);

    // Fit the map to the image bounds
    map.fitBounds(bounds);

    console.log("Image layer added successfully.");

    // Add search control with icon
    const searchControl = new L.Control.Search({
      position: 'topleft',
      layer: imageLayer,
      propertyName: 'searchText',
      marker: L.divIcon({ className: 'leaflet-search-icon' }),
    });

    searchControl.addTo(map);

  }, []);

  return (
    <div id="map" className="mapContainer"></div>
  );
};

export default ExploreAtlas;
