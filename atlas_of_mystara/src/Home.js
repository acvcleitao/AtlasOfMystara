import React from 'react';
import { Link } from 'react-router-dom';

const Home = () => (
  <div className="home-container">
    <Link to="/explore">
      <button>Explore the Atlas</button>
    </Link>
    <Link to="/upload">
      <button>Upload Map</button>
    </Link>
  </div>
);

export default Home;
