import React, { useState } from 'react';
import axios from 'axios';
import './create_account.css'

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
      // Use the API_URL in the axios request
      const response = await axios.post(`${API_URL}/api/create_account`, formData);
      alert(response.data.message);
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
      {error && <p className="error-message">{error}</p>}
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
          
          <div className='container-text-box'><
            h4 className='labelline'>Password</h4>
            <input className='create-form-text-box' type="password" required name="password1" onChange={handleChange} />
          </div>
            
          <div className='container-text-box'>
            <h4 className='labelline'>Confirm Password</h4>
            <input className='create-form-text-box' type="password" required name="password2" onChange={handleChange} />
          </div>
          
            <input className='submit-button' type="submit" value="Sign Up" />
          
        
      </form>
      </div>
    </div>
    </div>
  );
};

export default CreateAccount;


// import React, { useState } from 'react';
// import axios from 'axios';

// const CreateAccount = () => {
//   const [formData, setFormData] = useState({
//     name: '',
//     username: '',
//     password1: '',
//     password2: ''
//   });
//   const [error, setError] = useState('');

//   const handleSubmit = async (e) => {
//     e.preventDefault();
//     try {
//       const response = await axios.post('/api/create_account', formData);
//       alert(response.data.message);
//     } catch (err) {
//       setError(err.response.data.error);
//     }
//   };

//   const handleChange = (e) => {
//     setFormData({ ...formData, [e.target.name]: e.target.value });
//   };

//   return (
//     <div className="centered-container">
//       <h2 className="heading">Create Account</h2>
//       {error && <p className="error-message">{error}</p>}
//       <form className="login-form" onSubmit={handleSubmit}>
//         <table>
//           <tr>
//             <td>Name</td>
//             <td><input type="text" required name="name" onChange={handleChange} /></td>
//           </tr>
//           <tr>
//             <td>Username</td>
//             <td><input type="text" required name="username" onChange={handleChange} /></td>
//           </tr>
//           <tr>
//             <td>Password</td>
//             <td><input type="password" required name="password1" onChange={handleChange} /></td>
//           </tr>
//           <tr>
//             <td>Confirm Password</td>
//             <td><input type="password" required name="password2" onChange={handleChange} /></td>
//           </tr>
//           <tr>
//             <td></td>
//             <td><input type="submit" value="Create Account" /></td>
//           </tr>
//         </table>
//       </form>
//     </div>
//   );
// };

// export default CreateAccount;

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
