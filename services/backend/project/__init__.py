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
import re
import datetime
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
# from services.backend.project.config import Config
from sqlalchemy.exc import IntegrityError
from sqlalchemy import create_engine, text
import sqlalchemy
import psycopg2
from sqlalchemy import create_engine,text
from werkzeug.utils import secure_filename
import hashlib
import requests
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
app.config.from_object("project.config.Config")
app.config['SECRET_KEY'] = 'a_secure_random_secret_key'
app.config['SESSION_COOKIE_HTTPONLY'] = False
app.config['SESSION_COOKIE_SECURE'] = False
db = SQLAlchemy(app)
db_url = "postgresql://postgres:pass@postgres:5432"
engine = create_engine(db_url, connect_args={'application_name': '__init__.py'})
SPOTIFY_CLIENT_ID =  app.config["SPOTIFY_CLIENT_ID"]
SPOTIFY_REDIRECT_URI = app.config["SPOTIFY_REDIRECT_URI"]
SPOTIFY_CLIENT_SECRET = app.config["SPOTIFY_CLIENT_SECRET"]


CORS(app, resources={r"/*": {"origins": "*"}})

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

def is_logged_in():
    """Verify if the current session is logged in and check Spotify link status."""
    username = session.get('username')  # Check if username is stored in session
    if not username:
        return False
    
    return check_spotify_linked(username)

def check_spotify_linked(username):
    """Check if a user has linked their Spotify account."""
    with engine.connect() as connection:
        result = connection.execute(
            text("SELECT spotify_access_token FROM users WHERE screen_name = :username"),
            {'username': username}
        ).fetchone()
    return result is not None and result[0] is not None

