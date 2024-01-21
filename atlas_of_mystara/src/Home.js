import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useUser } from './UserContext';
import Login from './Login';

import './Home.css';

const Home = () => {
  const { isLoggedIn, login, logout, setNewMapsCount, newMapsCount } = useUser();
  const [showLoginPopup, setShowLoginPopup] = useState(false);

  useEffect(() => {
    // Add the 'home' class to the body when the component mounts
    document.body.classList.add('home');
    // Remove the 'home' class from the body when the component unmounts
    return () => {
      document.body.classList.remove('home');
    };
  }, []);

  useEffect(() => {
    const fetchNewMapsCount = async () => {
      try {
        // Make a request to the backend to get the new maps count
        const response = await fetch('http://127.0.0.1:5000/getNewMapsCount', {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
          },
        });

        if (response.ok) {
          const data = await response.json();
          setNewMapsCount(data.newMapsCount);
        } else {
          console.error('Failed to fetch new maps count');
        }
      } catch (error) {
        console.error('Error fetching new maps count:', error);
      }
    };

    // Fetch the new maps count only if the user is logged in
    if (isLoggedIn) {
      fetchNewMapsCount();
    }
  }, [isLoggedIn, setNewMapsCount]);

  const handleLogin = () => {
    setShowLoginPopup(true);
  };

  const handleLogout = () => {
    logout();
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
      {isLoggedIn ? (
        <div>
          <button className='login-out-button' onClick={handleLogout}>Logout</button>
          <Link to="/new_maps">
            <button className='new-maps-button'>
              New Maps ({newMapsCount})
            </button>
          </Link>
        </div>
      ) : (
        <button className='login-out-button' onClick={handleLogin}>Login</button>
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
