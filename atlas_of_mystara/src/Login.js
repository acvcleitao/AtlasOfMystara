// Login.js
import React, { useState } from 'react';
import './Login.css';

function Login({ onLogin, onClosePopup }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const handleLogin = () => {
    // Perform login logic
    onLogin();
    // Close the popup
    onClosePopup();
  };
  const handleLoginBackend = async () => {
    try {
      // Make a request to your backend to authenticate the user
      const response = await fetch('http://your-backend-url/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, password }),
      });

      if (response.ok) {
        const data = await response.json();
        // Assuming the backend sends back whether the user is an admin or not
        if (data.isAdmin) {
          onLogin();
        } else {
          alert('User is not an admin');
        }
        onClosePopup();
      } else {
        alert('Invalid username or password');
      }
    } catch (error) {
      console.error('Login error:', error);
      alert('An error occurred during login');
    }
  };

  return (
    <div className="popup-container">
      <div className="login-popup">
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
