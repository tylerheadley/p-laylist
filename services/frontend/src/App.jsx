import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Home from './components/home';
import Search from './components/search';
import Trending from './components/trending';
import CreateMessage from './components/create_message';
import Login from './components/login';
import Logout from './components/logout';
import CreateAccount from './components/create_account';
import NavBar from './components/base';

const App = () => {
  return (
    <Router>
      <div>
        <NavBar loggedIn={true /* You can replace this with actual login state */} />
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/search" element={<Search />} />
          <Route path="/trending" element={<Trending />} />
          <Route path="/create_message" element={<CreateMessage />} />
          <Route path="/login" element={<Login />} />
          <Route path="/logout" element={<Logout />} />
          <Route path="/create_account" element={<CreateAccount />} />
        </Routes>
      </div>
    </Router>
  );
};

export default App;

