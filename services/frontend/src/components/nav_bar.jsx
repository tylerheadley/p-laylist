import React from 'react';
import { Link } from 'react-router-dom';

const NavBar = ({ loggedIn }) => (
  <nav>
    <Link to="/">Home</Link>
    <Link to="/search">Search</Link>
    <Link to="/create_message">Create Message</Link>
    {loggedIn ? (
      <>
        <Link to="/logout">Logout</Link>
      </>
    ) : (
      <>
        <Link to="/login">Login</Link>
        <Link to="/create_account">Create Account</Link>
      </>
    )}
  </nav>
);

export default NavBar;
