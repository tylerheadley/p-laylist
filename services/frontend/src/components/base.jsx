import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';

const NavBar = () => {
  const [loggedIn, setLoggedIn] = useState(false);

  useEffect(() => {
    // Check if the user is logged in by calling the Flask API
    axios.get('/api/check_login')
      .then((response) => {
        setLoggedIn(response.data.logged_in);
      })
      .catch((error) => {
        console.error('Error checking login status:', error);
      });
  }, []);

  return (
    <header>
      <nav className="navbar">
        <h1 className="navbar-title">Big Data Twitter Clone</h1>
        <ol className="navbar-links">
          <li><Link to="/">Home</Link></li>
          <li><Link to="/search">Search</Link></li>
          <li><Link to="/trending">Trending</Link></li>
          {loggedIn ? (
            <>
              <li><Link to="/create_message">Create Message</Link></li>
              <li><Link to="/logout">Logout</Link></li>
            </>
          ) : (
            <>
              <li><Link to="/login">Login</Link></li>
              <li><Link to="/create_account">Create Account</Link></li>
            </>
          )}
        </ol>
      </nav>
    </header>
  );
};

export default NavBar;

// <!-- <!DOCTYPE html>
// <html lang="en">
// <head>
//     <meta charset="UTF-8">
//     <meta name="viewport" content="width=device-width, initial-scale=1.0">
//     <meta http-equiv="X-UA-Compatible" content="ie=edge">
//     <title>Tyler's Twitter Clone</title>
//     <link rel="stylesheet" type="text/css" href="{{ url_for('static', filename='css/styles.css') }}">
// </head>
// <body>
//     <script>0</script>
//     <header>
//         <nav class="navbar">
//             <h1 class="navbar-title">Big Data Twitter Clone</h1>
//             <ol class="navbar-links">
//                 <li><a href='/'>Home</a></li>
//                 <li><a href='/search'>Search</a></li>
//                 <li><a href='/trending'>Trending</a></li>
//                 {% if logged_in %}
//                 <li><a href='/create_message'>Create Message</a></li>
//                 <li><a href='/logout'>Logout</a></li>
//                 {% else %}
//                 <li><a href='/login'>Login</a></li>
//                 <li><a href='/create_account'>Create Account</a></li>
//                 {% endif %}
//             </ol>
//         </nav>
//     </header>

//     {% block content %}
//     {% endblock %}
// </body>
// </html> -->
