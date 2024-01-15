// src/Login.js
import React, { useState } from 'react';
import LoginPopup from './LoginPopup';

function Login({ onLogin }) {
  const [showPopup, setShowPopup] = useState(false);

  const handleLogin = () => {
    // Perform any additional login logic
    onLogin();
    setShowPopup(false);
  };

  return (
    <div>
      <h2>Login</h2>
      <button onClick={() => setShowPopup(true)}>Open Login Popup</button>

      {showPopup && (
        <LoginPopup
          onClose={() => setShowPopup(false)}
          onLogin={handleLogin}
        />
      )}
    </div>
  );
}

export default Login;
