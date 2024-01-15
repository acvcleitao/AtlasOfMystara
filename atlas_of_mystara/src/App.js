// src/App.js
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

  const handleLogin = () => {
    setIsLoggedIn(true);
    setIsAdmin(true);
    setNewMapsCount(3);
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
        {isLoggedIn ? (
          <div>
            <Link to="/explore">
              <button>Explore the Atlas</button>
            </Link>
            <Link to="/upload">
              <button>Upload Map</button>
            </Link>
            <Link to="/login">
              <button>Login</button>
            </Link>
            {isAdmin && (
              <Link to="/admin">
                <button>New Maps ({newMapsCount})</button>
              </Link>
            )}
            <button onClick={handleLogout}>Logout</button>
          </div>
        ) : (
          <Navigate to="/" />
        )}
        <Routes>
          <Route path="/explore" element={<ExploreAtlas />} />
          <Route path="/upload" element={<UploadMap />} />
          <Route path="/login" element={<Login onLogin={handleLogin} />} />
          <Route path="/admin" element={<AdminDashboard newMapsCount={newMapsCount} />} />
          <Route path="/" element={<Home onLogin={handleLogin} />} />
        </Routes>
      </div>
    </Router>
  );
}

function Home({ onLogin }) {
  return (
    <div>
      <h2>Welcome to the Atlas of Mystara</h2>
      <Link to="/explore">
        <button>Explore the Atlas</button>
      </Link>
      <Link to="/upload">
        <button>Upload Map</button>
      </Link>
      <Link to="/login">
        <button onClick={onLogin}>Login</button>
      </Link>
    </div>
  );
}

export default App;
