import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useLocation } from 'react-router-dom';
import './home.css'
import Carousel from 'react-multi-carousel';
import 'react-multi-carousel/lib/styles.css';


const Home = ({ loggedIn }) => {

  
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
    if (loggedIn) {
      console.log("logged in. fetching songs")

      fetchSongs();
    }
    else {
      console.log("not logged in.")
    }
    
  }, []);
  
  const responsive = {
    desktop: {
      breakpoint: { max: 3000, min: 1024 },
      items: 3,
      slidesToSlide: 1 // optional, default to 1.
    },
    tablet: {
      breakpoint: { max: 1024, min: 464 },
      items: 2,
      slidesToSlide: 2 // optional, default to 1.
    },
    mobile: {
      breakpoint: { max: 464, min: 0 },
      items: 1,
      slidesToSlide: 1 // optional, default to 1.
    }
  };


  return (
    
    <div className="song-container">
      <div className='title-section'>
        <h2 className='title'>Home</h2>
        <p className='subheading'>What would you like to listen to today?</p>
      </div>
      {spotifyConnected && <p>Spotify connected successfully!</p>}
      <div className="songs-section">
      <h2 className='song-section-title'>Your Daily Recommendations</h2>
      <Carousel
        swipeable={false}
        draggable={true}
        showDots={false}
        responsive={responsive}
        ssr={true} // means to render carousel on server-side.
        infinite={true}
        autoPlaySpeed={1000}
        keyBoardControl={true}
        customTransition="transform 0.8s ease-in-out"
        transitionDuration={800} 
        renderButtonGroupOutside={true}
        containerClass="carousel-container"
        removeArrowOnDeviceType={["tablet", "mobile"]}
        
        dotListClass="custom-dot-list-style"
        itemClass="carousel-item-padding-40-px"
      >
        {songList.length > 0 ? (

          songList.map((song, index) => (
            <div className="song" key={index}>
              <div className="song-info">
                <h3 className="song-title">{song.title}</h3>
                <p className="song-inf">{song.artist} · <em>{song.album}</em> · {song.duration}</p>
              </div>
              <div className="song-info">
                <p className="song-interactions"></p>
              </div>
              
              
            </div>
          ))
        
        ) : (
          <p>No songs available.</p>
        )}

      </Carousel>
      </div>
      
    </div>
  );
};

export default Home;
