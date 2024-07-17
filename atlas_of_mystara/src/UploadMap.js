import React, { useState, useRef } from 'react';
import './UploadMap.css';
import ProcessMap from './ProcessMap';

const UploadMap = ({ onUpload }) => {
  const [uploadedImage, setUploadedImage] = useState(null);
  const [mapName, setMapName] = useState('');
  const [mapAuthor, setMapAuthor] = useState('');
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

  const handleMapAuthorChange = (e) => {
    setMapAuthor(e.target.value);
  };

  const handleProceedToPreview = () => {
    setShowPreview(true);
  };

  const handleBack = () => {
    setShowPreview(false);
  };

  const handleUploadMap = async (data) => {
    try {
      // Make a request to the backend to upload the map
      const response = await fetch('http://127.0.0.1:5000/uploadMap', {
        method: 'POST',
        body: JSON.stringify(data),
        headers: {
          'Content-Type': 'application/json'
        }
      });

      if (response.ok) {
        const responseData = await response.json();
        alert(responseData.message);  // Display the upload message

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
          mapAuthor={mapAuthor}
          onConfirm={handleUploadMap} // Pass the handleUploadMap function
          onBack={handleBack} // Pass the handleBack function
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
            <label>
              Map Author:
              <input
                type="text"
                value={mapAuthor}
                onChange={handleMapAuthorChange}
                placeholder="Enter name of author"
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
