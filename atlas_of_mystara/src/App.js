// App.js
import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Link, Navigate } from 'react-router-dom';
import ExploreAtlas from './ExploreAtlas';
import UploadMap from './UploadMap';
import Login from './Login';
import AdminDashboard from './AdminDashboard';

import './App.css';

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [isAdmin, setIsAdmin] = useState(false);
  const [newMapsCount, setNewMapsCount] = useState(0);
  const [showLoginPopup, setShowLoginPopup] = useState(false);

  const handleLogin = () => {
    setIsLoggedIn(true);
    setIsAdmin(true);
    setNewMapsCount(3);
    setShowLoginPopup(false);
  };

  const handleLogout = () => {
    setIsLoggedIn(false);
    setIsAdmin(false);
    setNewMapsCount(0);
  };

  return (
    <Router>
      <div className="app-container">
        <h1>Atlas of Mystara</h1>
        <h2>Welcome to the Atlas of Mystara</h2>
        {isLoggedIn && (
          <div>
            <Link to="/explore">
              <button>Explore the Atlas</button>
            </Link>
            <Link to="/upload">
              <button>Upload Map</button>
            </Link>
            {isAdmin && (
              <Link to="/admin">
                <button>New Maps ({newMapsCount})</button>
              </Link>
            )}
            <button className="login-button" onClick={handleLogout}>
              Logout
            </button>
          </div>
        )}
        {!isLoggedIn && (
          <div>
            <Link to="/explore">
              <button>Explore the Atlas</button>
            </Link>
            <Link to="/upload">
              <button>Upload Map</button>
            </Link>
            <button className="login-button" onClick={() => setShowLoginPopup(true)}>
              Login
            </button>
          </div>
        )}
        <Routes>
          <Route
            path="/"
            element={
              isLoggedIn ? (
                <Home isLoggedIn={isLoggedIn} newMapsCount={newMapsCount} />
              ) : (
                <Navigate to="/" />
              )
            }
          />
          <Route path="/explore" element={<ExploreAtlas />} />
          <Route path="/upload" element={<UploadMap />} />
          <Route path="/admin" element={<AdminDashboard newMapsCount={newMapsCount} />} />
        </Routes>
        {showLoginPopup && (
          <Login onLogin={handleLogin} onClosePopup={() => setShowLoginPopup(false)} />
        )}
      </div>
    </Router>
  );
}

function Home({ newMapsCount }) {
  return (
    <div>
      <Link to="/explore">
        <button>Explore the Atlas</button>
      </Link>
      <Link to="/upload">
        <button>Upload Map</button>
      </Link>
      <Link to="/admin">
        <button>New Maps ({newMapsCount})</button>
      </Link>
    </div>
  );
}


export default App;
