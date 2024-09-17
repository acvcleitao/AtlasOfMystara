import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom'; 
import './EditMap.css';

const EditMap = () => {
  const { mapId } = useParams(); 
  const [selectedHex, setSelectedHex] = useState(null);
  const [hexType, setHexType] = useState('');
  const [hexagonTypes, setHexagonTypes] = useState([]);
  const [hexagons, setHexagons] = useState([]); 
  const [hexImages, setHexImages] = useState({}); 
  const [author, setAuthor] = useState('');
  const [title, setTitle] = useState('');
  const [loading, setLoading] = useState(true); 
  const [error, setError] = useState(null);

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

  useEffect(() => {
    const fetchMapHexagons = async () => {
      try {
        const response = await fetch(`http://127.0.0.1:5000/getMap/${mapId}`);
        if (!response.ok) {
          throw new Error('Failed to fetch hexagons for map');
        }
        const data = await response.json();
        setAuthor(data.author);
        setTitle(data.title);

        const hexagonLayer = data.layers.find(layer => layer.type === 'hexagon_layer');
        if (hexagonLayer) {
          const hexagons = hexagonLayer.hexagons;
          setHexagons(hexagons);
        
          const uniqueTypes = [...new Set(hexagons.map(hex => hex.type))];
        
          try {
            const response = await fetch('http://127.0.0.1:5000/getImage', {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json',
              },
              body: JSON.stringify({
                hexTypes: uniqueTypes,
                author: data.author,
              }),
            });
        
            const imagesDict = await response.json();
            setHexImages(imagesDict);
          } catch (error) {
            console.error('Error fetching base64 images:', error);
            setError('Failed to load hexagon images');
          }
        
          setLoading(false);
        }
        setLoading(false);
        
      } catch (error) {
        console.error('Error fetching hexagons or images:', error);
        setError('Failed to load map');
        setLoading(false);
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
    fetch(`http://127.0.0.1:5000/updateHexType`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ hexId: selectedHex, hexType: hexType }),
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
      <HexGrid 
        hexagonsData={hexagons} 
        centerX={0} 
        centerY={0} 
        zoomLevel={1} 
        author={author} 
        onHexClick={handleHexClick} 
        hexImages={hexImages} 
      />
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

const HexGrid = ({ hexagonsData, centerX, centerY, zoomLevel, author, onHexClick, hexImages }) => {
  const hexSize = 50;

  // Find the bottom-right hexagon to determine the grid size
  const maxX = Math.max(...hexagonsData.map(h => h.coordinate[0]));
  const maxY = Math.max(...hexagonsData.map(h => h.coordinate[1]));

  const numRows = maxY + 1; // since coordinates are zero-indexed
  const numCols = maxX + 1;

  const horizSpacing = 3 / 2 * hexSize;
  const vertSpacing = hexSize * Math.sqrt(3);

  let hexagons = [];

  if (hexagonsData && hexagonsData.length > 0) {
    const hexagonsMap = {};
    hexagonsData.forEach(({ type, coordinate: [x, y] }) => {
      hexagonsMap[`${x}-${y}`] = { type, coordinate: [x, y], imageBase64: hexImages[type] };
    });

    for (let row = centerY; row < numRows + centerY; row++) {
      for (let col = centerX; col < numCols + centerX; col++) {
        const x = (col - centerX) * horizSpacing;
        const y = (row - centerY) * vertSpacing + (col % 2) * (vertSpacing / 2);
        const key = `${row}-${col}`;
        const hexagonData = hexagonsMap[`${col}-${row}`];

        hexagons.push(
          <Hexagon
            key={key}
            id={`${author}_${zoomLevel}_${col}_${row}`}
            x={x}
            y={y}
            size={hexSize}
            hexagonData={hexagonData}
            onHexClick={onHexClick}
            coordinate={hexagonData ? hexagonData.coordinate : null} // Pass the coordinate here
          />
        );
      }
    }
  }

  const svgWidth = horizSpacing * numCols;
  const svgHeight = vertSpacing * numRows

  return (
    <svg width={svgWidth} height={svgHeight} className='hexagonalGrid'>
      {hexagons}
    </svg>
  );
};



const Hexagon = ({ id, x, y, size, hexagonData, onHexClick, coordinate }) => {
  const points = [
    [x + size * Math.cos(0), y + size * Math.sin(0)],
    [x + size * Math.cos(Math.PI / 3), y + size * Math.sin(Math.PI / 3)],
    [x + size * Math.cos(2 * Math.PI / 3), y + size * Math.sin(2 * Math.PI / 3)],
    [x + size * Math.cos(Math.PI), y + size * Math.sin(Math.PI)],
    [x + size * Math.cos(4 * Math.PI / 3), y + size * Math.sin(4 * Math.PI / 3)],
    [x + size * Math.cos(5 * Math.PI / 3), y + size * Math.sin(5 * Math.PI / 3)],
  ].map((point) => point.join(',')).join(' ');

  const handleClick = () => {
    if (hexagonData) {
      console.log("Hexagon coordinate:", coordinate);
      console.log("Hexagon type:", hexagonData.type);
    }
    onHexClick(id);
  };

  return (
    
  <svg className='hexagonalGrid'>
    <g className='hexagonProp'
      data-coordinate={coordinate ? `${coordinate}` : 'N/A'}
      data-type={hexagonData ? hexagonData.type : 'N/A'}
    >
      {hexagonData && hexagonData.imageBase64 && (
        <image
          className='hexagonProp'
          href={`data:image/png;base64,${hexagonData.imageBase64}`}
          x={x - size} 
          y={y - size}
        />
      )}
      <polygon points={points} fill="transparent" stroke="#000" strokeWidth="5" onClick={handleClick} />
    </g>
  </svg>
  );
};

export default EditMap;
