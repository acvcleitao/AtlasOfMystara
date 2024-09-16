import React, { useState, useEffect, useRef } from 'react';
import './ExploreAtlas.css';

const ExploreAtlas = ({ hexagons: propHexagons, onHexClick }) => {
  const [zoomLevel, setZoomLevel] = useState(1);
  const [selectedAuthor, setSelectedAuthor] = useState('');
  const [hexagons, setHexagons] = useState([]);
  const [isDragging, setIsDragging] = useState(false);
  const [dragStart, setDragStart] = useState({ x: 0, y: 0 });
  const [authors, setAuthors] = useState([]);
  const mapContainerRef = useRef(null);
  const mapContainerPosRef = useRef({ x: 0, y: 0 });
  const [viewportCenter, setViewportCenter] = useState({ x: 0, y: 0 });
  const [lastFetchedCenter, setLastFetchedCenter] = useState({ x: 0, y: 0 });
  const hexSize = 50;
  var centerX = -16;
  var centerY = -16;

  useEffect(() => {
    // Fetch authors if needed
    const fetchAuthors = async () => {
      try {
        const response = await fetch('http://127.0.0.1:5000/getAuthors');
        if (!response.ok) {
          throw new Error('Failed to fetch authors');
        }
        const data = await response.json();
        setAuthors(data.authors);
      } catch (error) {
        console.error('Error fetching authors:', error);
      }
    };

    fetchAuthors();
  }, []);

  useEffect(() => {
    if (propHexagons) {
      setHexagons(propHexagons);
      fetchHexagons(viewportCenter);
    } else {
      fetchHexagons(viewportCenter);
    }
  }, [zoomLevel, selectedAuthor, propHexagons]);

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

      centerX = (topLeft[0] + bottomRight[0]) / 2;
      centerY = (topLeft[1] + bottomRight[1]) / 2;
      if (propHexagons) return; // Skip fetching if hexagons are provided by prop

      const response = await fetch(`http://127.0.0.1:5000/getHexagons?zoomLevel=${zoomLevel}&author=${selectedAuthor}&topLeft=${topLeft.join(',')}&bottomRight=${bottomRight.join(',')}`);
      if (!response.ok) {
        throw new Error('Failed to fetch hexagons');
      }
      const data = await response.json();
      if (data.hexagons) {
        for (let i = 0; i < data.hexagons.length; i++) {
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
        setLastFetchedCenter(center);
      }
    } catch (error) {
      console.error('Error fetching hexagons:', error);
    }
  };

  const handleMouseDown = (event) => {
    setIsDragging(true);
    setDragStart({ x: event.clientX, y: event.clientY });
  };

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

  useEffect(() => {
    document.addEventListener('mousemove', handleMouseMove);
    document.addEventListener('mouseup', handleMouseUp);

    return () => {
      document.removeEventListener('mousemove', handleMouseMove);
      document.removeEventListener('mouseup', handleMouseUp);
    };
  }, [isDragging, dragStart]);

  const handleZoomIn = () => {
    setZoomLevel((prevZoomLevel) => prevZoomLevel + 1);
  };

  const handleZoomOut = () => {
    setZoomLevel((prevZoomLevel) => Math.max(1, prevZoomLevel - 1));
  };

  const handleAuthorChange = (event) => {
    setSelectedAuthor(event.target.value);
  };

  return (
    <div className="explore-atlas-container">
      <div className="button-container">
        <label htmlFor="author-select" className="author-label">
          Select Author:{' '}
        </label>
        <select id="author-select" onChange={handleAuthorChange}>
          <option value="">All Authors</option>
          {authors.map((author) => (
            <option key={author} value={author}>{author}</option>
          ))}
        </select>
        <div className="zoom-buttons">
          <button className="zoom-button" onClick={handleZoomIn}>
            +
          </button>
          <button className="zoom-button" onClick={handleZoomOut}>
            -
          </button>
        </div>
      </div>
      <div
        className="map-container"
        ref={mapContainerRef}
        onMouseDown={handleMouseDown}
        style={{ cursor: isDragging ? 'grabbing' : 'grab' }}
      >
        {!propHexagons && (
          <HexGrid hexagonsData={hexagons} centerX={centerX} centerY={centerY} zoomLevel={zoomLevel} author={selectedAuthor} onHexClick={onHexClick} 
          />
        )}
        {propHexagons && (<HexGridProp hexagonsData={hexagons} centerX={centerX} centerY={centerY} onHexClick={onHexClick} 
          />)}
      </div>
    </div>
  );
};

