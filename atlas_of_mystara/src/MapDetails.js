// MapDetails.js
import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import './MapDetails.css';

const MapDetails = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [selectedMap, setSelectedMap] = useState(null);

  useEffect(() => {
    const fetchMapDetails = async () => {
      try {
        const response = await fetch(`http://127.0.0.1:5000/getMapDetails/${id}`);
        if (response.ok) {
          const data = await response.json();
          setSelectedMap(data.map);
        } else {
          console.error('Failed to fetch map details');
        }
      } catch (error) {
        console.error('Error fetching map details:', error);
      }
    };

    fetchMapDetails();
  }, [id]);

  if (!selectedMap) {
    return <div>Loading...</div>;
  }

  const handleApprove = (mapId) => {
    // Perform any additional logic (e.g., API call, state update) for approval
    console.log('Approved');
    // Redirect user to the newMaps window
    navigate('/new_maps'); // Update to use navigate
  };

  const handleDiscard = (mapId) => {
    // Perform any additional logic (e.g., API call, state update) for discarding
    console.log('Discarded');
    // Redirect user to the newMaps window
    navigate('/new_maps'); // Update to use navigate
  };

  return (
    <div>
      <h2>{selectedMap.title}</h2>
      <img src={selectedMap.image_url} alt={selectedMap.title} />
      <div className="overlay-buttons">
        <button onClick={() => handleApprove(selectedMap._id)}>Approve</button>
        <button onClick={() => handleDiscard(selectedMap._id)}>Discard</button>
      </div>
    </div>
  );
};

export default MapDetails;
