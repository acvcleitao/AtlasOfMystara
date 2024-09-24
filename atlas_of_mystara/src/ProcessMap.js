import React, { useState, useRef } from 'react';
import { Rnd } from 'react-rnd';
import './ProcessMap.css';
import { ChromePicker } from 'react-color';

const ProcessMap = ({ uploadedImage, mapName, mapAuthor, onConfirm, onBack }) => {
  const [hexGridWidth, setHexGridWidth] = useState(200);
  const [hexGridHeight, setHexGridHeight] = useState(200);
  const [hexGridX, setHexGridX] = useState(100);
  const [hexGridY, setHexGridY] = useState(100);
  const [hexMaskType, setHexMaskType] = useState('flat');
  const [selectedColor, setSelectedColor] = useState('#ffffff');
  const [step, setStep] = useState(1);
  const [columns, setColumns] = useState(5);
  const [lines, setLines] = useState(5);


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

  const handleConfirmUpload = async () => {
    try {
      // Prepare data to send to the backend
      const data = {
        mapName,
        mapAuthor,
        uploadedImage,
        selectedColor,
        hexMaskType,
        imageWidth: imageRef.current.width,
        imageHeight: imageRef.current.height
      };

      // Create a combined image of map with grid overlay
      const canvas = document.createElement('canvas');
      const ctx = canvas.getContext('2d');
      canvas.width = imageRef.current.width;
      canvas.height = imageRef.current.height;
      ctx.drawImage(imageRef.current, 0, 0, canvas.width, canvas.height);

      // Draw hex grid overlay
      const hexGridImage = new Image();
      hexGridImage.onload = () => {
        ctx.drawImage(hexGridImage, hexGridX, hexGridY, hexGridWidth, hexGridHeight);
        const combinedImage = canvas.toDataURL('image/png');

        // Call onConfirm function with necessary data
        onConfirm({ ...data, combinedImage });
      };
      hexGridImage.src = `/resources/hexmapMask_${hexMaskType.charAt(0).toUpperCase() + hexMaskType.slice(1)}_${columns}_${lines}.png`;

    } catch (error) {
      console.error('Error confirming upload:', error);
      alert('An error occurred during map upload');
    }
  };

  const proceedToColorPicker = () => {
    setStep(2);
  };

  return (
    <div className="process-map-container">
      <label className="map-title">
        {mapName}, by {mapAuthor}
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
              setHexGridWidth(parseInt(ref.style.width, 10));
              setHexGridHeight(parseInt(ref.style.height, 10));
              setHexGridX(position.x);
              setHexGridY(position.y);
            }}
          >
            <img
              src={`/resources/hexmapMask_${hexMaskType.charAt(0).toUpperCase() + hexMaskType.slice(1)}_${columns}_${lines}.png`}
              alt={`Hex Grid Mask ${hexMaskType} x:${columns} y:${lines} not found`}
              style={{ width: '100%', height: '100%', zIndex:9999 }}
            />
          </Rnd>
        </div>
      </div>
      <div className="map-upload-details-container">
        <div className="controls">
          <div className="instruction-text">
            {step === 1 
              ? 'Align the hex grid with the hexagons in your image. Place the first hexagon of the grid on the top left hexagon of your image.'
              : 'Click on a water section of your image to select the water color.'
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
              <div className="color-picker-wrapper">
                <ChromePicker
                  color={selectedColor}
                  onChangeComplete={(color) => setSelectedColor(color.hex)}
                  width="150px"
                />
                <div className="button-group">
                  <button className="button" onClick={handleConfirmUpload}>
                    Confirm Upload
                  </button>
                  <button className="button" onClick={onBack}>
                    Back
                  </button>
                </div>
              </div>
            </div>
          </>
        )}
        </div>
        {step === 1 && (
          <div className="dynamic-grid-controls">
            <label>
              Columns:
              <input
                type="number"
                min="1"
                value={columns}
                onChange={(e) => setColumns(Number(e.target.value))}
              />
            </label>
            <label>
              Lines:
              <input
                type="number"
                min="1"
                value={lines}
                onChange={(e) => setLines(Number(e.target.value))}
              />
            </label>
          </div>
        )}
      </div>
    </div>
  );
};

export default ProcessMap;
