// Home.js
import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { useUser } from './UserContext';
import Login from './Login';

import './Home.css';


const Home = () => {
  const { isLoggedIn, login } = useUser();
  const [showLoginPopup, setShowLoginPopup] = useState(false);

  const handleLogin = () => {
    setShowLoginPopup(true);
  };

  const handleLoginSuccess = () => {
    login();
    setShowLoginPopup(false);
  };

  return (
    <div>
      <h1>Atlas of Mystara</h1>
      <h2>Welcome to the Atlas of Mystara</h2>
      <Link to="/explore">
        <button>Explore the Atlas</button>
      </Link>
      <Link to="/upload">
        <button>Upload Map</button>
      </Link>
      {!isLoggedIn && (
        <button className='login-button' onClick={handleLogin}>Login</button>
      )}

      {/* Conditionally render Login component based on showLoginPopup */}
      {showLoginPopup && (
        <Login
          onLogin={handleLoginSuccess}
          onClosePopup={() => setShowLoginPopup(false)}
        />
      )}
    </div>
  );
};

export default Home;
