// ProcessMap.js
import React, { useState } from 'react';
import { Rnd } from 'react-rnd';
import './ProcessMap.css';

const ProcessMap = ({ uploadedImage, mapName, onConfirm, onBack }) => {
  const [width, setWidth] = useState(400);
  const [height, setHeight] = useState(400);
  const [hexGridWidth, setHexGridWidth] = useState(200);
  const [hexGridHeight, setHexGridHeight] = useState(200);
  const [hexGridX, setHexGridX] = useState(100);
  const [hexGridY, setHexGridY] = useState(100);

  return (
    <div className="process-map-container">
      <div style={{ position: 'relative' }}>
        <img
          src={uploadedImage}
          alt="Process Map"
          className="process-image"
          style={{ width: `${width}px`, height: `${height}px` }}
        />
        <Rnd
          className="rnd-outline"
          size={{ width: hexGridWidth, height: hexGridHeight }}
          position={{ x: hexGridX, y: hexGridY }}
          onDragStop={(e, d) => {
            setHexGridX(d.x);
            setHexGridY(d.y);
          }}
          onResizeStop={(e, direction, ref, delta, position) => {
            setHexGridWidth(ref.style.width);
            setHexGridHeight(ref.style.height);
            setHexGridX(position.x);
            setHexGridY(position.y);
          }}
        >
          <img
            src="/resources/hexmapMaskFlat.png"
            alt="Hex Grid Mask"
            style={{ width: '100%', height: '100%' }}
          />
        </Rnd>
      </div>
      <h2>{mapName}</h2>
      <button className="confirm-button" onClick={onConfirm}>
        Confirm Upload
      </button>
      <button className="back-button" onClick={onBack}>
        Back
      </button>
    </div>
  );
};

export default ProcessMap;
