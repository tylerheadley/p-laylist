import React, { useState, useEffect } from 'react';
import SongGrid from './song_grid';

const Library = () => {

  const API_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:1341';
  const [songs, setSongs] = useState([]);

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
      setSongs(data);      

    } catch(error) {
        console.error('Error fetching songs:', error);
      };
  };

    useEffect(() => {
      getLibrary();
    }, [])

    return (
        <div className="total-container">
          <div className='title-section'>
            <h2 className='title'>Library</h2>
            <p className='subheading'>View your songs</p>
          </div>
            <div className='library-grid'>
              <SongGrid songList={songs.songs} />
            </div>
          
        </div>
    );
};

export default Library;
