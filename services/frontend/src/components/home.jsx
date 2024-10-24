import React, { useEffect, useState } from 'react';
import axios from 'axios';

const Home = () => {
  const [tweets, setTweets] = useState([]);
  const [prevPageUrl, setPrevPageUrl] = useState(null);
  const [nextPageUrl, setNextPageUrl] = useState(null);
  const [page, setPage] = useState(1); // Manage current page state

  // Function to fetch data from the API
  const fetchTweets = (pageNumber) => {
    axios.get(`/?page=${pageNumber}`)
      .then((response) => {
        // Ensure response.data.tweets exists before setting state
        const { tweets = [], next_page_url, prev_page_url } = response.data;
        setTweets(tweets);
        setPrevPageUrl(prev_page_url);
        setNextPageUrl(next_page_url);
        setPage(pageNumber); // Update the current page
      })
      .catch((error) => {
        console.error('Error fetching tweets:', error);
        // Optionally handle error by resetting tweets or showing a message
      });
  };

  // Fetch data on component mount
  useEffect(() => {
    fetchTweets(page);
  }, [page]);

  return (
    <div className="centered-container">
      <h2>Home Feed</h2>
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
