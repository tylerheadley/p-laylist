import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './create_account.css'
import Button from '@mui/material/Button';



const CreateAccount = () => {
  const [formData, setFormData] = useState({ name: '', username: '', password1: '', password2: '' });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const API_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:1341';

  useEffect(() => {
    document.cookie.split(";").forEach((cookie) => {
      const eqPos = cookie.indexOf("=");
      const name = eqPos > -1 ? cookie.substr(0, eqPos) : cookie;
      document.cookie = `${name}=;expires=Thu, 01 Jan 1970 00:00:00 GMT;path=/`;
    });
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (formData.password1 !== formData.password2) {
      setError('Passwords do not match');
      return;
    }

    setLoading(true); // Start loading
    try {
      const response = await axios.post(`${API_URL}/create_account`, formData);
      if (response.status === 201) {
        window.location.href = response.data.redirect;
      } else {
        setError('Unexpected response from the server');
      }
    } catch (err) {
      setError(err.response?.data?.error || 'An error occurred');
    } finally {
      setLoading(false); // End loading
    }
  };

  const handleChange = (e) => setFormData({ ...formData, [e.target.name]: e.target.value });


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
            <Button variant="contained" type ='submit' id='submit-button'> {loading ? "Creating Account..." : "Sign Up "}</Button>
        
        
      </form>
      </div>
    </div>
    </div>
  );
};

export default CreateAccount;