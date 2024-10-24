import React, { useState } from 'react';
import axios from 'axios';

function CreateTweet() {
  const [tweet, setTweet] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    axios.post('/api/create_message', { tweet })
      .then(response => {
        alert('Tweet created!');
      })
      .catch(error => {
        console.error('There was an error creating the tweet!', error);
      });
  };

  return (
    <form onSubmit={handleSubmit}>
      <textarea
        value={tweet}
        onChange={(e) => setTweet(e.target.value)}
        rows="10"
        placeholder="Enter your tweet here..."
      />
      <button type="submit">Send Tweet</button>
    </form>
  );
}

export default CreateTweet;
// <!-- {% extends 'base.html' %}

// {% block content %}
// <div class="centered-container">
//     <h2>Create Message</h2>
//     <form class="tweet-form" action="/create_message" method="POST">
//         <textarea rows="10" id="tweet" name="tweet" placeholder="Enter your tweet here..."></textarea>
//         <input type="submit" value="Send Tweet"> 
//     </form>
        
// </div>
// {% endblock %} -->
