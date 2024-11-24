import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';

const NavBar = () => {
  const [loggedIn, setLoggedIn] = useState(false);
  const API_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:1341';

  useEffect(() => {
    axios.get(`${API_URL}/api/login`)
      .then((response) => {
        setLoggedIn(response.data.logged_in);
      })
      .catch((error) => {
        console.error('Error checking login status:', error);
      });
  }, [API_URL]);

  return (
    <header>
      <nav className="navbar">
        <h1 className="navbar-title">Big Data Twitter Clone</h1>
        <ol className="navbar-links">
          <li><Link to="/">Home</Link></li>
          <li><Link to="/library">Library</Link></li>
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
