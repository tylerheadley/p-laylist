import React, { useEffect, useState } from 'react';
import axios from 'axios';
import Button from '@mui/material/Button';
import './friends.css'

const Friends = () => {
    const [tags, setTags] = useState([]);
    const [friendList, setFriendList] = useState([]);

    const API_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:1341';
    
    const fetchFriends = async() => {
        try {
          const response = await fetch('http://localhost:1341/api/friend');
          console.log('Fetch Response:', response);
          if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
          }
    
          const data = await response.json();
          setFriendList(data.friends); // Update state
          
    
        } catch(error) {
            console.error('Error fetching songs:', error);
          };
      };

    useEffect(() => {
        const fetchFriendsTags = async () => {
            try {
                const response = await axios.get(`${API_URL}/friends`);
                setTags(response.data.tags);
            } catch (error) {
                console.error('Error fetching friends:', error);
            }
        };
        fetchFriendsTags();
        fetchFriends();
    }, []);
      
    return (
        <div className='friend-home-page'>
            <div className='title-section'>
                <h2 className='title'>Friends</h2>
                <p className='subheading'>Discover new friends</p>
            </div>
        <div className= 'friend-container'>
            {friendList.length > 0 ? (

                friendList.map((friend, index) => (
                <div className="friend" key={index}>
                    <img src='placeholder-icon.png' className='profile-picture'/>
                    <div className="friend-info">
                    <h3 className="friend-name">{friend.name}</h3>
                    <p className="friend-inf">@{friend.username} · <em>{friend.recordmendations} Recordmendations</em> </p>
                    </div>
                    <div className='listening-to'>
                        <p className="friend-inf">Listening to... </p>
                        <p>{friend.recent_songs}</p>
                    </div>
                    <Button variant="contained"  id='follow-button'>Follow</Button>
                    
                </div>
                ))
            ) : (
                <p>No friends available.</p>
            )}
            </div>
          </div>
    );
};

export default Friends;
