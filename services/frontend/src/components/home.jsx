import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useLocation } from 'react-router-dom';

const Home = () => {
  const [tweets, setTweets] = useState([]);
  const [prevPageUrl, setPrevPageUrl] = useState(null);
  const [nextPageUrl, setNextPageUrl] = useState(null);
  const [page, setPage] = useState(1);
  const [spotifyConnected, setSpotifyConnected] = useState(false);
  const location = useLocation();

  const API_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:1341';

  const fetchTweets = (pageNumber) => {
    axios.get(`${API_URL}/?page=${pageNumber}`)
      .then((response) => {
        const { tweets = [], next_page_url, prev_page_url } = response.data;
        setTweets(tweets);
        setPrevPageUrl(prev_page_url);
        setNextPageUrl(next_page_url);
        setPage(pageNumber);
      })
      .catch((error) => {
        console.error('Error fetching tweets:', error);
      });
  };

  useEffect(() => {
    const params = new URLSearchParams(location.search);
    if (params.get('spotify_connected') === '1') {
      setSpotifyConnected(true);
    }
    fetchTweets(page);
  }, [page, location.search]);

  return (
    <div className="centered-container">
      <h2>Home Feed</h2>
      {spotifyConnected && <p>Spotify connected successfully!</p>}
      <div className="tweets">
        {tweets.length > 0 ? (
          tweets.map((tweet, index) => (
            <div className="tweet" key={index}>
              <div className="user-info">
                <span className="user-name">{tweet.user_name}</span>
                <span className="screen-name">@{tweet.screen_name}</span>
              </div>
              <p className="tweet-text">{tweet.text}</p>
              <p className="created-at">Created at: {new Date(tweet.created_at).toLocaleString()}</p>
            </div>
          ))
        ) : (
          <p>No tweets available.</p>
        )}
      </div>
      <div className="pagination">
        {prevPageUrl && <button onClick={() => fetchTweets(page - 1)}>Previous Page</button>}
        {nextPageUrl && <button onClick={() => fetchTweets(page + 1)}>Next Page</button>}
      </div>
    </div>
  );
};

export default Home;
