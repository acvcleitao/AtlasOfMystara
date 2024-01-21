// ExploreAtlas.js
import React, { useEffect } from 'react';
import L from 'leaflet';
import './ExploreAtlas.css';  // Create a new CSS file for ExploreAtlas styles

const ExploreAtlas = () => {
  useEffect(() => {
    console.log("Map component is mounting...");

    const map = L.map('map').setView([0, 0], 1);

    console.log("Map created successfully:", map);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);

    console.log("Tile layer added successfully.");
  }, []);

  return (
    <div id="map" style={{ height: '100vh' }}></div>
  );
};

export default ExploreAtlas;
