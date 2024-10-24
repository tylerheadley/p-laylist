// Search.js
import React, { useState, useEffect } from 'react';

const Search = () => {
    const [searchQuery, setSearchQuery] = useState('');
    const [tweets, setTweets] = useState([]);
    const [prevPageUrl, setPrevPageUrl] = useState(null);
    const [nextPageUrl, setNextPageUrl] = useState(null);

    const handleSearch = async (event) => {
        event.preventDefault();
        const response = await fetch(`/search?search_query=${searchQuery}`);
        const data = await response.json();
        setTweets(data.tweets);
        setPrevPageUrl(data.prev_page_url);
        setNextPageUrl(data.next_page_url);
    };

    return (
        <div className="centered-container">
            <h2>Search</h2>
            <form className="searchbar" onSubmit={handleSearch}>
                <input
                    type="text"
                    required
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    placeholder="Search Tweets"
                />
                <input type="submit" value="Search" />
            </form>
            <div className="tweets">
                {tweets.map((tweet, index) => (
                    <div key={index} className="tweet">
                        <div className="user-info">
                            <span className="user-name">{tweet.user_name}</span>
                            <span className="screen-name">@{tweet.screen_name}</span>
                        </div>
                        <p className="tweet-text" dangerouslySetInnerHTML={{ __html: tweet.text }}></p>
                        <p className="created-at">Created at: {tweet.created_at}</p>
                    </div>
                ))}

                {prevPageUrl && <a className="prev btn" href={prevPageUrl}>Previous Page</a>}
                {nextPageUrl && <a className="next btn" href={nextPageUrl}>Next Page</a>}
            </div>
        </div>
    );
};

export default Search;

// {% extends 'base.html' %}

// {% block content %}
// <div class="centered-container">
//     <h2>Search</h2>
//     <form class="searchbar" action="/search" method="GET">
//         <input type="text" required name="search_query" placeholder="Search Tweets">
//         <input type="submit" value="Search"> 
//     </form>
//     <div class="tweets">
//         {% for tweet in tweets %}
//         <div class="tweet">
//             <div class="user-info">
//                 <span class="user-name">{{ tweet.user_name }}</span>
//                 <span class="screen-name">@{{ tweet.screen_name }}</span>
//             </div>
//             <p class="tweet-text">{{ tweet.text | safe }}</p>
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
