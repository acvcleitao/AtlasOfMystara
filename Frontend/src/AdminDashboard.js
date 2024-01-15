// src/AdminDashboard.js
import React from 'react';

function AdminDashboard({ newMapsCount }) {
  return (
    <div>
      <h2>Admin Dashboard</h2>
      <p>New maps: {newMapsCount}</p>
      <button>New Maps ({newMapsCount})</button>
    </div>
  );
}

export default AdminDashboard;
