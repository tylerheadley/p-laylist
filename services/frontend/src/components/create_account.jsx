import React, { useState } from 'react';
import axios from 'axios';

const CreateAccount = () => {
  const [formData, setFormData] = useState({
    name: '',
    username: '',
    password1: '',
    password2: ''
  });
  const [error, setError] = useState('');

  // Set the API URL dynamically from environment variables or default to localhost
  const API_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:1341';

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post(`${API_URL}/create_account`, formData);
      alert(response.data.message);
    } catch (err) {
      setError(err.response?.data?.error || 'An error occurred');
    }
  };

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  return (
    <div className="centered-container">
      <h2 className="heading">Create Account</h2>
      {error && <p className="error-message">{error}</p>}
      <form className="login-form" onSubmit={handleSubmit}>
        <table>
          <tr>
            <td>Name</td>
            <td><input type="text" required name="name" onChange={handleChange} /></td>
          </tr>
          <tr>
            <td>Username</td>
            <td><input type="text" required name="username" onChange={handleChange} /></td>
          </tr>
          <tr>
            <td>Password</td>
            <td><input type="password" required name="password1" onChange={handleChange} /></td>
          </tr>
          <tr>
            <td>Confirm Password</td>
            <td><input type="password" required name="password2" onChange={handleChange} /></td>
          </tr>
          <tr>
            <td></td>
            <td><input type="submit" value="Create Account" /></td>
          </tr>
        </table>
      </form>
    </div>
  );
};

export default CreateAccount;
