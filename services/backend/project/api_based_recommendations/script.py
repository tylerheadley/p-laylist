from ytmusicapi import YTMusic
from dotenv import load_dotenv
import os

load_dotenv()
# Initialize YTMusic with OAuth credentials

from ytmusicapi import YTMusic, OAuthCredentials
client_id = os.getenv('YT_MUSIC_CLIENT')
client_secret = os.getenv('YT_MUSIC_KEY')
ytmusic = YTMusic('oauth.json', oauth_credentials=OAuthCredentials(client_id=client_id, client_secret=client_secret))

def get_song_recommendations(song_title, artist_name=None):
    # Construct search query
    query = f"{song_title} {artist_name}" if artist_name else song_title
    search_results = ytmusic.search(query, filter='songs', limit=1)

    if not search_results:
        print("Song not found.")
        return []
    print(search_results)

    # Get the videoId of the first matching song
    song_id = search_results[0]['videoId']
    

    # Retrieve related songs (You might also like)
    related_songs = ytmusic.get_watch_playlist(song_id)

    # print(related_songs)

    # Process the related songs to extract title and artists
    # recommendations = []
    # for track in related_songs.get('tracks', []):
    #     title = track.get('title', 'Unknown Title')
    #     # Each track may include a list of artists (each as a dict with a 'name' key)
    #     artists = track.get('artists', [])
    #     artist_names = ', '.join(artist.get('name', 'Unknown Artist') for artist in artists)
    #     recommendations.append(f"{title} by {artist_names}")
    
    return related_songs


if __name__ == "__main__":
    # Input parameters for the song
    song_title = "Shape of You"
    artist_name = "Ed Sheeran"  # Optional

    recs = get_song_recommendations(song_title, artist_name)
    if recs:
        print("You might also like:")
        for idx, rec in enumerate(recs, start=1):
            print(f"{idx}. {rec}")
    else:
        print("No recommendations found.")