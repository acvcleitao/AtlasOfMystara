// ProcessMap.js
import React, { useState, useRef } from 'react';
import { Rnd } from 'react-rnd';
import './ProcessMap.css';
import { ChromePicker } from 'react-color';

const ProcessMap = ({ uploadedImage, mapName, onConfirm, onBack }) => {
  const [hexGridWidth, setHexGridWidth] = useState(200);
  const [hexGridHeight, setHexGridHeight] = useState(200);
  const [hexGridX, setHexGridX] = useState(100);
  const [hexGridY, setHexGridY] = useState(100);
  const [hexMaskType, setHexMaskType] = useState('pointy');
  const [selectedColor, setSelectedColor] = useState('#ffffff');
  const [step, setStep] = useState(1);

  const imageRef = useRef(null);

  const handleHexMaskChange = (e) => {
    setHexMaskType(e.target.value);
  };

  const handleImageClick = (e) => {
    const canvas = document.createElement('canvas');
    const ctx = canvas.getContext('2d');
    canvas.width = imageRef.current.width;
    canvas.height = imageRef.current.height;
    ctx.drawImage(imageRef.current, 0, 0, canvas.width, canvas.height);
    const x = e.nativeEvent.offsetX;
    const y = e.nativeEvent.offsetY;
    const pixel = ctx.getImageData(x, y, 1, 1).data;
    const color = `rgb(${pixel[0]}, ${pixel[1]}, ${pixel[2]})`;
    setSelectedColor(color);
  };

  const handleConfirmUpload = () => {
    let hexSize;
    if (hexMaskType === 'flat') {
      hexSize = hexGridWidth / 20;
    } else if (hexMaskType === 'pointy') {
      hexSize = hexGridHeight / 20;
    } else {
      // Default to pointy top if no type is selected
      hexSize = hexGridHeight / 20;
    }

    // Call onConfirm function with necessary data
    onConfirm(mapName, uploadedImage, hexSize, selectedColor);
  };

  const proceedToColorPicker = () => {
    setStep(2);
  };

  return (
    <div className="process-map-container">
      <label className="map-title">
        Map Name: {mapName}
      </label>
      <div className="upload-image-container" onClick={step === 2 ? handleImageClick : null}>
        <div style={{ position: 'relative', width: '100%', height: '100%' }}>
          <img
            src={uploadedImage}
            alt="Process Map"
            className="uploaded-image"
            style={{ width: '100%', height: '100%', objectFit: 'contain', borderRadius: '15px' }}
            ref={imageRef}
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
            {step === 1 
              ? 'Align the hex grid with the hexagons in your image. Place the first hexagon of the grid on the top left hexagon of your image.'
              : 'Click on the ocean area in your image to select the sea/ocean color.'
            }
          </div>
          {step === 1 && (
            <>
              <label className="hex-mask-label">
                Hex Mask Type:
                <select value={hexMaskType} onChange={handleHexMaskChange}>
                  <option value="pointy">Pointy Top</option>
                  <option value="flat">Flat Top</option>
                </select>
              </label>
              <button className="button" onClick={proceedToColorPicker}>
                Next: Select Ocean Color
              </button>
            </>
          )}
          {step === 2 && (
            <>
              <div className="color-picker-container">
                <div className="selected-color" style={{ backgroundColor: selectedColor }}></div>
                <ChromePicker color={selectedColor} onChangeComplete={(color) => setSelectedColor(color.hex)} />
              </div>
              <button className="button" onClick={handleConfirmUpload}>
                Confirm Upload
              </button>
              <button className="button" onClick={onBack}>
                Back
              </button>
            </>
          )}
        </div>
      </div>
    </div>
  );
};

export default ProcessMap;
