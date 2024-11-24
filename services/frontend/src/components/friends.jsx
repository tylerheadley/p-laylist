import React, { useEffect, useState } from 'react';
import axios from 'axios';

const Friends = () => {
    const [tags, setTags] = useState([]);

    const API_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:1341';
    
    useEffect(() => {
        const fetchTrendingTags = async () => {
            try {
                const response = await axios.get(`${API_URL}/trending`);
                setTags(response.data.tags);
            } catch (error) {
                console.error('Error fetching trending tags:', error);
            }
        };
        fetchTrendingTags();
    }, []);

    return (
        <div className="centered-container">
            <h2>Trending Hashtags</h2>
            <table className="hashtag-table">
                <thead>
                    <tr>
                        <th>Rank</th>
                        <th>Hashtag</th>
                        <th>Count</th>
                    </tr>
                </thead>
                <tbody>
                    {tags.map((tag, index) => (
                        <tr key={index}>
                            <td><span className="rank">{tag.rank}</span></td>
                            <td><a className="hashtag-link" href={tag.url}>{tag.tag}</a></td>
                            <td>{tag.count}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
};

export default Friends;
