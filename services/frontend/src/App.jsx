import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Home from './components/home';
import Search from './components/search';
import Trending from './components/trending';
import CreateMessage from './components/create_message';
import Login from './components/login';
import Logout from './components/logout';
import CreateAccount from './components/create_account';
import NavBar from './components/nav_bar';
import axios from 'axios';

const API_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:1341';

const App = () => {
  const [loggedIn, setLoggedIn] = useState(false);

  // Check if user is logged in when the app loads
  useEffect(() => {
    const checkLoginStatus = async () => {
      try {
        const response = await axios.get(`${API_URL}/is_logged_in`);
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

// import React from 'react';
// import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
// import Home from './components/home';
// import Search from './components/search';
// import Trending from './components/trending';
// import CreateMessage from './components/create_message';
// import Login from './components/login';
// import Logout from './components/logout';
// import CreateAccount from './components/create_account';
// import NavBar from './components/base';

// const App = () => {
//   return (
//     <Router>
//       <div>
//         <NavBar loggedIn={true /* You can replace this with actual login state */} />
//         <Routes>
//           <Route path="/" element={<Home />} />
//           <Route path="/search" element={<Search />} />
//           <Route path="/trending" element={<Trending />} />
//           <Route path="/create_message" element={<CreateMessage />} />
//           <Route path="/login" element={<Login />} />
//           <Route path="/logout" element={<Logout />} />
//           <Route path="/create_account" element={<CreateAccount />} />
//         </Routes>
//       </div>
//     </Router>
//   );
// };

// export default App;
