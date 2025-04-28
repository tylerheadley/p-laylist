from ytmusicapi import YTMusic
from dotenv import load_dotenv
import os

load_dotenv()
# Initialize YTMusic with OAuth credentials

from ytmusicapi import YTMusic, OAuthCredentials
client_id = os.getenv('YT_CLIENT_ID')
client_secret = os.getenv('YT_CLIENT_SECRET')

ytmusic = YTMusic('services/backend/project/api_based_recommendations/oauth.json', oauth_credentials=OAuthCredentials(client_id=client_id, client_secret=client_secret))

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