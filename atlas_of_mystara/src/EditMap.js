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
  const [imageWidth, setImageWidth] = useState(null);
  const [isOverlayOpen, setIsOverlayOpen] = useState(false);
  const [selectedHexCoastline, setSelectedHexCoastline] = useState('')
  const [selectedHexBaseImage, setSelectedHexBaseImage] = useState('')
  const [tempCoastline, setTempCoastline] = useState(selectedHexCoastline);
  

  useEffect(() => {
    const fetchHexagonTypes = async () => {
      try {
        const response = await fetch(`http://127.0.0.1:5000/getAuthorHexes/${author}`);
        if (!response.ok) {
          throw new Error('Failed to fetch hexagon types');
        }
        const data = await response.json();
        setHexagonTypes(data.hexagonTypes);
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
          console.log(hexagons)
        
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
    const hex = hexagons.find(hex => `${author}_${hex.coordinate[0]}_${hex.coordinate[1]}` === hexId);
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
      if (hex) {
        setHexType(hex.type.split('.')[0]);
      } else {
        setHexType('');
      }
    }
    
    setSelectedHexCoastline(hex.coastline);
    setSelectedHexBaseImage(hexImages[hex.type]);
    setTempCoastline(hex.coastline);
  };

  const handleHexTypeChange = (event) => {
    setHexType(event.target.value);
  };

  const saveHexType = async () => {
    // Check if the hexType has a corresponding image in the hexImages map
    if (!hexImages[hexType]) {
      // Fetch the image if not already in hexImages
      try {
        const response = await fetch('http://127.0.0.1:5000/getImage', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            hexTypes: [hexType],
            author: author,
          }),
        });
        const imagesDict = await response.json();
        // Update hexImages with the new image
        setHexImages(prevImages => ({
          ...prevImages,
          ...imagesDict,
        }));
      } catch (error) {
        console.error('Error fetching image:', error);
        return; // Exit function if fetching fails
      }
    }
  
    // Create new hexagons with updated type and image
    const updatedHexagons = hexagons.map(hex => {
      if (selectedHex.has(`${author}_${hex.coordinate[0]}_${hex.coordinate[1]}`)) {
        return {
          ...hex,
          type: hexType,
          imageBase64: hexImages[hexType] || hex.imageBase64, // Use new image or keep old
        };
      }
      return hex;
    });
  
    // Update hexagons list with the new hexagons
    setHexagons(updatedHexagons);
  };

  const toggleBaseImageVisibility = () => {
    setIsBaseImageVisible(!isBaseImageVisible);
  };

  const openOverlay = () => {
    setIsOverlayOpen(true);
  };

  const closeOverlay = () => {
    setIsOverlayOpen(false);
  };

  const uploadMapToDatabase = async () => {
    try {
        console.log("Updating map")
        console.log(hexagons);
        const response = await fetch(`http://127.0.0.1:5000/updateMap/${mapId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                hexagons: hexagons
            }),
        });

        if (!response.ok) {
            throw new Error('Failed to upload map');
        }

        const result = await response.json();
        console.log('Map updated successfully:');
        // Show a pop-up on success and redirect to the base route "/"
        window.alert("Map uploaded successfully!");
        window.location.href = "/";

    } catch (error) {
        console.error('Error uploading map:', error);
    }
  };

  const downloadCoastline = () => {
    if (selectedHex.size > 0) {
      const hexId = Array.from(selectedHex)[0]; // Only one hex selected at a time
      const selectedHexagon = hexagons.find(hex => `${author}_${hex.coordinate[0]}_${hex.coordinate[1]}` === hexId);

      if (selectedHexagon && selectedHexagon.coastline) {
        const base64Image = selectedHexagon.coastline;
        const link = document.createElement('a');
        link.href = `data:image/png;base64,${base64Image}`;
        link.download = `coastline_hex_${selectedHexagon.coordinate[0]}_${selectedHexagon.coordinate[1]}.png`;
        link.click();
      } else {
        console.log("No coastline image found for the selected hexagon.");
      }
    }
  };

  const swapCoastline = () => {
    // Trigger the hidden file input
    document.getElementById('fileInput').click();
  };
  
  const handleFileChange = (event) => {
    const file = event.target.files[0];
  
    if (file) {
      const reader = new FileReader();
  
      reader.onloadend = () => {
        const originalImage = new Image();
        originalImage.src = reader.result;
  
        originalImage.onload = () => {
          // Create an off-screen canvas
          const canvas = document.createElement('canvas');
          const ctx = canvas.getContext('2d');
  
          // Set desired width and height for the new image
          const desiredWidth = 64;
          const desiredHeight = 56;
  
          // Resize the canvas
          canvas.width = desiredWidth;
          canvas.height = desiredHeight;
  
          // Draw the original image onto the canvas, resizing it in the process
          ctx.drawImage(originalImage, 0, 0, desiredWidth, desiredHeight);
  
          // Get the resized image as a base64 string
          const base64Image = canvas.toDataURL('image/png').split(',')[1];
  
          // Store the new coastline in temporary state
          setTempCoastline(base64Image);
        };
      };
  
      reader.readAsDataURL(file); // Convert the image file to a base64 string
    }
  };

  // Function to confirm and update the selected hexagon's coastline
  const confirmCoastlineChange = () => {
    if (selectedHex.size > 0) {
      const hexId = Array.from(selectedHex)[0]; // Only one hex selected at a time
      const selectedHexagon = hexagons.find(hex => `${author}_${hex.coordinate[0]}_${hex.coordinate[1]}` === hexId);

      if (selectedHexagon) {
        // Update the selected hexagon's coastline
        selectedHexagon.coastline = tempCoastline;

        // Update the UI or state accordingly
        setSelectedHexCoastline(tempCoastline); // Update the coastline image in the UI
      }
    }
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
      
      <div className="edit-tools">
        <div className="dropdown-save-container">
          <label htmlFor="hex-type">Hex Type: </label>
          <select id="hex-type" value={hexType} onChange={handleHexTypeChange}>
            <option key={hexType} value={hexType}>{hexType}</option>
            {hexagonTypes.map((type) => (
              type !== hexType ? (
                <option key={type} value={type}>{type}</option>
              ) : null
            ))}
          </select>
          <button className="upload-map-button" onClick={saveHexType}>Save</button>
        </div>
  
        <button className="base-image-toggle-button" onClick={toggleBaseImageVisibility}>
          {isBaseImageVisible ? 'Hide Base Image' : 'Show Base Image'}
        </button>
        <button className="upload-map-button" onClick={openOverlay}>Edit Coastline</button>

        <button className="upload-map-button" onClick={uploadMapToDatabase}>Upload Map</button>
      </div> 
      <div>
        {isOverlayOpen && (
          <div className="overlay">
            <div className="overlay-content">
              <button className="close-button" onClick={closeOverlay}>
                X
              </button>

              <div className="hexagon-info">
                <h3>Selected Hexagon: {hexType}</h3>
                <h4>Base Image</h4>
                <img 
                  src={`data:image/png;base64,${selectedHexBaseImage}`} 
                  alt="Hexagon" 
                />
              </div>

              <div className="coastline-info">
                <h4>Coastline Image</h4>
                {/* Properly format the coastline base64 URL */}
                <img 
                  src={`data:image/png;base64,${tempCoastline}`} 
                  alt="Coastline" 
                />
              </div>
              <div className="image-stack">
                <h4>Hexagon Image</h4>
                <img
                  className="base-image"
                  src={`data:image/png;base64,${selectedHexBaseImage}`}
                  alt="Hexagon Base"
                />
                <img
                  className="coastline-image"
                  src={`data:image/png;base64,${tempCoastline}`}
                  alt="Coastline"
                />
              </div>
              <div className="overlay-button-container">
                <button onClick={downloadCoastline}>Download Coastline</button>
                <button onClick={swapCoastline}>Swap Coastline</button>
                <input 
                  type="file" 
                  id="fileInput" 
                  style={{ display: "none" }} 
                  accept="image/*" 
                  onChange={handleFileChange} 
                />
                <button onClick={confirmCoastlineChange}>Confirm Coastline Change</button>
                <button onClick={closeOverlay}>Cancel</button>
              </div>
            </div>
          </div>
        )}
      </div>

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
            className="base-image-overlay"
            src={baseImage ? `data:image/png;base64,${baseImage}` : 'https://archive.org/download/placeholder-image/placeholder-image.jpg'}
            alt="Base Image"
            style={{ width: '100%', height: '100%', opacity: 0.5 }}
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
    hexagonsData.forEach(({ type, coordinate: [x, y], coastline }) => {
      hexagonsMap[`${x}-${y}`] = { type, coordinate: [x, y], imageBase64: hexImages[type], coastline };
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
      {hexagonData && hexagonData.coastline && (
        <image
          className='hexagonProp'
          href={`data:image/png;base64,${hexagonData.coastline}`}
          x={x - size}
          y={y - size}
        />
      )}
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
