import React, { useState, useEffect, useRef } from 'react';
import './ExploreAtlas.css';

const ExploreAtlas = () => {
  const [zoomLevel, setZoomLevel] = useState(1);
  const [selectedAuthor, setSelectedAuthor] = useState('');
  const [hexagons, setHexagons] = useState([]);
  const [isDragging, setIsDragging] = useState(false);
  const [dragStart, setDragStart] = useState({ x: 0, y: 0 });
  const mapContainerRef = useRef(null);
  const mapContainerPosRef = useRef({ x: 0, y: 0 });
  const [viewportCenter, setViewportCenter] = useState({ x: 0, y: 0 });
  const [lastFetchedCenter, setLastFetchedCenter] = useState({ x: 0, y: 0 });
  const hexSize = 50;
  var centerX = -16;
  var centerY = -16;

  const fetchHexagons = async (center) => {
    try {
      const col = Math.round(center.x / (3 / 2 * hexSize));
      const row = Math.round(center.y / (hexSize * Math.sqrt(3)));

      const numRows = 32;
      const numCols = 32;

      const topLeft = [
        col - Math.floor(numCols / 2),
        row - Math.floor(numRows / 2)
      ];
      const bottomRight = [
        col + Math.ceil(numCols / 2),
        row + Math.ceil(numRows / 2)
      ];
      // Calculate centerX and centerY as the midpoint between topLeft and bottomRight
      centerX = (topLeft[0] + bottomRight[0]) / 2;
      centerY = (topLeft[1] + bottomRight[1]) / 2;

      const response = await fetch(`http://127.0.0.1:5000/getHexagons?zoomLevel=${zoomLevel}&author=${selectedAuthor}&topLeft=${topLeft.join(',')}&bottomRight=${bottomRight.join(',')}`);
      if (!response.ok) {
        throw new Error('Failed to fetch hexagons');
      }
      const data = await response.json();
      if (data.hexagons) {
        for (let i = 0; i < data.hexagons.length; i++) {
          // console.log('New Image Received:', data.hexagons[i].imageURL);
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
        setLastFetchedCenter(center); // Update the last fetched center
        // console.log('Got Hexagons!', data.hexagons);
        HexGrid(data.hexagons, centerX, centerY)
      }
    } catch (error) {
      console.error('Error fetching hexagons:', error);
    }
  };

  useEffect(() => {
    fetchHexagons(viewportCenter);
  }, [zoomLevel, selectedAuthor]);

  useEffect(() => {
    const handleMouseMove = (event) => {
      if (isDragging) {
        const deltaX = event.clientX - dragStart.x;
        const deltaY = event.clientY - dragStart.y;

        mapContainerPosRef.current.x += deltaX;
        mapContainerPosRef.current.y += deltaY;

        mapContainerRef.current.style.transform = `translate(${mapContainerPosRef.current.x}px, ${mapContainerPosRef.current.y}px)`;

        setDragStart({ x: event.clientX, y: event.clientY });
        setViewportCenter((prev) => ({
          x: prev.x - deltaX,
          y: prev.y - deltaY
        }));
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

  useEffect(() => {
    const distance = Math.sqrt(
      Math.pow(viewportCenter.x - lastFetchedCenter.x, 2) +
      Math.pow(viewportCenter.y - lastFetchedCenter.y, 2)
    );

    if (distance > 16 * hexSize) {
      fetchHexagons(viewportCenter);
      console.log("fetching hexagons...");
    }
  }, [viewportCenter]);

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
        <HexGrid hexagonsData={hexagons} centerX={centerX} centerY={centerY} />
      </div>
    </div>
  );
};

const HexGrid = ({ hexagonsData, centerX, centerY }) => {
  console.log("Creating hex grid arround center:(" + centerX + "," + centerY + ")");
  // console.log('HexGrid - hexagonsData:', hexagonsData);
  const hexSize = 50; // Adjust hexagon size as needed
  const numRows = 32; // Number of rows
  const numCols = 64; // Number of columns

  const horizSpacing = 3 / 2 * hexSize;
  const vertSpacing = hexSize * Math.sqrt(3);

  let hexagons = [];

  if (hexagonsData && hexagonsData.length > 0) {
    const hexagonsMap = {};
    hexagonsData.forEach(({ type, coordinates, imageURL }) => {
      coordinates.forEach(([x, y]) => {
        hexagonsMap[`${x}-${y}`] = { type, imageURL };
      });
    });

    for (let row = centerY - Math.floor(numRows / 2); row <= centerY + Math.ceil(numRows / 2); row++) {
      for (let col = centerX - Math.floor(numCols / 2); col <= centerX + Math.ceil(numCols / 2); col++) {
        const x = (col - (centerX - Math.floor(numCols / 2))) * horizSpacing; // Calculate x position
        const y = (row - (centerY - Math.floor(numRows / 2))) * vertSpacing + (col % 2) * (vertSpacing / 2); // Calculate y position
        const key = `${row}-${col}`; // Unique key for each hexagon
        const hexagonData = hexagonsMap[`${col}-${row}`]; // Note the reversal of x and y here
        hexagons.push(
          <Hexagon key={key} id={key} x={x} y={y} size={hexSize} hexagonData={hexagonData} />
        );
      }
    }
  } else {
    for (let row = centerY - Math.floor(numRows / 2); row <= centerY + Math.ceil(numRows / 2); row++) {
      for (let col = centerX - Math.floor(numCols / 2); col <= centerX + Math.ceil(numCols / 2); col++) {
        const x = (col - (centerX - Math.floor(numCols / 2))) * horizSpacing; // Calculate x position
        const y = (row - (centerY - Math.floor(numRows / 2))) * vertSpacing + (col % 2) * (vertSpacing / 2); // Calculate y position
        const key = `${row}-${col}`; // Unique key for each hexagon
        hexagons.push(
          <Hexagon key={key} id={key} x={x} y={y} size={hexSize} />
        );
      }
    }
  }

  const svgWidth = horizSpacing * numCols;
  const svgHeight = vertSpacing * numRows;

  return (
    <svg width={svgWidth} height={svgHeight}>
      {hexagons}
    </svg>
  );
};

const Hexagon = ({ id, x, y, size, hexagonData }) => {
  const points = [
    [x + size * Math.cos(0), y + size * Math.sin(0)],
    [x + size * Math.cos(Math.PI / 3), y + size * Math.sin(Math.PI / 3)],
    [x + size * Math.cos(2 * Math.PI / 3), y + size * Math.sin(2 * Math.PI / 3)],
    [x + size * Math.cos(Math.PI), y + size * Math.sin(Math.PI)],
    [x + size * Math.cos(4 * Math.PI / 3), y + size * Math.sin(4 * Math.PI / 3)],
    [x + size * Math.cos(5 * Math.PI / 3), y + size * Math.sin(5 * Math.PI / 3)],
  ].map((point) => point.join(',')).join(' ');

  const handleClick = () => {
    console.log('Hexagon clicked:', id);
  };

  return (
    <g>
      <polygon points={points} fill="#555" stroke="#000" strokeWidth="2" onClick={handleClick} />
      {hexagonData && hexagonData.imageURL && (
        <image href={hexagonData.imageURL} x={x - size} y={y - size} width={size * 2} height={size * 2} />
      )}
    </g>
  );
};

export default ExploreAtlas;