@app.route("/login", methods=['GET', 'POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    if are_credentials_good(username, password):
        session['username'] = username  # Store username in session instead of cookies
        return jsonify({"message": "Login successful!"}), 200
    else:
        return jsonify({"error": "Invalid credentials"}), 401

@app.route("/check_logged_in", methods=["GET"])
def check_logged_in():
    # API endpoint to check if the user is logged in and if Spotify is linked
    logged_in = is_logged_in()
    spotify_linked = False
    if logged_in:
        username = session.get('username')
        spotify_linked = check_spotify_linked(username)
    return jsonify({"loggedIn": logged_in, "spotifyLinked": spotify_linked})


@app.route("/logout")
def logout():
    session.clear()
    return redirect("http://localhost:1341/")


@app.route('/create_account', methods=['POST'])
def create_account():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password1')
    hashed_password = generate_password_hash(password)
    if data and data['password1'] == data['password2']:
        try:
            # Attempt to insert user data into the database
            with engine.connect() as connection:
                connection.execute(text(
                    "INSERT INTO users (name, screen_name, password) VALUES (:name, :username, :password)"
                ), {'name': username, 'username': username, 'password': hashed_password})
            
            # Store the username in the session after account creation
            session['username'] = username
            print("create acc", session.get('username'))
            print("username create", username)

            # Check if Spotify account is linked
            spotify_connected = check_spotify_linked(username)

            # Prepare the response and set cookies securely
            response = make_response(jsonify({'message': 'Account created successfully!'}), 201)
            # response.set_cookie('username', username, httponly=True, secure=False, samesite='Lax')
            
            # Redirect to link music if Spotify is not linked
            if not spotify_connected:
                response.headers['Location'] = url_for('link_music_app', spotify_connected='0')
            else:
                response.headers['Location'] = url_for('home')

            return response

        except IntegrityError:
            return jsonify({"error": "Username already exists"}), 400
        except Exception as e:
            print(f"Database error: {e}")
            return jsonify({"error": "Account creation failed"}), 400
    else:
        return jsonify({"error": "Passwords do not match"}), 400

@app.route('/link_music_app', methods=['GET'])
def link_music_app():
    spotify_connected = request.args.get('spotify_connected') == '1'
    # This route would render the front-end component, not necessary to add code here
    return jsonify({'spotify_connected': spotify_connected})


@app.route("/spotify_authorize")
def spotify_authorize():
    scopes = "user-read-private user-read-email"
    auth_url = (
        f"https://accounts.spotify.com/authorize?response_type=code"
        f"&client_id={SPOTIFY_CLIENT_ID}&scope={scopes}&redirect_uri={SPOTIFY_REDIRECT_URI}"
    )
    return redirect(auth_url)

@app.route("/spotify_callback")
def spotify_callback():
    code = request.args.get("code")
    if not code:
        return jsonify({"error": "Authorization failed"}), 400

    token_url = "https://accounts.spotify.com/api/token"
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": SPOTIFY_REDIRECT_URI,
        "client_id": SPOTIFY_CLIENT_ID,
        "client_secret": SPOTIFY_CLIENT_SECRET,
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    response = requests.post(token_url, data=data, headers=headers)
    if response.status_code == 200:
        tokens = response.json()
        access_token = tokens['access_token']
        refresh_token = tokens['refresh_token']
        
        username = session.get('username')  # Get username from session
        print("username", username)
        if not username:
            return redirect(url_for('login'))
        print(f"Username in callback: {username}")

        # Update tokens in the database
        with engine.connect() as connection:
            connection.execute(
                text("UPDATE users SET spotify_access_token = :access_token, spotify_refresh_token = :refresh_token WHERE screen_name = :username"),
                {"access_token": access_token, "refresh_token": refresh_token, "username": username}
            )

        return redirect(url_for('link_music_app', spotify_connected='1'))
    else:
        return jsonify({"error": "Failed to retrieve tokens"}), 400

@app.route("/create_message", methods=['GET', 'POST'])
def create_message():
    if is_logged_in() and request.form.get('tweet'):

        tweet_content = request.form.get('tweet')

        # Define the regular expression pattern for hashtags
        hashtag_pattern = r'\B#\w+'

        # Find all matches of the pattern in the text
        hashtags = list(set(re.findall(hashtag_pattern, tweet_content)))

        db_url = "postgresql://postgres:pass@postgres:5432"
        engine = sqlalchemy.create_engine(db_url, connect_args={
            'application_name': '__init__.py create_message()',
        })
        connection = engine.connect()

        username = request.cookies.get('username')

        current_time = datetime.datetime.utcnow()

        # index scan using idx_username_password
        result = connection.execute(text(
            "SELECT id_users, screen_name "
            "FROM users "
            "WHERE screen_name=:username "
        ), {'username': username})

        for row in result.fetchall():
            user_id = row[0]

        result = connection.execute(text(
            "SELECT last_value FROM tweets_id_tweets_seq "
        ))

        for row in result.fetchall():
            tweet_id = row[0]

        connection.execute(text(
            "INSERT INTO tweets (id_users, text, created_at, lang) "
            "VALUES (:id_users, :text, :created_at, 'en');"
        ), {'id_users': user_id, 'text': tweet_content, 'created_at': current_time})

        for hashtag in hashtags:
            connection.execute(text(
                "INSERT INTO tweet_tags (id_tweets, tag) "
                "VALUES (:id_tweets, :tag) "
            ), {'id_tweets': tweet_id, 'tag': hashtag})

        connection.commit()

        connection.close()

        return jsonify({"message": "Tweet created successfully!"}), 201

    return jsonify({"error": "User not logged in or invalid tweet"}), 400


@app.route("/search", methods=['GET', 'POST'])
def search():
    try:
        page = int(request.args.get('page', 1))  # Get the page number from the query parameter, default to 1
    except ValueError:
        page = 1
    per_page = 20  # Number of messages per page

    search_query = request.args.get('search_query')

    db_url = "postgresql://postgres:pass@postgres:5432"
    engine = sqlalchemy.create_engine(db_url, connect_args={
        'application_name': '__init__.py root()',
    })
    connection = engine.connect()

    # Calculate OFFSET based on the page number
    offset = max(0, (page - 1) * per_page)

    is_hashtag_search = request.args.get('hashtag_search')
    if is_hashtag_search == '1':
        result = connection.execute(text(
            "SELECT "
            "u.name, u.screen_name, "
            "ts_headline('english', t.text, plainto_tsquery(:search_query), 'StartSel=<span> StopSel=</span>') AS highlighted_text, "
            "t.created_at "
            "FROM tweets t "
            "JOIN users u USING (id_users) "
            "WHERE t.text ILIKE '%#' || :search_query || '%' "
            "LIMIT :per_page OFFSET :offset;"
        ), {'per_page': per_page, 'offset': offset, 'search_query': search_query})
    else:
        # Fetch the most recent 20 messages for the current page
        result = connection.execute(text(
            "SELECT "
            "u.name, u.screen_name, "
            "ts_headline('english', t.text, plainto_tsquery(:search_query), 'StartSel=<span> StopSel=</span>') AS highlighted_text, "
            "t.created_at, "
            "ts_rank(to_tsvector('english', t.text), plainto_tsquery(:search_query)) AS rank "
            "FROM tweets t "
            "JOIN users u USING (id_users) "
            "WHERE to_tsvector('english', t.text) @@ plainto_tsquery(:search_query) "
            "ORDER BY rank DESC "
            "LIMIT :per_page OFFSET :offset;"
        ), {'per_page': per_page, 'offset': offset, 'search_query': search_query})

    connection.close()

    rows = result.fetchall()

    tweets = []
    for row in rows:
        tweets.append({
            'user_name': row[0],
            'screen_name': row[1],
            'text': bleach.clean(row[2], tags=['p', 'br', 'a', 'b', 'span'], attributes={'a': ['href']}).replace("<span>", "<span class=highlight>"),
            'created_at': row[3]
        })

    # Check if there are more messages to display on next pages
    next_page_url = None
    if len(rows) == per_page:
        next_page_url = url_for('search', search_query=search_query, hashtag_search=is_hashtag_search, page=page + 1)

    prev_page_url = None
    if page > 1:
        prev_page_url = url_for('search', search_query=search_query, hashtag_search=is_hashtag_search, page=page - 1)

    return jsonify(tweets=tweets, next_page_url=next_page_url, prev_page_url=prev_page_url)

@app.route('/trending')
def trending():
    db_url = "postgresql://postgres:pass@postgres:5432"
    engine = sqlalchemy.create_engine(db_url, connect_args={
        'application_name': '__init__.py root()',
    })
    connection = engine.connect()

    result = connection.execute(text(
        "SELECT tag, count_tags "
        "FROM tweet_tags_counts "
        "ORDER BY count_tags DESC, tag "
        "LIMIT 20; "
    ))

    connection.close()

    rows = result.fetchall()

    tags = []
    i = 1
    for row in rows:
        tags.append({
            'tag': row[0],
            'count': row[1],
            'rank': i,
            'url': "/search?hashtag_search=1&search_query=" + row[0][1:]
        })
        i += 1

    return jsonify({
        'tags': [{
            'rank': tag.rank,
            'tag': tag.tag,
            'count': tag.count,
            'url': tag.url
        } for tag in tags]
    })