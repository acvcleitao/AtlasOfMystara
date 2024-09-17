import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom'; 
import './EditMap.css';
import { Rnd } from "react-rnd";


const EditMap = () => {
  const { mapId } = useParams(); 
  const [selectedHex, setSelectedHex] = useState(new Set()); 
  const [hexType, setHexType] = useState('');
  const [hexagonTypes, setHexagonTypes] = useState([]);
  const [selectedHexType, setSelectedHexType] = useState('');
  const [hexagons, setHexagons] = useState([]); 
  const [hexImages, setHexImages] = useState({}); 
  const [author, setAuthor] = useState('');
  const [title, setTitle] = useState('');
  const [baseImage, setBaseImage] = useState(''); // State for the base image
  const [baseImageWidth, setBaseImageWidth] = useState(600); // Initial width
  const [baseImageHeight, setBaseImageHeight] = useState(400); // Initial height
  const [baseImageX, setBaseImageX] = useState(0); // Initial X position
  const [baseImageY, setBaseImageY] = useState(0); // Initial Y position
  const [isBaseImageVisible, setIsBaseImageVisible] = useState(false); // Toggle visibility
  const [loading, setLoading] = useState(true); 
  const [error, setError] = useState(null);
  

  useEffect(() => {
    const fetchHexagonTypes = async () => {
      try {
        const response = await fetch(`http://127.0.0.1:5000/getAuthorHexes/${author}`);
        if (!response.ok) {
          throw new Error('Failed to fetch hexagon types');
        }
        const data = await response.json();
        setHexagonTypes(data.hexagonTypes);
        console.log("Got Types", data.hexagonTypes);
      } catch (error) {
        console.error('Error fetching hexagon types:', error);
      }
    };
    if (author) {
      fetchHexagonTypes();
    }
  }, [author]);

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

        // Set the base image from the map document
        setBaseImage(data.baseImage);
        

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

  const handleHexClick = (hexId, event) => {
    const isCtrlPressed = event.ctrlKey;
    if (isCtrlPressed) {
      setSelectedHex(prevSelectedHex => {
        const newSelectedHex = new Set(prevSelectedHex);
        if (newSelectedHex.has(hexId)) {
          newSelectedHex.delete(hexId); 
        } else {
          newSelectedHex.add(hexId); 
        }
        return newSelectedHex;
      });
    } else {
      setSelectedHex(prevSelectedHex => {
        const newSelectedHex = new Set();
        if (!prevSelectedHex.has(hexId)) {
          newSelectedHex.add(hexId); 
        }
        return newSelectedHex;
      });
      // Update hexType to the type of the clicked hexagon
      const hex = hexagons.find(hex => `${author}_${hex.coordinate[0]}_${hex.coordinate[1]}` === hexId);
      if (hex) {
        setHexType(hex.type.split('.')[0]);
      } else {
        setHexType('');
      }
    }
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
      body: JSON.stringify({ hexId: Array.from(selectedHex), hexType: hexType }),
    }).then(response => response.json())
      .then(data => {
        console.log(data);
      })
      .catch(error => {
        console.error('Error updating hex type:', error);
      });
  };

  const toggleBaseImageVisibility = () => {
    setIsBaseImageVisible(!isBaseImageVisible);
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
        selectedHex={selectedHex} 
      />

      {selectedHex.size > 0 && (
        <div className="edit-tools">
          <label htmlFor="hex-type">Hex Type: </label>
          <select id="hex-type" value={hexType} onChange={handleHexTypeChange}>
            <option key={hexType} value={hexType}>{hexType}</option>
            {hexagonTypes.map((type) => (
              type !== hexType ? (
                <option key={type} value={type}>{type}</option>
              ) : null
            ))}
          </select>
          <button onClick={saveHexType}>Save</button>
        </div>
      )}
      <button className='base-image-toggle-button' onClick={toggleBaseImageVisibility}>
        {isBaseImageVisible ? 'Hide Base Image' : 'Show Base Image'}
      </button>
      {isBaseImageVisible && (
        <Rnd
          className="rnd-outline"
          size={{ width: baseImageWidth, height: baseImageHeight }}
          position={{ x: baseImageX, y: baseImageY }}
          onDragStop={(e, d) => {
            setBaseImageX(d.x);
            setBaseImageY(d.y);
          }}
          onResizeStop={(e, direction, ref, delta, position) => {
            setBaseImageWidth(parseInt(ref.style.width, 10));
            setBaseImageHeight(parseInt(ref.style.height, 10));
            setBaseImageX(position.x);
            setBaseImageY(position.y);
          }}
        >
          <img
            className='base-image-overlay'
            src={baseImage ? `data:image/png;base64,${baseImage}` : 'https://archive.org/download/placeholder-image/placeholder-image.jpg'}
            alt="Base Image"
            style={{ width: '100%', height: '100%', opacity: 0.9 }}
          />
        </Rnd>
      )}
    
    </div>
  );
};

