import React, { useState } from 'react';
import axios from 'axios';

const Login = () => {
  const [formData, setFormData] = useState({
    username: '',
    password: ''
  });
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('/api/login', formData);
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

// {% extends 'base.html' %}

// {% block content %}
// <div class="centered-container">
//     <h2 class="heading">Login</h2>

//     {% if not login_default %}
//         {% if not logged_in %}
//         <p class="error-message">ERROR: your username and password are incorrect. Please try again.</p>
//         {% else %}
//         <p class="success-message">Login Successful</p>
//         {% endif %}
//     {% endif %}

//     <form class="login-form" action="/login" method="POST">
//         <table>
//             <tr>
//                 <td>username</td>
//                 <td><input type="text" required name="username"></td>
//             </tr>
//             <tr>
//                 <td>password</td>
//                 <td><input type="password" required name="password"></td>
//             </tr>
//             <tr>
//                 <td></td>
//                 <td><input type="submit" value="Login"></td>
//             </tr>
//         </table>
//     </form>
// </div>
// {% endblock %}