const HexGrid = ({ hexagonsData, centerX, centerY, zoomLevel, author, onHexClick }) => {
  const hexSize = 50;
  const numRows = 32;
  const numCols = 64;

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
        const x = (col - (centerX - Math.floor(numCols / 2))) * horizSpacing;
        const y = (row - (centerY - Math.floor(numRows / 2))) * vertSpacing + (col % 2) * (vertSpacing / 2);
        const key = `${row}-${col}`;
        const hexagonData = hexagonsMap[`${col}-${row}`];
        hexagons.push(
          <Hexagon key={key} id={`${author}_${zoomLevel}_${col}_${row}`} x={x} y={y} size={hexSize} hexagonData={hexagonData} onHexClick={onHexClick} />
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

const Hexagon = ({ id, x, y, size, hexagonData, onHexClick }) => {
  const points = [
    [x + size * Math.cos(0), y + size * Math.sin(0)],
    [x + size * Math.cos(Math.PI / 3), y + size * Math.sin(Math.PI / 3)],
    [x + size * Math.cos(2 * Math.PI / 3), y + size * Math.sin(2 * Math.PI / 3)],
    [x + size * Math.cos(Math.PI), y + size * Math.sin(Math.PI)],
    [x + size * Math.cos(4 * Math.PI / 3), y + size * Math.sin(4 * Math.PI / 3)],
    [x + size * Math.cos(5 * Math.PI / 3), y + size * Math.sin(5 * Math.PI / 3)],
  ].map((point) => point.join(',')).join(' ');

  const handleClick = () => {
    onHexClick(id);
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

const HexGridProp = ({hexagonsData, centerX, centerY, onHexClick}) => {
  console.log("Got data: ", hexagonsData)

  const hexSize = 50;
  const numRows = 32;
  const numCols = 64;

  const horizSpacing = 3 / 2 * hexSize;
  const vertSpacing = hexSize * Math.sqrt(3);

  let hexagons = [];

  if (hexagonsData && hexagonsData.length > 0) {
    const hexagonsMap = {};
    
    hexagonsData.forEach(({ type, coordinate }) => {
      const [x, y] = coordinate;
      hexagonsMap[`${x}-${y}`] = { type };
    });

    for (let row = centerY - Math.floor(numRows / 2); row <= centerY + Math.ceil(numRows / 2); row++) {
      for (let col = centerX - Math.floor(numCols / 2); col <= centerX + Math.ceil(numCols / 2); col++) {
        const x = (col - (centerX - Math.floor(numCols / 2))) * horizSpacing;
        const y = (row - (centerY - Math.floor(numRows / 2))) * vertSpacing + (col % 2) * (vertSpacing / 2);
        const key = `${row}-${col}`;
        const hexagonData = hexagonsMap[`${col}-${row}`];
        hexagons.push(
          <HexagonProp key={key} x={x} y={y} size={hexSize} hexagonData={hexagonData} onHexClick={onHexClick} />
        );
      }
    }
  }

  return (
    <svg className="hex-grid" width="100%" height="100%">
      {hexagons}
    </svg>
  );
};

const HexagonProp = ({ x, y, size, hexagonData, onHexClick }) => {
  const points = [
    [x + size * Math.cos(0), y + size * Math.sin(0)],
    [x + size * Math.cos(Math.PI / 3), y + size * Math.sin(Math.PI / 3)],
    [x + size * Math.cos(2 * Math.PI / 3), y + size * Math.sin(2 * Math.PI / 3)],
    [x + size * Math.cos(Math.PI), y + size * Math.sin(Math.PI)],
    [x + size * Math.cos(4 * Math.PI / 3), y + size * Math.sin(4 * Math.PI / 3)],
    [x + size * Math.cos(5 * Math.PI / 3), y + size * Math.sin(5 * Math.PI / 3)],
  ].map((point) => point.join(',')).join(' ');

  const handleClick = () => {
    onHexClick();
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
