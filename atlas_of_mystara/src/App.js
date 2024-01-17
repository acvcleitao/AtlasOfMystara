// App.js
import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import ExploreAtlas from './ExploreAtlas';  
import UploadMap from './UploadMap';
import Login from './Login';
import AdminDashboard from './AdminDashboard';
import Home from './Home';

import './App.css';

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
          <Route path="/" element={<Home />} />
          <Route path="/upload" element={<UploadMap />} />
          <Route
            path="/admin"
            element={isLoggedIn ? <AdminDashboard /> : <Navigate to="/" />}
          />
          <Route path="/explore" element={<ExploreAtlas />} />
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
