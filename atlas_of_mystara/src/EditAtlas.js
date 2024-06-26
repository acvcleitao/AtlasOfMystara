import React, { useState, useEffect } from 'react';
import ExploreAtlas from './ExploreAtlas';
import './EditAtlas.css';

const EditAtlas = () => {
  const [selectedHex, setSelectedHex] = useState(null);
  const [hexType, setHexType] = useState('');
  const [hexagonTypes, setHexagonTypes] = useState([]);

  useEffect(() => {
    const fetchHexagonTypes = async () => {
      try {
        const response = await fetch('http://127.0.0.1:5000/getHexagonTypes');
        if (!response.ok) {
          throw new Error('Failed to fetch hexagon types');
        }
        const data = await response.json();
        setHexagonTypes(data.hexagonTypes);
      } catch (error) {
        console.error('Error fetching hexagon types:', error);
      }
    };

    fetchHexagonTypes();
  }, []);

  const handleHexClick = (hexId) => {
    setSelectedHex(hexId);
  };

  const handleHexTypeChange = (event) => {
    setHexType(event.target.value);
  };

  const saveHexType = () => {
    console.log(`Hex ${selectedHex} updated to type: ${hexType}`);
    fetch(`http://127.0.0.1:5000/updateHexType`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ hexId: selectedHex, hexType: hexType })
    }).then(response => response.json())
      .then(data => {
        console.log(data);
      })
      .catch(error => {
        console.error('Error updating hex type:', error);
      });
  };

  return (
    <div className="edit-atlas-container">
      <ExploreAtlas onHexClick={handleHexClick} />
      {selectedHex && (
        <div className="edit-tools">
          <label htmlFor="hex-type">Hex Type: </label>
          <select id="hex-type" value={hexType} onChange={handleHexTypeChange}>
            {hexagonTypes.map((authorGroup) => (
              <optgroup key={authorGroup.author} label={authorGroup.author}>
                {authorGroup.hexTypes.map((type) => (
                  <option key={type} value={type}>{type}</option>
                ))}
              </optgroup>
            ))}
          </select>
          <button onClick={saveHexType}>Save</button>
        </div>
      )}
    </div>
  );
};

export default EditAtlas;
