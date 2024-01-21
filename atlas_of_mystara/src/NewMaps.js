// NewMapsPage.js
import React, { useState, useEffect } from 'react';
import './NewMaps.css';

const NewMaps = () => {
  const [newMaps, setNewMaps] = useState([]);

  useEffect(() => {
    // Fetch new maps from the backend when the component mounts
    fetchNewMaps();
  }, []);

  const fetchNewMaps = async () => {
    try {
      const response = await fetch('http://127.0.0.1:5000/getNewMapsWithURL');
      if (response.ok) {
        const data = await response.json();
        setNewMaps(data.maps);
      } else {
        console.error('Failed to fetch new maps');
      }
    } catch (error) {
      console.error('Error fetching new maps:', error);
    }
  };

  return (
    <div>
      <h1>New Maps Page</h1>
      <div className="maps-grid">
        {newMaps.map((map) => (
          <div key={map._id} className="map-item">
            <img src={map.image_url} alt={map.title} className="map-image" />
            <p className="map-title">{map.title}</p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default NewMaps;
