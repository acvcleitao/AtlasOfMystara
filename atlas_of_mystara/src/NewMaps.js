// NewMaps.js
import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import './NewMaps.css';

const NewMaps = () => {
  const [newMaps, setNewMaps] = useState([]);

  useEffect(() => {
    fetchNewMaps();
    document.body.classList.add('newmaps');
    return () => {
      document.body.classList.remove('newmaps');
    };
  }, []);

  const fetchNewMaps = async () => {
    try {
      const response = await fetch('http://127.0.0.1:5000/getNewMapsWithURL');
      if (response.ok) {
        const data = await response.json();
        console.log('Fetched Maps:', data.maps);
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
          <Link to={map._id ? `/map/${map._id}` : '#'} key={map._id} className="map-item">
            <img src={map.image_url} alt={map.title} className="map-image" />
            <p className="map-title">{map.title}</p>
          </Link>
        ))}
      </div>
    </div>
  );
};

export default NewMaps;
