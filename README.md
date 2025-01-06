# p-laylist

[![tests](https://github.com/tylerheadley/twitter-clone/actions/workflows/tests.yml/badge.svg)](https://github.com/tylerheadley/twitter-clone/actions/workflows/tests.yml)

## Table of Contents

1. [Overview](#overview)
2. [Tech Stack](#tech-stack)
3. [Data](#data)
4. [Features](#features)
5. [Schema](#schema)
6. [Build Instructions](#build-instructions)

## Overview 

Have you ever been frustrated with Spotify recommending the same songs repeatedly, even when your interests change? Or wished you could expand your music taste and fill in the gaps in your playlists? What about that friend with impeccable music taste whose playlists you can’t access because they use Apple Music? Our project tackles these issues by developing an AI-powered web app for collaborative music recommendations. 

Our platform will generate daily, personalized playlists by using a hybrid of collaborative filtering and content-based recommendation techniques. The core of our product is a recommendation engine that analyzes both user behavior and song characteristics. In addition, we plan to integrate social media-like features for collaborative music sharing, song reviews, and discussions, enhancing community interaction around music discovery.

On the technical side, our recommendation model will employ an ensemble approach. We’ll combine deep learning for music content analysis with traditional recommendation algorithms like matrix factorization or graph-based models for collaborative filtering. By tuning parameterized weights, users can receive diverse recommendations, such as music beyond their typical taste, emerging artists, or popular picks overall. Our ultimate goal is to offer a seamless, engaging experience, connecting users across various streaming platforms, and providing them with dynamic music recommendations based on their playlists and listening habits.

## Tech Stack 

 - Python: Used for backend development.
 - Flask: Micro web framework used for server-side logic.
 - HTML/CSS: Frontend design and styling.
 - Jinja2: Templating engine for rendering dynamic content.
 - PostgreSQL: Database management system.
 - Docker (+ Docker Compose): Containerization for development and production environments.
 - Nginx: High-performance web server and reverse proxy server.
 - Gunicorn: WSGI (Web Server Gateway Interface) HTTP server.
 - AWS EC2: Cloud computing and hosting.
 - GitHub Actions: Implemented for continuous integration.

## Data 

The database is initially seeded with data using a script after spinning up the containers. There are two options for the source of the data. The `data/` folder in this repo contains about 100,000 real tweets from January 1st-10th, 2021. If more data is desired, there is an option to instead insert randomly generated tweets. These tweets consist of 5-12 random english words, followed by 1-4 randomly generated hashtags. 

## Features 

This project seeks to replicate Twitter's core CRUD (Create Read Update Delete) functionaility. This project has 7 endpoints, each facilitating a different primary function:

**Home Page**
 - The home page displays all tweets in the system, along with the user that posted it and the date + time of creation.
 - The most recent 20 messages are displayed, with all older tweets available on subsequent pages.

**Create Account**
 - Displays a form for a user to enter their name, username, and password.
 - Checks whether the username is taken, and that the password confirmation matches
 - If valid, inserts the new user information to the `users` table.

**Login**
  - Checks that entered credentials are valid, and stores them using cookies to keep the user logged in.

**Logout**
 - Deletes the cookies containing the user's credentials.

**Create Message**
 - Inserts the message entered into the `tweets` table, and the message is made visible at the top of the homepage.

**Search**
 - Uses full text search to find and display relevant tweets.

**Trending**
 - Displays the top trending hashtags in the system.

## Schema 

To enable this desired functionality, I designed a simple schema, shown in this E-R diagram.

![schema E-R diagram](schema.png)

There is also a view not shown in the diagram called `tweet_tags_count` that precomputes the counts for each hashtag usage for quick access later.

## Build Instruction

**To bring up the services, follow these steps:**

First, clone this repository and navigate to the project directory.

To build and run the development containers:

```
$ docker-compose up -d --build
```

Access the Flask app at http://localhost:1341/.

To stop the containers:

```
$ docker-compose down
```

You may include the -v flag at the end of this command to delete the postgres volume.

For production, use the docker-compose.prod.yml file instead. 
The production environment includes a few differences from the development build. The most substantial difference is the use of Nginx and Gunicorn as a WSGI server.
Note that you will need to add your own `.env.prod.db` text file containing database credentials. My file has 3 environment variables, `POSTGRES_USER`,`POSTGRES_PASSWORD`, and `PGUSER`.

Build and run the production containers, and initialize the PostgreSQL database:

```
$ docker-compose -f docker-compose.prod.yml up -d --build
```

Access the production Flask app at http://localhost:80/.


To stop the production containers:

```
$ docker-compose -f docker-compose.prod.yml down -v
```

To add initial data to the Postgres database, you may use the `load_tweets_parallel.sh` script. The usage for this file is:

```
$ sh load_tweets_parallel.sh [DATA SOURCE (--local_tweets or --random_tweets)] [NUMBER OF TWEETS (positive integer value)]
```

The local tweets option has a maximum of 99,997 tweets.
