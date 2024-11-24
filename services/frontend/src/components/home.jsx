import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useLocation } from 'react-router-dom';
import './home.css'



const Home = () => {

  
  const [songList, setsongList] = useState([]);
  const [spotifyConnected, setSpotifyConnected] = useState(false);
  const location = useLocation();


  const API_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:1341';

  const fetchSongs = async() => {
    try {
      const response = await fetch('http://localhost:1341/api/songs');
      console.log('Fetch Response:', response);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      setsongList(data.songs); // Update state
      

    } catch(error) {
        console.error('Error fetching songs:', error);
      };
  };

  useEffect(() => {

    const url = ''
    const params = new URLSearchParams(location.search);
    if (params.get('spotify_connected') === '1') {
      setSpotifyConnected(true);
    }


  }, [location.search]);

  useEffect(() => {
    fetchSongs();
    
    
  }, []);
  
  
  return (
    
    <div className="song-container">
      <div className='title-section'>
        <h2 className='title'>Home</h2>
        <p className='subheading'>What would you like to listen to today?</p>
      </div>
      {spotifyConnected && <p>Spotify connected successfully!</p>}
      <div className="songs-section">
      <h2 className='song-section-title'>Your Daily Recommendations</h2>
        {songList.length > 0 ? (
          songList.map((song, index) => (
            <div className="song" key={index}>
              <div className="song-info">
                <h3 className="song-title">{song.title}</h3>
                <p className="song-inf">{song.artist} · {song.album} · {song.duration}</p>
              </div>
              <div className="song-info">
                <p className="song-interactions"></p>
              </div>
              
              
            </div>
          ))
        ) : (
          <p>No songs available.</p>
        )}
      </div>
      
    </div>
  );
};

export default Home;
