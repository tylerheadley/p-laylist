import os
from flask import (
    Flask,
    jsonify,
    send_from_directory,
    request,
    render_template,
    url_for,
    make_response,
    redirect
)
import bleach
import re
import datetime
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from sqlalchemy import text
import sqlalchemy
import psycopg2
from sqlalchemy import create_engine,text
from werkzeug.utils import secure_filename
from flask import jsonify, request
import hashlib 

app = Flask(__name__)
app.config.from_object("project.config.Config")
db = SQLAlchemy(app)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route("/api/tweets", methods=["GET"])
def root():
    try:
        page = int(request.args.get('page', 1))  # Get the page number from the query parameter, default to 1
    except ValueError:
        page = 1

    per_page = 20  # Number of messages per page

    db_url = "postgresql://postgres:pass@postgres:5432"
    engine = sqlalchemy.create_engine(db_url, connect_args={
        'application_name': '__init__.py root()',
    })
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
    """Checks if the provided username and password match a user in the database."""
    hashed_password = hashlib.sha256(password.encode()).hexdigest()  # Hashing for security
    query = """
        SELECT screen_name 
        FROM users 
        WHERE screen_name = :username AND password = :password
    """

    try:
        with engine.connect() as connection:
            result = connection.execute(
                text(query), {'username': username, 'password': hashed_password}
            ).fetchone()
            return result is not None
    except Exception as e:
        print(f"Database error: {e}")
        return False

def is_logged_in():
    """Verifies if the current session is logged in based on cookies."""
    username = request.cookies.get('username')
    password = request.cookies.get('password')
    
    if not username or not password:
        return False

    return are_credentials_good(username, password)

@app.route("/check_logged_in", methods=["GET"])
def check_logged_in():
    """API endpoint to check if the user is logged in."""
    logged_in = is_logged_in()
    return jsonify({"loggedIn": logged_in})


@app.route("/login", methods=['GET', 'POST'])
def login():

    username = request.form.get('username')
    password = request.form.get('password')

    login_default = False
    if not username and not password:
        login_default = True

    good_credentials = are_credentials_good(username, password)

    if good_credentials:
        response = make_response(redirect(url_for('root')))
        response.set_cookie('username', username)
        response.set_cookie('password', password)
        return jsonify({"message": "Login successful!"}), 200
    else:
        return jsonify({"error": "Invalid credentials"}), 401


@app.route("/logout")
def logout():
    response = jsonify({'message': 'Logged out successfully'})

    response.set_cookie('username', '', expires=0)
    response.set_cookie('password', '', expires=0)

    return response

@app.route("/create_account", methods=['POST'])
def create_account():
    data = request.json  # Expecting JSON data from React

    # Default states
    username_exists = False
    passwords_different = False

    if data and data['password1'] == data['password2']:
        try:
            # Database connection
            db_url = "postgresql://postgres:pass@postgres:5432"
            engine = create_engine(db_url, connect_args={
                'application_name': '__init__.py create_account()',
            })
            connection = engine.connect()

            # Insert user into database
            connection.execute(text(
                "INSERT INTO users (name, screen_name, password) "
                "VALUES (:name, :username, :password1);"
            ), data)

            connection.commit()
            connection.close()

            # Create response with cookie (username and password)
            response = make_response(jsonify({"message": "Account created successfully!"}), 201)
            response.set_cookie('username', data['username'])
            response.set_cookie('password', data['password1'])

            return response

        except IntegrityError as e:
            # Handle case where username already exists
            print("Error inserting user:", e)
            username_exists = True
            return jsonify({"error": "Username already exists"}), 400

    elif data:
        # Passwords don't match
        passwords_different = True
        return jsonify({"error": "Passwords do not match"}), 400

    return jsonify({"error": "Invalid input"}), 400

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
    # return jsonify({
    #     'tweets': [{
    #         'user_name': tweet.user_name,
    #         'screen_name': tweet.screen_name,
    #         'text': tweet.text,
    #         'created_at': tweet.created_at
    #     } for tweet in tweets],
    #     'next_page_url': next_page_url,
    #     'prev_page_url': prev_page_url
    # })

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

"""How to get id of the user here???"""
def get_friends(id_user):
    db_url = "postgresql://postgres:pass@postgres:5432"
    engine = sqlalchemy.create_engine(db_url, connect_args={
        'application_name': '__init__.py root()',
    })
    connection = engine.connect()

    query = """
    SELECT f.id_friend, u.name, u.screen_name, u.recordmmendations
    FROM friends f
    JOIN user u ON f.id_friend = u.id_user
    WHERE f.id_user = :user_id
    """

    result = connection.execute(text(query), {'user_id': id_user})
    friends = result.fetchall()

    connection.close()

    friendsData = []
    for friend in friends:
        friendInfo = {
            'id_friend': friend[0],
            'screen_name': friend[1],
            'recordmmendations': friend[3]
        }

        friendsData.append(friendInfo)
    
    return jsonify(friendsData)

# @app.route("/static/<path:filename>")
# def staticfiles(filename):
#     return send_from_directory(app.config["STATIC_FOLDER"], filename)
#
#
# @app.route("/media/<path:filename>")
# def mediafiles(filename):
#     return send_from_directory(app.config["MEDIA_FOLDER"], filename)
#
#
# @app.route("/upload", methods=["GET", "POST"])
# def upload_file():
#     if request.method == "POST":
#         file = request.files["file"]
#         filename = secure_filename(file.filename)
#         file.save(os.path.join(app.config["MEDIA_FOLDER"], filename))
#     return """
#     <!doctype html>
#     <title>upload new File</title>
#     <form action="" method=post enctype=multipart/form-data>
#       <p><input type=file name=file><input type=submit value=Upload>
#     </form>
#     """
