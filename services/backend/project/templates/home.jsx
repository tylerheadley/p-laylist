import React, { useEffect, useState } from 'react';
import axios from 'axios';

const Home = () => {
  const [tweets, setTweets] = useState([]);
  const [prevPageUrl, setPrevPageUrl] = useState('');
  const [nextPageUrl, setNextPageUrl] = useState('');

  useEffect(() => {
    axios.get('/api/search?search_query=')
      .then((response) => {
        setTweets(response.data.tweets);
        setPrevPageUrl(response.data.prev_page_url);
        setNextPageUrl(response.data.next_page_url);
      });
  }, []);

  return (
    <div className="centered-container">
      <h2>Home Feed</h2>
      <div className="tweets">
        {tweets.map((tweet, index) => (
          <div className="tweet" key={index}>
            <div className="user-info">
              <span className="user-name">{tweet.user_name}</span>
              <span className="screen-name">@{tweet.screen_name}</span>
            </div>
            <p className="tweet-text">{tweet.text}</p>
            <p className="created-at">Created at: {new Date(tweet.created_at).toLocaleString()}</p>
          </div>
        ))}
        {prevPageUrl && <a className="prev btn" href={prevPageUrl}>Previous Page</a>}
        {nextPageUrl && <a className="next btn" href={nextPageUrl}>Next Page</a>}
      </div>
    </div>
  );
};

export default Home;

// {% extends 'base.html' %}

// {% block content %}
// <div class="centered-container">
//     <h2>Home Feed</h2>
//     <div class="tweets">
//         {% for tweet in tweets %}
//         <div class="tweet">
//             <div class="user-info">
//                 <span class="user-name">{{ tweet.user_name }}</span>
//                 <span class="screen-name">@{{ tweet.screen_name }}</span>
//             </div>
//             <p class="tweet-text">{{ tweet.text }}</p>
//             <p class="created-at">Created at: {{ tweet.created_at }}</p>
//         </div>
//         {% endfor %}

//         {% if prev_page_url %}
//         <a class="prev btn" href="{{ prev_page_url }}">Previous Page</a>
//         {% endif %}
//         {% if next_page_url %}
//         <a class="next btn" href="{{ next_page_url }}">Next Page</a>
//         {% endif %}

//     </div>
// </div>
// {% endblock %}
