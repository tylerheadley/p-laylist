// Trending.js
import React, { useEffect, useState } from 'react';

const Trending = () => {
    const [tags, setTags] = useState([]);

    useEffect(() => {
        const fetchTrendingTags = async () => {
            const response = await fetch('/trending');
            const data = await response.json();
            setTags(data.tags);
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

export default Trending;

// {% extends 'base.html' %}

// {% block content %}
// <div class="centered-container">
//     <h2>Trending Hashtags</h2>
//     <table class="hashtag-table">
//         <thead>
//             <tr>
//                 <th>Rank</th>
//                 <th>Hashtag</th>
//                 <th>Count</th>
//             </tr>
//         </thead>
//         <tbody>
//             {% for tag in tags %}
//             <tr>
//                 <td><span class="rank">{{ tag.rank }}</span></td>
//                 <td><a class="hashtag-link" href="{{ tag.url }}">{{ tag.tag }}</a></td>
//                 <td>{{ tag.count }}</td>
//             </tr>
//             {% endfor %}
//         </tbody>
//     </table>
// </div>
// {% endblock %}
