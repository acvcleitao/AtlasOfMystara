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

  const handleUploadMap = async () => {
    try {
      // Check if mapName is not empty and uploadedImage is not null
      if (mapName.trim() !== '' && uploadedImage) {
        // Create a FormData object to send the image and map title
        const formData = new FormData();
        formData.append('title', mapName);
        formData.append('image', uploadedImage);

        // Make a request to your backend to upload the map
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
  
          // You can update other state or perform additional actions if needed
  
        } else {
          const errorData = await response.json();
          alert(`Error: ${errorData.message}`);
        }
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
