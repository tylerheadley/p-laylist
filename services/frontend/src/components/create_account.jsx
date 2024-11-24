import React, { useState } from 'react';
import axios from 'axios';
import './create_account.css'
import Button from '@mui/material/Button';
import LinkMusic from './link_music_app';


const CreateAccount = () => {
  const [formData, setFormData] = useState({
    name: '',
    username: '',
    password1: '',
    password2: ''
  });
  const [error, setError] = useState('');
  const API_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:1341';

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post(`${API_URL}/create_account`, formData);
      alert(response.data.message);
      // Redirect to Spotify OAuth flow after account creation
      window.location.href = `${API_URL}/spotify_authorize`;
    } catch (err) {
      setError(err.response?.data?.error || 'An error occurred');
    }
  };

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  return (
    <div className='page-background'>
    <div className="flex-container">
      {/* left side of page info */}
      <div className = 'information-container'> 
        <h2 className="heading pale-white bolded">Join P-laylist</h2>
        {/* image with text besides it container*/}
        <div className='info-bullet-points'>
          <img src='Music-note.svg'/>
          <h3 className = 'pale-white'>Get <span className='bolded'>free, personalized</span> music recommendations </h3>
        </div>
        <div className='info-bullet-points'>
          <img src='Music-note.svg'/>
          <h3 className = 'pale-white'><span className='bolded'>Connect</span> with friends and share music</h3>
        </div>
        <div className='info-bullet-points'>
          <img src='Music-note.svg'/>
          <h3 className = 'pale-white'>Expand your music taste with a <span className='bolded'>diverse</span> range of recommendations</h3>
        </div>
        

      </div>
      <div className='form-container'>
      
      <form className="login-form" onSubmit={handleSubmit}>
      <h2 className="heading">Create Account</h2>
        
        
          <div className='container-text-box'>
            <h4 className='labelline'>Name</h4>
            <input className='create-form-text-box' type="text" required name="name" onChange={handleChange} />
            
          </div>
        
          
          <div className='container-text-box'>
            <h4 className='labelline'>Username</h4>
            <input className='create-form-text-box' type="text" required name="username" onChange={handleChange} />
          </div>
          
          <div className='container-text-box'>
            <h4 className='labelline'>Password</h4>
            <input className='create-form-text-box' type="password" required name="password1" onChange={handleChange} />
          </div>
            
          <div className='container-text-box'>
            <h4 className='labelline'>Confirm Password</h4>
            <input className='create-form-text-box' type="password" required name="password2" onChange={handleChange} />
          </div>
          {error && <p className="error-message">{error}</p>}
            <Button variant="contained" type ='submit' id='submit-button'>Sign Up</Button>
        
        
      </form>
      </div>
    </div>
    </div>
  );
};

export default CreateAccount;