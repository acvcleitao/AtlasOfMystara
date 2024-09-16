import React, { useState, useRef } from 'react';
import './UploadMap.css';
import ProcessMap from './ProcessMap';
import EditAtlas from './EditMap'; // Import EditAtlas component
import { useNavigate } from 'react-router-dom';
 
const UploadMap = ({ onUpload }) => {
  const [uploadedImage, setUploadedImage] = useState(null);
  const [mapName, setMapName] = useState('');
  const [mapAuthor, setMapAuthor] = useState('');
  const [showPreview, setShowPreview] = useState(false);
  const [showEditAtlas, setShowEditAtlas] = useState(false); // New state to control EditAtlas display
  const fileInputRef = useRef();
  const navigate = useNavigate();

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
      const response = await fetch('http://127.0.0.1:5000/uploadMap', {
        method: 'POST',
        body: JSON.stringify(data),
        headers: {
          'Content-Type': 'application/json'
        }
      });

      if (response.ok) {
        const data = await response.json();
        const mapId = data.map_id; // Access the map_id from the response
        console.log('Map ID:', mapId);
        alert(data.message);  // Display the upload message
        
        // Navigate to editAtlas component and pass mapId
        navigate(`/edit_map/${mapId}`);

        // Reset state
        setUploadedImage(null);
        setMapName('');
        setShowPreview(false);
        setShowEditAtlas(true);  // Show EditAtlas after successful upload

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
      {showEditAtlas ? ( // Show EditAtlas if the upload is successful
        <EditAtlas />
      ) : showPreview ? (
        <ProcessMap
          uploadedImage={uploadedImage}
          mapName={mapName}
          mapAuthor={mapAuthor}
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
