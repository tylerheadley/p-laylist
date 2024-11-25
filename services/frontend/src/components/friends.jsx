import React, { useEffect, useState } from 'react';
import axios from 'axios';

const Friends = () => {
    const [tags, setTags] = useState([]);

    const API_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:1341';
    
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
    }, []);

    return (
        <div className="centered-container">
            <h2>Friends</h2>
        </div>
    );
};

export default Friends;
