import os
from flask import (
    Flask,
    jsonify,
    send_from_directory,
    request,
    render_template,
    url_for,
    make_response,
    redirect,
    session
)
import bleach
import json
import re
import datetime
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import create_engine, text
import sqlalchemy
import psycopg2
from sqlalchemy import create_engine,text
from werkzeug.utils import secure_filename
import hashlib
import requests
import jwt
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
app.config.from_object("project.config.Config")
app.config['SECRET_KEY'] = app.config["FLASK_SECRET_KEY"]
app.config['SESSION_COOKIE_HTTPONLY'] = False
app.config['SESSION_COOKIE_SECURE'] = False
app.config['SESSION_TYPE'] = 'filesystem'  # Use the filesystem to persist sessions
app.config['SESSION_PERMANENT'] = False   # Sessions are not permanent
app.config['SESSION_USE_SIGNER'] = True   # Sign cookies for extra security
Session(app)
db = SQLAlchemy(app)
db_url = "postgresql://postgres:pass@postgres:5432"
engine = create_engine(db_url, connect_args={'application_name': '__init__.py'})
SPOTIFY_CLIENT_ID =  app.config["SPOTIFY_CLIENT_ID"]
SPOTIFY_REDIRECT_URI = app.config["SPOTIFY_REDIRECT_URI"]
SPOTIFY_CLIENT_SECRET = app.config["SPOTIFY_CLIENT_SECRET"]


CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

@app.route("/api/tweets", methods=["GET"])
def root():
    try:
        page = int(request.args.get('page', 1))  # Get the page number from the query parameter, default to 1
    except ValueError:
        page = 1

    per_page = 20  # Number of messages per page

    connection = engine.connect()

    # Calculate OFFSET based on the page number
    offset = max(0, (page - 1) * per_page)

    # Fetch the most recent 20 messages for the current page
    result = connection.execute(text(
        "SELECT u.name, u.screen_name, t.text, t.created_at "
        "FROM tweets t "
        "JOIN users u USING (id_users) "
        "ORDER BY t.created_at DESC, u.screen_name "
        "LIMIT :per_page OFFSET :offset;"
    ), {'per_page': per_page, 'offset': offset})

    rows = result.fetchall()

    tweets = []
    for row in rows:
        tweets.append({
            'user_name': row[0],
            'screen_name': row[1],
            'text': row[2],
            'created_at': row[3]
        })

    # Check if there are more messages to display on the next pages
    next_page_url = None
    if len(rows) == per_page:
        next_page_url = url_for('root', page=page + 1, _external=True)

    prev_page_url = None
    if page > 1:
        prev_page_url = url_for('root', page=page - 1, _external=True)

    # Return JSON data instead of rendering HTML
    return jsonify({
        'tweets': tweets,
        'next_page_url': next_page_url,
        'prev_page_url': prev_page_url
    })


@app.route('/create_account', methods=['POST'])
def create_account():
    session.clear()
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid data"}), 400

    username = data.get('username')
    password1 = data.get('password1')
    password2 = data.get('password2')
    name = data.get('name')

    connection = engine.connect()
    result = connection.execute(
            text("SELECT id_users FROM users WHERE screen_name = :username"),
            {'username': username}
    ).fetchone()
    if result:
        return jsonify({"error": "Username already exists"}), 400

    # Log incoming data (except passwords for security)
    print(f"Received data: username={username}, name={name}")

    hashed_password = generate_password_hash(password1)
    
    user_data = {
        "username": username,
        "name": name,
        "hashed_password": hashed_password,
    }

    # Encode data in a JWT to pass to Spotify flow
    token = jwt.encode(user_data, app.config["SECRET_KEY"], algorithm="HS256")
    return jsonify({"redirect": f"http://localhost:1341/spotify_authorize?token={token}"}), 201


def get_spotify_tokens(auth_code):
    token_url = "https://accounts.spotify.com/api/token"
    data = {
        "grant_type": "authorization_code",
        "code": auth_code,
        "redirect_uri": SPOTIFY_REDIRECT_URI,
        "client_id": SPOTIFY_CLIENT_ID,
        "client_secret": SPOTIFY_CLIENT_SECRET,
    }
    response = requests.post(token_url, data=data)
    if response.status_code != 200:
        raise Exception("Spotify token request failed")
    return response.json()

