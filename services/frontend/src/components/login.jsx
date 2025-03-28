import React, { useState } from 'react';
import axios from 'axios';
import './login.css'; 
import './create_account.css'; 
import Button from '@mui/material/Button';
import { Link, useLocation } from 'react-router-dom';


const Login = () => {
  const location = useLocation();
  const isActive = (path) => location.pathname === path ? 'nav-link active' : 'nav-link';
  const [formData, setFormData] = useState({
    username: '',
    password: ''
  });
  const [error, setError] = useState('');
  const API_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:1341';

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post(`${API_URL}/login`, new URLSearchParams(formData), {
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        withCredentials: true
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
        <div className="title-section">
          <h2 className="heading">Login</h2>
          <p className="subheading">Welcome back! Login to continue to your personalized music experience.</p>
          <img src='p-laylist-logo.svg' className='login-image'/>
        </div>
        <form className="login-form" onSubmit={handleSubmit}>
          <div className="form-group">
        
            <input type="text" required name="username"  className='login-form-box' onChange={handleChange} placeholder='Username'/>
          </div>
          <div className="form-group">
          
            <input type="password" required name="password" className='login-form-box' onChange={handleChange} placeholder='Password' />
          </div>
          {error && <p className="error-message">{error}</p>}
          <Button variant="contained" type ='submit' id='login-button'>Login</Button>
          <div className='sign-up-section'>
            <p>Don't have an account?</p><Link to="/create_account" className='link-sign'>Sign Up.</Link>
          </div>
        </form>
      </div>
    </div>
  );
};

export default Login;
