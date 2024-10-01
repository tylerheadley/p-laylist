# Twitter Replica

[![tests](https://github.com/tylerheadley/twitter-clone/actions/workflows/tests.yml/badge.svg)](https://github.com/tylerheadley/twitter-clone/actions/workflows/tests.yml)

## Overview {#overview}

Welcome to my Twitter Clone project! This project is an implementation of basic Twitter functionality using Instagram's architecture. The end result is a production ready web app that is fast and scalable.

## Table of Contents

1. [Overview](#overview)
2. [Technologies Used](#technologies-used)
3. [Features](#features)
    - [Project Structure](#project-structure)
    - [Database Design](#database-design)
    - [Routes and Functionality](#routes-and-functionality)
4. [Other Tasks Completed](#other-tasks-completed)
5. [Demo and Grading](#demo-and-grading)
6. [Recommended Timeline](#recommended-timeline)

## Technologies Used {#technologies-used}
 - Python: Used for backend development.
 - Flask: Micro web framework used for server-side logic.
 - HTML/CSS: Frontend design and styling.
 - Jinja2: Templating engine for rendering dynamic content.
 - PostgreSQL: Database management system.
 - Docker (+ Docker Compose): Containerization for development and production environments.
 - Nginx: High-performance web server and reverse proxy server.
 - Gunicorn: WSGI (Web Server Gateway Interface) HTTP server.
 - AWS EC2: Cloud computing and deployment.
 - GitHub Actions: Implemented for continuous integration.


## Build Instructions

**To bring up the services, follow these steps:**

First, clone this repository and navigate to the project directory.

To build and run the development containers:

```
$ docker-compose up -d --build
```
Access the Flask app at http://localhost:1341/.

To stop the containers:

```
$ docker-compose down -v
```

For production, use the docker-compose.prod.yml file instead. 
Note that you will need to add your own `.env.prod.db` text file containing your database credentials.

Build and run the production containers, and initialize the PostgreSQL database:

```
$ docker-compose -f docker-compose.prod.yml up -d --build
$ docker-compose -f docker-compose.prod.yml exec web python manage.py create_db
```

Access the production Flask app at http://localhost:1337/.


To stop the production containers:

```
$ docker-compose -f docker-compose.prod.yml down -v
```
