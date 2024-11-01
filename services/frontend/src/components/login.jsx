import React, { useState } from 'react';
import axios from 'axios';

const Login = () => {
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
      <h2 className="heading">Login</h2>
      {error && <p className="error-message">{error}</p>}
      <form className="login-form" onSubmit={handleSubmit}>
        <table>
          <tr>
            <td>Username</td>
            <td><input type="text" required name="username" onChange={handleChange} /></td>
          </tr>
          <tr>
            <td>Password</td>
            <td><input type="password" required name="password" onChange={handleChange} /></td>
          </tr>
          <tr>
            <td></td>
            <td><input type="submit" value="Login" /></td>
          </tr>
        </table>
      </form>
    </div>
  );
};

export default Login;
