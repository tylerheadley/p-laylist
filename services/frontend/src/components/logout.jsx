import React, { useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

const API_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:1341';

const Logout = () => {
  const navigate = useNavigate();

  useEffect(() => {
    const logoutUser = async () => {
      try {
        const response = await axios.get(`${API_URL}/logout`, { withCredentials: true });
        alert(response.data.message);

        navigate('/login');
      } catch (error) {
        console.error('Error during logout:', error);
      }
    };

    logoutUser();
  }, [navigate]);

  return (
    <div className="centered-container">
      <h2>Logout</h2>
      <p className="success-message">Logging you out...</p>
    </div>
  );
};

export default Logout;

