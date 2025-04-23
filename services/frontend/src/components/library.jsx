import React, { useState, useEffect } from 'react';

const Library = () => {

    const API_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:1341';

  const getLibrary = async() => {
    try {
      const response = await fetch(`${API_URL}/get_library`, {
        method: "GET",
        credentials: "include"
      });
      console.log('Fetch Response:', response);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      console.log('Library Data:', data.songs);      

    } catch(error) {
        console.error('Error fetching songs:', error);
      };
  };


    useEffect(() => {
      getLibrary();
    }, [])

    return (
        <div className="total-container">
            <h2>Search</h2>
            
        </div>
    );
};

export default Library;
