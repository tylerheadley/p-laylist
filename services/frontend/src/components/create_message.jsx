import React, { useState } from 'react';
import axios from 'axios';

function CreateTweet() {
  const [tweet, setTweet] = useState('');
  const API_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:1341'; // Use environment variable

  const handleSubmit = (e) => {
    e.preventDefault();
    axios.post(`${API_URL}/api/create_message`, { tweet }) // Updated to use API_URL
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
