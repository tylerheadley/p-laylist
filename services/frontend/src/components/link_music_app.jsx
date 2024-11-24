// import React, { useEffect } from 'react';
import { useLocation } from 'react-router-dom';

const LinkMusic = () => {
    const location = useLocation();
    const params = new URLSearchParams(location.search);
    const spotifyConnected = params.get("spotify_connected") === "1";
    const handleSpotifyLink = async () => {
        window.location.href = "http://localhost:1341/spotify_authorize";
      };

    return (
      <div style={{ textAlign: 'center', padding: '2rem' }}>
        <h2>Link Your Music Account</h2>
        {spotifyConnected ? (
          <p>Spotify is connected! You may proceed with your account setup.</p>
        ) : (
          <div>
            <p>Please connect to a music service to complete your account setup.</p>
            <button onClick={handleSpotifyLink} style={{ padding: '1rem', marginTop: '1rem' }}>
              Link Spotify Account
            </button>
          </div>
        )}
      </div>
    );
  };

export default LinkMusic;