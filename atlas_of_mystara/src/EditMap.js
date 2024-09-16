import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom'; // Import useParams to get map_id from URL
import ExploreAtlas from './ExploreAtlas';
import './EditMap.css';

const EditAtlas = () => {
  const { mapId } = useParams(); // Get map_id from URL parameters
  const [selectedHex, setSelectedHex] = useState(null);
  const [hexType, setHexType] = useState('');
  const [hexagonTypes, setHexagonTypes] = useState([]);
  const [hexagons, setHexagons] = useState([]); // State to store hexagons of the specific map
  const [author, setAuthor] = useState('');
  const [title, setTitle] = useState('');
  const [loading, setLoading] = useState(true); // For loading state
  const [error, setError] = useState(null); // For error handling

  // Fetch hexagon types when component mounts
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

  // Fetch hexagons for the specific mapId
  useEffect(() => {
    const fetchMapHexagons = async () => {
      try {
        const response = await fetch(`http://127.0.0.1:5000/getMap/${mapId}`);
        if (!response.ok) {
          throw new Error('Failed to fetch hexagons for map');
        }
        
        const data = await response.json();
        console.log('Got a map! ', data)

        // Extract and set author, title, and hexagons
        setAuthor(data.author);
        setTitle(data.title);

        const hexagonLayer = data.layers.find(layer => layer.type === 'hexagon_layer');
        if (hexagonLayer) {
          setHexagons(hexagonLayer.hexagons);
        }
        setLoading(false);
        
      } catch (error) {
        console.error('Error fetching hexagons:', error);
      }
    };

    if (mapId) {
      fetchMapHexagons();
    }
  }, [mapId]);

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
      <ExploreAtlas onHexClick={handleHexClick} hexagons={hexagons} /> {/* Pass hexagons data */}
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
