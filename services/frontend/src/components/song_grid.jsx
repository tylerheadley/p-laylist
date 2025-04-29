import Song from './song.jsx';
import React, { useState, useEffect } from 'react';
import { Grid2, Pagination } from '@mui/material';
import './song.css'

const SongGrid = ({songList}) => {
    const songsPerPage = 12;

    const [currentSongs, setCurrentSongs] = useState([]);
    const [totalPages, setTotalPages] = useState(0);

    const calculateCurrentSongs = (currentPage) => {
        const indexOfLastSong = currentPage * songsPerPage;
        const indexOfFirstSong = indexOfLastSong - songsPerPage;
        setCurrentSongs(songList.slice(indexOfFirstSong, indexOfLastSong));
    }

    useEffect(() => {
    if (songList) {
        calculateCurrentSongs(1);
        setTotalPages(Math.ceil(songList.length / songsPerPage));
    } }, [songList]);


    const handleChange = (event, value) => {
        calculateCurrentSongs(value);
      };

    
    return (
        console.log(currentSongs),
        <>
            <div className='total-container'>
               {currentSongs && currentSongs.length > 0 ?
                <div className='grid-container'>
                    <Grid2 
                    container spacing={2} 
                    columns={{ xs: 2, sm: 3, md: 12 }}
                    className='song-grid'>

                    {currentSongs.map((song) => (
                        (
                        <Grid2 item size={{xs: 12, sm: 6, md:4, lg:4}} key={song.id}>
                            <Song                            
                                song={song}
                            />
                        </Grid2>
                            // <Song                            
                            //     song={song}
                            // />
                        )
                    )) }
                    </Grid2>

                    <Pagination count={totalPages} onChange={handleChange} />
                </div>

                : 
                    <p>No Songs Found</p>
                
                }



            </div>
        </>
    )
}

export default SongGrid;