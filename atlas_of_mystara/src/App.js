// App.js
import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Home from './Home';
import ExploreAtlas from './ExploreAtlas';
import UploadMap from './UploadMap';
import NewMaps from './NewMaps';
import { UserProvider } from './UserContext';
import MapDetails from './MapDetails';

const App = () => {
  return (
    <UserProvider>
      <Router>
        <div className="app-container">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/upload" element={<UploadMap />} />
            <Route path="/new_maps" element={<NewMaps />} />
            <Route path="/explore" element={<ExploreAtlas />} />
            <Route path="/map/:id" element={<MapDetails />} />
          </Routes>
        </div>
      </Router>
    </UserProvider>
  );
};

export default App;
