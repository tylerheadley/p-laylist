import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Home from './components/home';
import Library from './components/library';
import Friends from './components/friends';
import Login from './components/login';
import Logout from './components/logout';
import CreateAccount from './components/create_account';
import NavBar from './components/nav_bar';
import LinkMusic from './components/link_music_app';
import axios from 'axios';


const API_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:1341';

const App = () => {
  const [loggedIn, setLoggedIn] = useState(false);

  // Check if user is logged in when the app loads
  useEffect(() => {
    const checkLoginStatus = async () => {
      try {
        const response = await axios.get(`${API_URL}/check_logged_in`);
        setLoggedIn(response.data.loggedIn);
      } catch (error) {
        console.error("Error checking login status:", error);
      }
    };

    checkLoginStatus();
  }, []);

  return (
    <Router>
      <div>
        <NavBar loggedIn={loggedIn} />
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/library" element={<Library />} />
          <Route path="/friends" element={<Friends />} />
          <Route path="/login" element={<Login />} />
          <Route path="/logout" element={<Logout />} />
          <Route path="/create_account" element={<CreateAccount />} />
          <Route path="/link_music_app" element={<LinkMusic />} />
        </Routes>
      </div>
    </Router>
  );
};

export default App;
