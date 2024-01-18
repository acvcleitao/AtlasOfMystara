// UploadMap.js
import React, { useState, useRef } from 'react';
import './UploadMap.css';

const UploadMap = ({ onUpload }) => {
  const [uploadedImage, setUploadedImage] = useState(null);
  const [mapName, setMapName] = useState('');
  const fileInputRef = useRef();

  const handleImageUpload = (e) => {
    const file = e.target.files[0];
    const reader = new FileReader();

    reader.onload = (event) => {
      setUploadedImage(event.target.result);
    };

    reader.readAsDataURL(file);
  };

  const handleMapNameChange = (e) => {
    setMapName(e.target.value);
  };

  const handleUploadMap = () => {
    // Check if mapName is not empty and uploadedImage is not null
    if (mapName.trim() !== '' && uploadedImage) {
      // Send the map data to the server
      // You can make a fetch request to your server here
      // For now, we'll just call the onUpload callback
      onUpload({ mapName, imageData: uploadedImage });

      // Reset state
      setUploadedImage(null);
      setMapName('');
    }
  };

  const handleImageClick = () => {
    if (fileInputRef.current) {
      fileInputRef.current.click();
    }
  };

  return (
    <div className="upload-map-container">
      <div className="upload-image-container" onClick={handleImageClick}>
        {uploadedImage ? (
          <img src={uploadedImage} alt="Uploaded Map" className="uploaded-image" />
        ) : (
          <label className="upload-label">Click to Upload Map</label>
        )}
        <input
          type="file"
          id="fileInput"
          accept="image/*"
          onChange={handleImageUpload}
          ref={fileInputRef}
          style={{ display: 'none' }}
        />
      </div>
      <div className="map-details-container">
        <label>
          Map Name:
          <input
            type="text"
            value={mapName}
            onChange={handleMapNameChange}
            placeholder="Enter map name"
            disabled={!uploadedImage}
          />
        </label>
        <button
          className="upload-button"
          onClick={handleUploadMap}
          disabled={!uploadedImage || mapName.trim() === ''}
        >
          Upload Map
        </button>
      </div>
    </div>
  );
};

export default UploadMap;
