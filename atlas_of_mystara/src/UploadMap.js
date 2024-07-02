// UploadMap.js
import React, { useState, useRef } from 'react';
import './UploadMap.css';
import ProcessMap from './ProcessMap';

const UploadMap = ({ onUpload }) => {
  const [uploadedImage, setUploadedImage] = useState(null);
  const [mapName, setMapName] = useState('');
  const [showPreview, setShowPreview] = useState(false);
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

  const handleProceedToPreview = () => {
    setShowPreview(true);
  };

  const handleBack = () => {
    setShowPreview(false);
  };

  const handleUploadMap = async (mapName, uploadedImage, hexagonSize) => {
    try {
      // Create a FormData object to send the image, map title, and float parameter
      const formData = new FormData();
      formData.append('title', mapName);
      formData.append('image', uploadedImage);
      formData.append('hexagonSize', hexagonSize);

      // Make a request to the backend to upload the map
      const response = await fetch('http://127.0.0.1:5000/uploadMap', {
        method: 'POST',
        body: formData,
      });

      if (response.ok) {
        const data = await response.json();
        alert(data.message);  // Display the upload message

        // Reset state
        setUploadedImage(null);
        setMapName('');
        setShowPreview(false);

      } else {
        const errorData = await response.json();
        alert(`Error: ${errorData.message}`);
      }
    } catch (error) {
      console.error('Upload map error:', error);
      alert('An error occurred during map upload');
    }
  };

  const handleImageClick = () => {
    if (fileInputRef.current) {
      fileInputRef.current.click();
    }
  };

  return (
    <div className="upload-map-container">
      {showPreview ? (
        <ProcessMap
          uploadedImage={uploadedImage}
          mapName={mapName}
          onConfirm={handleUploadMap}
          onBack={handleBack}
        />
      ) : (
        <>
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
              className="proceed-button"
              onClick={handleProceedToPreview}
              disabled={!uploadedImage || mapName.trim() === ''}
            >
              Proceed to Preview
            </button>
          </div>
        </>
      )}
    </div>
  );
};

export default UploadMap;
