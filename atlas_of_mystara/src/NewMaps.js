// NewMaps.js
import React, { useState, useEffect } from 'react';

const NewMaps = () => {
  const [newMaps, setNewMaps] = useState([]);

  useEffect(() => {
    // Fetch new maps from the backend when the component mounts
    fetchNewMaps();
  }, []);

  const fetchNewMaps = async () => {
    try {
      const response = await fetch('http://127.0.0.1:5000/getNewMaps');
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
      <h1>New Maps</h1>
      <div className="maps-grid">
        {newMaps.map((map) => (
          <div key={map._id} className="map-item">
            <img src={map.imageURL} alt={map.title} />
            <p>{map.title}</p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default NewMaps;
