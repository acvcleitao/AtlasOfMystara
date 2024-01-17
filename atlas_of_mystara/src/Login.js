// Login.js
import React, { useState } from 'react';
import { useUser } from './UserContext';
import './Login.css';

function Login({ onClosePopup }) {
  const { login } = useUser();
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const handleLogin = async () => {
    try {
      // Make a request to your backend to authenticate the user
      const response = await fetch('http://127.0.0.1:5000', {
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
          login();
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
