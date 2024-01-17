// ExploreAtlas.js
import React, { useRef, useEffect, useState } from 'react';
import styles from './ExploreAtlas.css'; // Import the CSS module

const ExploreAtlas = () => {
  const mapContainerRef = useRef(null);
  const [zoomLevel, setZoomLevel] = useState(1);

  useEffect(() => {
    const handleWheel = (event) => {
      // Implement zooming on mouse wheel
      if (event.deltaY > 0) {
        setZoomLevel((prevZoom) => Math.max(1, prevZoom - 0.1));
      } else {
        setZoomLevel((prevZoom) => prevZoom + 0.1);
      }
    };

    const handleDrag = (event) => {
      // Implement panning on mouse drag
      const { movementX, movementY } = event;
      mapContainerRef.current.scrollLeft += movementX;
      mapContainerRef.current.scrollTop += movementY;
    };

    const mapContainer = mapContainerRef.current;
    mapContainer.addEventListener('wheel', handleWheel);
    mapContainer.addEventListener('mousedown', () => {
      mapContainer.addEventListener('mousemove', handleDrag);
    });
    mapContainer.addEventListener('mouseup', () => {
      mapContainer.removeEventListener('mousemove', handleDrag);
    });

    return () => {
      mapContainer.removeEventListener('wheel', handleWheel);
      mapContainer.removeEventListener('mousemove', handleDrag);
    };
  }, []);

  return (
    <div className={styles.mapContainer} ref={mapContainerRef}>
      {/* Your very large image goes here */}
      <img
        src="path/to/your/very/large/image.jpg"
        alt="Map"
        style={{ transform: `scale(${zoomLevel})` }}
      />

      {/* Zoom in/out buttons */}
      <div className={styles.zoomButtons}>
        <button onClick={() => setZoomLevel((prevZoom) => prevZoom + 0.1)}>Zoom In</button>
        <button onClick={() => setZoomLevel((prevZoom) => Math.max(1, prevZoom - 0.1))}>
          Zoom Out
        </button>
      </div>

      {/* SearchBar */}
      <div className={styles.searchBar}>
        <input type="text" placeholder="Search location..." />
        <button>Search</button>
      </div>
    </div>
  );
};

export default ExploreAtlas;
