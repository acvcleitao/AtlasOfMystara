// App.js
import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Home from './Home';
import ExploreAtlas from './ExploreAtlas';
import UploadMap from './UploadMap';
import AdminDashboard from './AdminDashboard';
import { UserProvider } from './UserContext';

const App = () => {
  return (
    <UserProvider>
      <Router>
        <div className="app-container">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/upload" element={<UploadMap />} />
            <Route path="/admin" element={<AdminDashboard />} />
            <Route path="/explore" element={<ExploreAtlas />} />
          </Routes>
        </div>
      </Router>
    </UserProvider>
  );
};

export default App;