const HexGrid = ({ hexagonsData, centerX, centerY, zoomLevel, author, onHexClick, hexImages, selectedHex }) => {
  const hexSize = 50;

  const maxX = Math.max(...hexagonsData.map(h => h.coordinate[0]));
  const maxY = Math.max(...hexagonsData.map(h => h.coordinate[1]));

  const numRows = maxY + 1;
  const numCols = maxX + 1;

  const horizSpacing = 3 / 2 * hexSize;
  const vertSpacing = hexSize * Math.sqrt(3);

  let hexagons = [];
  let selectedHexagons = [];

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
        const hexId = `${author}_${col}_${row}`;
        const isSelected = selectedHex.has(hexId);

        const hexagon = (
          <Hexagon
            key={key}
            id={hexId}
            x={x}
            y={y}
            size={hexSize}
            hexagonData={hexagonData}
            onHexClick={onHexClick}
            coordinate={hexagonData ? hexagonData.coordinate : null}
            isSelected={isSelected}
          />
        );

        if (isSelected) {
          selectedHexagons.push(hexagon); // Capture selected hexagons
        } else {
          hexagons.push(hexagon);
        }
      }
    }
  }

  const svgWidth = horizSpacing * numCols;
  const svgHeight = vertSpacing * numRows;

  return (
    <svg width={svgWidth} height={svgHeight} className='hexagonalGrid'>
      <g className="hexagons-layer">
        {hexagons}
      </g>
      <g className="selected-hexagon-layer">
        {selectedHexagons} {/* Render selected hexagons above all others */}
      </g>
    </svg>
  );
};

const Hexagon = ({ id, x, y, size, hexagonData, onHexClick, coordinate, isSelected }) => {
  const points = [
    [x + size * Math.cos(0), y + size * Math.sin(0)],
    [x + size * Math.cos(Math.PI / 3), y + size * Math.sin(Math.PI / 3)],
    [x + size * Math.cos(2 * Math.PI / 3), y + size * Math.sin(2 * Math.PI / 3)],
    [x + size * Math.cos(Math.PI), y + size * Math.sin(Math.PI)],
    [x + size * Math.cos(4 * Math.PI / 3), y + size * Math.sin(4 * Math.PI / 3)],
    [x + size * Math.cos(5 * Math.PI / 3), y + size * Math.sin(5 * Math.PI / 3)],
  ].map((point) => point.join(',')).join(' ');

  const handleClick = (event) => {
    onHexClick(id, event); // Pass the event to handleHexClick
  };

  return (
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
      {/* Draw the border on top */}
      {isSelected && (
        <polygon
          points={points}
          fill="transparent"
          stroke="red"
          strokeWidth="10"
          pointerEvents="none" // Prevent click events on this layer
        />
      )}
      <polygon
        points={points}
        fill="transparent"
        stroke="#000"
        strokeWidth="5"
        onClick={handleClick}
      />
    </g>
  );
};

export default EditMap;