@app.route("/spotify_callback")
def spotify_callback():
    state = request.args.get("state")  # Retrieve the token from the state parameter
    if not state:
        return jsonify({"error": "Missing token"}), 400

    try:
        user_data = jwt.decode(state, app.config["SECRET_KEY"], algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token expired"}), 400
    except jwt.InvalidTokenError:
        return jsonify({"error": "Invalid token"}), 400

    code = request.args.get("code")
    if not code:
        return jsonify({"error": "Authorization failed"}), 400

    # Request Spotify tokens...
    tokens = get_spotify_tokens(code)
    print("spotify tokens:", tokens)
    print("name:", user_data["name"])
    print("username:", user_data["username"])
    print("password:", user_data["hashed_password"])

    try:
        with engine.connect() as connection:
            result = connection.execute(
                text(
                    "INSERT INTO users (name, screen_name, password, spotify_access_token, spotify_refresh_token) "
                    "VALUES (:name, :username, :password, :access_token, :refresh_token)"
                ),
                {
                    "name": user_data["name"],
                    "username": user_data["username"],
                    "password": user_data["hashed_password"],
                    "access_token": tokens["access_token"],
                    "refresh_token": tokens["refresh_token"]
                }
            )
            print("Insert result:", result.rowcount)

            connection.commit()

            connection.close()
    except Exception as e:
        return jsonify({"error": "Database save error"}), 500
    

    return redirect("http://localhost:3000")


def are_credentials_good(username, password):
    query = "SELECT password FROM users WHERE screen_name = :username"
    try:
        with engine.connect() as connection:
            result = connection.execute(text(query), {'username': username}).fetchone()
            if result:
                stored_password = result[0]
                return check_password_hash(stored_password, password)
            return False
    except Exception as e:
        print(f"Database error: {e}")
        return False

@app.route("/login", methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    if are_credentials_good(username, password):
        session['username'] = username
        return jsonify({"message": "Login successful!"}), 200
    return jsonify({"error": "Invalid credentials"}), 401


def check_spotify_linked(username):
    """Check if a user has linked their Spotify account."""
    with engine.connect() as connection:
        result = connection.execute(
            text("SELECT spotify_access_token FROM users WHERE screen_name = :username"),
            {'username': username}
        ).fetchone()
    return result is not None and result[0] is not None

@app.route("/check_logged_in", methods=["GET"])
def check_logged_in():
    # API endpoint to check if the user is logged in and if Spotify is linked
    username = session.get('username')
    logged_in = False
    spotify_linked = False
    if username:
        logged_in = True
    if logged_in:
        spotify_linked = check_spotify_linked(username)
    return jsonify({"loggedIn": logged_in, "spotifyLinked": spotify_linked})


@app.route("/logout")
def logout():
    session.clear()
    return redirect("http://localhost:3000/")


@app.route('/link_music_app', methods=['GET'])
def link_music_app():
    spotify_connected = request.args.get('spotify_connected') == '1'
    # This route would render the front-end component, not necessary to add code here
    return jsonify({'spotify_connected': spotify_connected})



@app.route("/spotify_authorize")
def spotify_authorize():
    token = request.args.get("token")
    if not token:
        return jsonify({"error": "Missing token"}), 400

    scopes = "user-read-private user-read-email"
    auth_url = (
        f"https://accounts.spotify.com/authorize?response_type=code"
        f"&client_id={SPOTIFY_CLIENT_ID}&scope={scopes}&redirect_uri={SPOTIFY_REDIRECT_URI}"
        f"&state={token}"  # Include the token in the state parameter
    )
    return redirect(auth_url)



@app.route("/api/songs", methods=["GET"])
def song_data():
    
    try:
        # Define the path to your JSON file
        file_path = os.path.join(os.path.dirname(__file__), "test_song_data", "recommended_songs.json")
       
        # Open and read the JSON file
        with open(file_path, "r") as file:
            data = json.load(file)  # Parse the JSON data

        # Return the data as a JSON response
        return jsonify(data)
    
    except FileNotFoundError:
        return jsonify({"error": "File not found"}), 404
    except json.JSONDecodeError:
        return jsonify({"error": "Invalid JSON format"}), 500

if __name__ == "__main__":
    app.run(debug=True)

# @app.route("/create_message", methods=['GET', 'POST'])
# def create_message():
#     if request.form.get('tweet'):

#         tweet_content = request.form.get('tweet')

#         # Define the regular expression pattern for hashtags
#         hashtag_pattern = r'\B#\w+'

#         # Find all matches of the pattern in the text
#         hashtags = list(set(re.findall(hashtag_pattern, tweet_content)))

#         db_url = "postgresql://postgres:pass@postgres:5432"
#         engine = sqlalchemy.create_engine(db_url, connect_args={
#             'application_name': '__init__.py create_message()',
#         })
#         connection = engine.connect()

#         username = request.cookies.get('username')

#         current_time = datetime.datetime.utcnow()

#         # index scan using idx_username_password
#         result = connection.execute(text(
#             "SELECT id_users, screen_name "
#             "FROM users "
#             "WHERE screen_name=:username "
#         ), {'username': username})

#         for row in result.fetchall():
#             user_id = row[0]

#         result = connection.execute(text(
#             "SELECT last_value FROM tweets_id_tweets_seq "
#         ))

#         for row in result.fetchall():
#             tweet_id = row[0]

#         connection.execute(text(
#             "INSERT INTO tweets (id_users, text, created_at, lang) "
#             "VALUES (:id_users, :text, :created_at, 'en');"
#         ), {'id_users': user_id, 'text': tweet_content, 'created_at': current_time})

#         for hashtag in hashtags:
#             connection.execute(text(
#                 "INSERT INTO tweet_tags (id_tweets, tag) "
#                 "VALUES (:id_tweets, :tag) "
#             ), {'id_tweets': tweet_id, 'tag': hashtag})

#         connection.commit()

#         connection.close()

#         return jsonify({"message": "Tweet created successfully!"}), 201

#     return jsonify({"error": "User not logged in or invalid tweet"}), 400


# @app.route("/search", methods=['GET', 'POST'])
# def search():
#     try:
#         page = int(request.args.get('page', 1))  # Get the page number from the query parameter, default to 1
#     except ValueError:
#         page = 1
#     per_page = 20  # Number of messages per page

#     search_query = request.args.get('search_query')

#     db_url = "postgresql://postgres:pass@postgres:5432"
#     engine = sqlalchemy.create_engine(db_url, connect_args={
#         'application_name': '__init__.py root()',
#     })
#     connection = engine.connect()

#     # Calculate OFFSET based on the page number
#     offset = max(0, (page - 1) * per_page)

#     is_hashtag_search = request.args.get('hashtag_search')
#     if is_hashtag_search == '1':
#         result = connection.execute(text(
#             "SELECT "
#             "u.name, u.screen_name, "
#             "ts_headline('english', t.text, plainto_tsquery(:search_query), 'StartSel=<span> StopSel=</span>') AS highlighted_text, "
#             "t.created_at "
#             "FROM tweets t "
#             "JOIN users u USING (id_users) "
#             "WHERE t.text ILIKE '%#' || :search_query || '%' "
#             "LIMIT :per_page OFFSET :offset;"
#         ), {'per_page': per_page, 'offset': offset, 'search_query': search_query})
#     else:
#         # Fetch the most recent 20 messages for the current page
#         result = connection.execute(text(
#             "SELECT "
#             "u.name, u.screen_name, "
#             "ts_headline('english', t.text, plainto_tsquery(:search_query), 'StartSel=<span> StopSel=</span>') AS highlighted_text, "
#             "t.created_at, "
#             "ts_rank(to_tsvector('english', t.text), plainto_tsquery(:search_query)) AS rank "
#             "FROM tweets t "
#             "JOIN users u USING (id_users) "
#             "WHERE to_tsvector('english', t.text) @@ plainto_tsquery(:search_query) "
#             "ORDER BY rank DESC "
#             "LIMIT :per_page OFFSET :offset;"
#         ), {'per_page': per_page, 'offset': offset, 'search_query': search_query})

#     connection.close()

#     rows = result.fetchall()

#     tweets = []
#     for row in rows:
#         tweets.append({
#             'user_name': row[0],
#             'screen_name': row[1],
#             'text': bleach.clean(row[2], tags=['p', 'br', 'a', 'b', 'span'], attributes={'a': ['href']}).replace("<span>", "<span class=highlight>"),
#             'created_at': row[3]
#         })

#     # Check if there are more messages to display on next pages
#     next_page_url = None
#     if len(rows) == per_page:
#         next_page_url = url_for('search', search_query=search_query, hashtag_search=is_hashtag_search, page=page + 1)

#     prev_page_url = None
#     if page > 1:
#         prev_page_url = url_for('search', search_query=search_query, hashtag_search=is_hashtag_search, page=page - 1)

#     return jsonify(tweets=tweets, next_page_url=next_page_url, prev_page_url=prev_page_url)
