import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { DownOutlined} from '@ant-design/icons';
import { Dropdown, Space } from 'antd';

import './nav_bar.css'

  const NavBar = ({ loggedIn }) => {
  const location = useLocation();
  const isActive = (path) => location.pathname === path ? 'nav-link active' : 'nav-link';

  const unloggedInItems = [
    
    {
      key: '1',
      label: (
        <Link to="/login" className={isActive('/login')}>Login</Link>
      ),
      
    },
    {
      key: '2',
      label: (<Link to="/create_account" className={isActive('/create_account')}>Create Account</Link>),
      
    }]

    const loggedInItems = [
      {
        key: '1',
        label: (
          <Link to="/" className={isActive('/')}>My Profile</Link>
        ),
        
      },
      {
        key: '2',
        label: (<Link to="/logout" className={isActive('/logout')}>Logout</Link>),
        
      }
    ]

  return (
  <header className='header'>
    <Link to="/" className='logo '><img src='p-laylist-logo-white.svg'/><h2>p-laylist</h2></Link>
  <nav className='nav-bar'>
    <Link to="/" className={isActive('/')}>Home</Link>
    <Link to="/library" className={isActive('/library')}>Library</Link>
    <Link to="/friends" className={isActive('/friends')}>Friends</Link>
    
    {loggedIn ? (
      <>
        <Dropdown
          menu={{ items: loggedInItems }}
        >
          <a onClick={(e) => e.preventDefault()}>
            <Space>
              My Account
              <DownOutlined />
            </Space>
          </a>
        </Dropdown>
      </>
    ) : (
      
      <>
        <Dropdown
          menu={{ items: unloggedInItems }}
        >
          <a onClick={(e) => e.preventDefault()}>
            <Space>
              My Account
              <DownOutlined />
            </Space>
          </a>
        </Dropdown>
        
        
      </>
    )}
  </nav>
  </header>
);
};

export default NavBar;
