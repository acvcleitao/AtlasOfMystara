// index.js or your root file
import React from 'react';
import ReactDOM from 'react-dom';
import App from './App';
import { UserProvider } from './UserContext';
import 'leaflet/dist/leaflet.css';

ReactDOM.render(
  <UserProvider>
    <App />
  </UserProvider>,
  document.getElementById('root')
);
