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

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('/api/create_account', formData);
      alert(response.data.message);
    } catch (err) {
      setError(err.response.data.error);
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

// {% extends 'base.html' %}

// {% block content %}
// <div class="centered-container">
//     <h2 class="heading">Create Account</h2>
//     <p>Welcome to Tyler's Twitter Clone! To get started, please fill out this form to create an account.
//     {% if username_exists %}
//     <p class="error-message">ERROR: username already exists. Please try again.</p>
//     {% endif %}
//     {% if passwords_different %}
//     <p class="error-message">ERROR: passwords do not match</p>
//     {% endif %}

//     <form class="login-form" action="/create_account" method="POST">
//         <table>
//             <tr>
//                 <td>Name</td>
//                 <td><input type="text" required name="name"></td>
//             </tr>
//             <tr>
//                 <td>Username</td>
//                 <td><input type="text" required name="username"></td>
//             </tr>
//             <tr>
//                 <td>Password</td>
//                 <td><input type="password" required minlength="8" name="password1"></td>
//             </tr>
//             <tr>
//                 <td>Confirm Password</td>
//                 <td><input type="password" required minlength="8" name="password2"></td>
//             </tr>
//             <tr>
//                 <td></td>
//                 <td><input type="submit" value="Create Account"></td>
//             </tr>
//         </table>
//     </form>
// </div>
// {% endblock %}
