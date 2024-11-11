import React, { useState } from 'react';
import axios from 'axios';
import './Login.css'; // Make sure to add this CSS file for styling

const Login = () => {
  const [formData, setFormData] = useState({
    email: '',
    password: ''
  });
  const [error, setError] = useState('');
  const API_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:1341';

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post(`${API_URL}/login`, new URLSearchParams(formData), {
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      });
      alert(response.data.message);
    } catch (err) {
      setError(err.response?.data?.error || "An unexpected error occurred");
    }
  };

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  return (
    <div className="centered-container">
      <div className="login-box">
        <h2 className="heading">Login</h2>
        {error && <p className="error-message">{error}</p>}
        <form className="login-form" onSubmit={handleSubmit}>
          <div className="form-group">
            <label>Email</label>
            <input type="email" required name="email" onChange={handleChange} />
          </div>
          <div className="form-group">
            <label>Password</label>
            <input type="password" required name="password" onChange={handleChange} />
          </div>
          <button type="submit" className="submit-button">Login</button>
        </form>
        <div className="separator">or</div>
        <div className="social-login">
          <button className="google-button">Login with Google</button>
          <button className="spotify-button">Login with Spotify</button>
        </div>
        <div className="additional-options">
          <p><a href="/forgot-password">Forgot your password?</a></p>
          <p><a href="/create-account">Create an account</a></p>
        </div>
      </div>
    </div>
  );
};

export default Login;
