import React, { useState, useEffect, useRef } from 'react';
import './ExploreAtlas.css'; // Import your ExploreAtlas CSS file

const ExploreAtlas = () => {
  const [zoomLevel, setZoomLevel] = useState(1);
  const [selectedAuthor, setSelectedAuthor] = useState('');
  const [hexagons, setHexagons] = useState([]);
  const [isDragging, setIsDragging] = useState(false);
  const [dragStart, setDragStart] = useState({ x: 0, y: 0 });
  const mapContainerRef = useRef(null);
  const mapContainerPosRef = useRef({ x: 0, y: 0 });

  const fetchHexagons = async () => {
    try {
      const coordinates = { topLeft: [0, 0], bottomRight: [256, 256] };
      const response = await fetch(`http://127.0.0.1:5000/getHexagons?zoomLevel=${zoomLevel}&author=${selectedAuthor}&topLeft=${coordinates.topLeft.join(',')}&bottomRight=${coordinates.bottomRight.join(',')}`);
      if (!response.ok) {
        throw new Error('Failed to fetch hexagons');
      }
      const data = await response.json();
      if (data.hexagons) {
        for (let i = 0; i < data.hexagons.length; i++) {
          console.log('New Image Received:', data.hexagons[i].imageURL);
          const imageResponse = await fetch(`http://127.0.0.1:5000/static/hexagons/${data.hexagons[i].imageURL}`);
          if (imageResponse.ok) {
            const blob = await imageResponse.blob();
            const imageUrl = URL.createObjectURL(blob);
            data.hexagons[i].imageURL = imageUrl;
          } else {
            console.error('Failed to fetch image:', imageResponse.status);
          }
        }
        setHexagons(data.hexagons);
        console.log('Got Hexagons!', data.hexagons);
      }
    } catch (error) {
      console.error('Error fetching hexagons:', error);
    }
  };
  
  useEffect(() => {
    fetchHexagons();
  }, [zoomLevel, selectedAuthor, isDragging]);
  

  useEffect(() => {
    const handleMouseMove = (event) => {
      if (isDragging) {
        const deltaX = event.clientX - dragStart.x;
        const deltaY = event.clientY - dragStart.y;

        mapContainerPosRef.current.x += deltaX;
        mapContainerPosRef.current.y += deltaY;

        mapContainerRef.current.style.transform = `translate(${mapContainerPosRef.current.x}px, ${mapContainerPosRef.current.y}px)`;

        setDragStart({ x: event.clientX, y: event.clientY });
      }
    };

    const handleMouseUp = () => {
      setIsDragging(false);
    };

    document.addEventListener('mousemove', handleMouseMove);
    document.addEventListener('mouseup', handleMouseUp);

    return () => {
      document.removeEventListener('mousemove', handleMouseMove);
      document.removeEventListener('mouseup', handleMouseUp);
    };
  }, [isDragging, dragStart]);

  const handleMouseDown = (event) => {
    setIsDragging(true);
    setDragStart({ x: event.clientX, y: event.clientY });
  };

  const handleZoomIn = () => {
    setZoomLevel((prevZoomLevel) => prevZoomLevel + 1);
  };

  const handleZoomOut = () => {
    setZoomLevel((prevZoomLevel) => Math.max(1, prevZoomLevel - 1));
  };

  const handleAuthorChange = (event) => {
    setSelectedAuthor(event.target.value);
  };

  const handleSearch = (searchText) => {
    console.log('Search for:', searchText);
  };

  return (
    <div className="explore-atlas-container">
      <div className="button-container">
        <label htmlFor="author-select" className="author-label">
          Select Author:{' '}
        </label>
        <select id="author-select" onChange={handleAuthorChange}>
          <option value="">All Authors</option>
          <option value="Thorf">Thorf</option>
          {/* Add more authors as needed */}
        </select>
        <div className="zoom-buttons">
          <button className="zoom-button" onClick={handleZoomIn}>
            +
          </button>
          <button className="zoom-button" onClick={handleZoomOut}>
            -
          </button>
        </div>
        <input
          type="text"
          placeholder="Search..."
          className="search-bar"
          onChange={(e) => handleSearch(e.target.value)}
        />
      </div>
      <div
        className="map-container"
        ref={mapContainerRef}
        onMouseDown={handleMouseDown}
        style={{ cursor: isDragging ? 'grabbing' : 'grab' }}
      >
        {/* SVG grid of hexagons */}
        <HexGrid hexagonsData={hexagons} />
      </div>
    </div>
  );
};

const HexGrid = ({ hexagonsData }) => {
  console.log('HexGrid - hexagonsData:', hexagonsData);
  const hexSize = 50; // Adjust hexagon size as needed
  const numRows = 20; // Number of rows
  const numCols = 30; // Number of columns

  const horizSpacing = 3 / 2 * hexSize;
  const vertSpacing = hexSize * Math.sqrt(3);

  let hexagons = [];

  if (hexagonsData && hexagonsData.length > 0) {
    // Map fetched hexagons to their coordinates
    const hexagonsMap = {};
    hexagonsData.forEach(({ type, coordinates, imageURL }) => {
      coordinates.forEach(([x, y]) => {
        hexagonsMap[`${x}-${y}`] = { type, imageURL };
      });
    });

    for (let row = 0; row < numRows; row++) {
      for (let col = 0; col < numCols; col++) {
        const x = col * horizSpacing;
        const y = row * vertSpacing + (col % 2) * (vertSpacing / 2);
        const key = `${row}-${col}`; // Unique key for each hexagon
        const hexagonData = hexagonsMap[key];
        hexagons.push(
          <Hexagon key={key} id={key} x={x} y={y} size={hexSize} hexagonData={hexagonData} />
        );
      }
    }
    console.log(hexagonsData)
  } else {
    // Render placeholder hexagons if no hexagon data is available
    for (let row = 0; row < numRows; row++) {
      for (let col = 0; col < numCols; col++) {
        const x = col * horizSpacing;
        const y = row * vertSpacing + (col % 2) * (vertSpacing / 2);
        const key = `${row}-${col}`; // Unique key for each hexagon
        hexagons.push(
          <Hexagon key={key} id={key} x={x} y={y} size={hexSize} />
        );
      }
    }
  }

  return (
    <svg
      width={horizSpacing * (numCols - 1) + hexSize}
      height={vertSpacing * (numRows - 1) + hexSize}
    >
      {hexagons}
    </svg>
  );
};

const Hexagon = ({ id, x, y, size, hexagonData }) => {
  const points = [
    [x + size * Math.cos(0), y + size *Math.sin(0)],
    [x + size * Math.cos(Math.PI / 3), y + size * Math.sin(Math.PI / 3)],
    [x + size * Math.cos(2 * Math.PI / 3), y + size * Math.sin(2 * Math.PI / 3)],
    [x + size * Math.cos(Math.PI), y + size * Math.sin(Math.PI)],
    [x + size * Math.cos(4 * Math.PI / 3), y + size * Math.sin(4 * Math.PI / 3)],
    [x + size * Math.cos(5 * Math.PI / 3), y + size * Math.sin(5 * Math.PI / 3)],
  ].map((point) => point.join(',')).join(' ');

  const handleClick = () => {
    // Handle click event for the hexagon
    console.log('Hexagon clicked:', id);
  };

  return (
    <g>
      <polygon points={points} fill="#555" stroke="#000" strokeWidth="2" onClick={handleClick} />
      {hexagonData && hexagonData.imageURL && (
        <image href={hexagonData.imageURL} x={x - size} y={y - size} width={size*2} height={2*size} />
      )}
    </g>
  );
};

export default ExploreAtlas;