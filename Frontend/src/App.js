// src/App.js
import React, { useState } from 'react';
import { BrowserRouter as Router, Route, Link, Redirect } from 'react-router-dom';
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
    // In a real scenario, you would authenticate the user on the backend
    // and then set the states accordingly based on the response.
    setIsLoggedIn(true);
    setIsAdmin(true); // For demonstration, assuming the logged-in user is an admin.
    setNewMapsCount(3); // For demonstration, assuming there are 3 new maps.
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
            {isAdmin && (
              <Link to="/admin">
                <button>New Maps ({newMapsCount})</button>
              </Link>
            )}
            <button onClick={handleLogout}>Logout</button>
          </div>
        ) : (
          <Redirect to="/" />
        )}
        <Route path="/explore" component={ExploreAtlas} />
        <Route path="/upload" component={UploadMap} />
        <Route
          path="/login"
          component={() => <Login onLogin={handleLogin} />}
        />
        <Route
          path="/admin"
          component={() => <AdminDashboard newMapsCount={newMapsCount} />}
        />
        <Route
          path="/"
          exact
          component={() => <Home onLogin={handleLogin} />}
        />
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
