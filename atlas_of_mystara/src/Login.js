// Import necessary dependencies
import React, { useState, useEffect } from 'react';
import { useUser } from './UserContext';
import './Login.css';

function Login({ onClosePopup }) {
  // Destructure the necessary functions from useUser
  const { login, setNewMapsCount } = useUser();
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const handleLogin = async () => {
    try {
      // Make a request to your backend to authenticate the user
      const response = await fetch('http://127.0.0.1:5000/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, password }),
      });

      if (response.ok) {
        const data = await response.json();
        alert(data.message);  // Display the login message

        // Update the newMaps count in the UserContext
        if (typeof data.newMaps === 'number') {
          setNewMapsCount(data.newMaps);
        }

        login();
        onClosePopup();
      } else {
        const errorData = await response.json();
        alert(`Error: ${errorData.message}`);
      }
    } catch (error) {
      console.error('Login error:', error);
      alert('An error occurred during login');
    }
  };

  // Close the popup when clicking outside the popup
  const handleClosePopup = (e) => {
    if (e.target.classList.contains('popup-container')) {
      onClosePopup();
    }
  };

  // Close the popup when clicking on the "X" button
  const handleCloseButtonClick = () => {
    onClosePopup();
  };

  // Attach a click event listener to the document for the entire component
  useEffect(() => {
    document.addEventListener('click', handleClosePopup);

    // Clean up the event listener on component unmount
    return () => {
      document.removeEventListener('click', handleClosePopup);
    };
  }, [onClosePopup]);

  return (
    <div className="popup-container">
      <div className="login-popup">
        <span className="close" onClick={handleCloseButtonClick}>&times;</span>
        <h2 className="login-title">Hello Admin! Please login.</h2>
        <div className="login-input">
          <label>
            Username:
            <input type="text" value={username} onChange={(e) => setUsername(e.target.value)} />
          </label>
        </div>
        <div className="login-input">
          <label>
            Password:
            <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} />
          </label>
        </div>
        <div className="login-input">
          <button className="login-submit-button" type="button" onClick={handleLogin}>
            Submit
          </button>
        </div>
      </div>
    </div>
  );
}

export default Login;
