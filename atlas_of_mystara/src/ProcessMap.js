// ProcessMap.js
import React, { useState } from 'react';
import { Rnd } from 'react-rnd';
import './ProcessMap.css';

const ProcessMap = ({ uploadedImage, mapName, onConfirm, onBack }) => {
  const [hexGridWidth, setHexGridWidth] = useState(200);
  const [hexGridHeight, setHexGridHeight] = useState(200);
  const [hexGridX, setHexGridX] = useState(100);
  const [hexGridY, setHexGridY] = useState(100);
  const [hexMaskType, setHexMaskType] = useState('pointy');

  const handleHexMaskChange = (e) => {
    setHexMaskType(e.target.value);
  };

  const handleConfirmUpload = () => {
    let floatParameter;
    if (hexMaskType === 'flat') {
      floatParameter = hexGridWidth / 20;
    } else if (hexMaskType === 'pointy') {
      floatParameter = hexGridHeight / 20;
    } else {
      // Default to pointy top if no type is selected
      floatParameter = hexGridHeight / 20;
    }

    // Call onConfirm function with necessary data
    onConfirm(mapName, uploadedImage, floatParameter);
  };

  return (
    <div className="process-map-container">
      <label className="map-title">
        Map Name: {mapName}
      </label>
      <div className="upload-image-container">
        <div style={{ position: 'relative', width: '100%', height: '100%' }}>
          <img
            src={uploadedImage}
            alt="Process Map"
            className="uploaded-image"
            style={{ width: '100%', height: '100%', objectFit: 'contain', borderRadius: '15px' }}
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
              src={`/resources/hexmapMask${hexMaskType.charAt(0).toUpperCase() + hexMaskType.slice(1)}.png`}
              alt={`Hex Grid Mask ${hexMaskType}`}
              style={{ width: '100%', height: '100%' }}
            />
          </Rnd>
        </div>
      </div>
      <div className="map-details-container">
        <div className="controls">
          <div className="instruction-text">
            Align the hex grid with the hexagons in your image. Place the first hexagon of the grid on the top left hexagon of your image.
          </div>
          <label className="hex-mask-label">
            Hex Mask Type:
            <select value={hexMaskType} onChange={handleHexMaskChange}>
              <option value="pointy">Pointy Top</option>
              <option value="flat">Flat Top</option>
            </select>
          </label>
        </div>

        <button className="button" onClick={handleConfirmUpload}>
          Confirm Upload
        </button>
        <button className="button" onClick={onBack}>
          Back
        </button>
      </div>
    </div>
  );
};

export default ProcessMap;
