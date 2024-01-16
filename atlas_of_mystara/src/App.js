// App.js
import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Link, Navigate } from 'react-router-dom';
import ExploreAtlas from './ExploreAtlas';
import UploadMap from './UploadMap';
import Login from './Login';
import AdminDashboard from './AdminDashboard';

import './App.css';

const Home = () => (
  <div className="home-container">
    <Link to="/explore">
      <button>Explore the Atlas</button>
    </Link>
    <Link to="/upload">
      <button>Upload Map</button>
    </Link>
  </div>
)

const App = () => {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [showLoginPopup, setShowLoginPopup] = useState(false);

  const handleLogin = () => {
    setIsLoggedIn(true);
    setShowLoginPopup(false);
  };

  const handleLogout = () => {
    setIsLoggedIn(false);
  };

  const handleNewMaps = () => {
    return 1;
  }

  return (
    <Router>
      <div className="app-container">
        <h1>Atlas of Mystara</h1>
        <h2>Welcome to the Atlas of Mystara</h2>

        <Routes>
          <Route path="/" element={<Home isLoggedIn={isLoggedIn}/>} />
          <Route path="/explore" element={<ExploreAtlas />} />
          <Route path="/upload" element={<UploadMap />} />
          <Route
            path="/admin"
            element={isLoggedIn ? <AdminDashboard /> : <Navigate to="/" />}
          />
        </Routes>

        <div>
          {!isLoggedIn && (
            <button className="login-button" onClick={() => setShowLoginPopup(true)}>
              Login
            </button>
          )}

          {isLoggedIn && (
            <button className="login-button" onClick={handleLogout}>
              Logout
            </button>
          )}
        </div>

        <div>
        {isLoggedIn && (
          <button className='newmaps-button' onClick={handleNewMaps}>
            New Maps
          </button>
        )}
        </div>

        <div>
          {showLoginPopup && (
            <Login onLogin={handleLogin} onClosePopup={() => setShowLoginPopup(false)} />
          )}
        </div>
      </div>
    </Router>
  );
};

export default App;
