import React, { useState, useEffect } from 'react';
import axios from 'axios';

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
    <div className="centered-container">
      <h2>Create Account</h2>
      {error && <p className="error-message">{error}</p>}
      <form onSubmit={handleSubmit}>
        <input type="text" name="name" placeholder="Name" required onChange={handleChange} />
        <input type="text" name="username" placeholder="Username" required onChange={handleChange} />
        <input type="password" name="password1" placeholder="Password" required onChange={handleChange} />
        <input type="password" name="password2" placeholder="Confirm Password" required onChange={handleChange} />
        <button type="submit" disabled={loading}>
          {loading ? "Creating Account..." : "Create Account"}
        </button>
      </form>
    </div>
  );
};

export default CreateAccount;