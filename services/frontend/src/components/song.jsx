import './song.css'
import {
    Card,
    
} from '@mui/material';
import {
    LinkOutlined
} from '@ant-design/icons'
const Song = ({song}) => {
    return (
        <>
            <Card
                variant="outlined"
                className='song-container'
            >
                <div className='song-info'>
                    <img className='album-image' src={song.album_cover}/>
                    <div>
                        <div className='song-title'>
                            <h3>{song.title}</h3>
                        </div>
                        <div className='song-artist'>
                            <h4>{song.artist}</h4>
                        </div>
                    </div>
                </div>
                
                <a href={song.url} target="_blank" ><LinkOutlined /></a>
                
            </Card>
        </>
    )
}

export default Song;