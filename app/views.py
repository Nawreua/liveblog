"""
The main submodule, defining all Flask routes
"""

from datetime import datetime

from flask import render_template, request, abort, jsonify
from sqlalchemy import exc

from app import app, db
from app.models import Post
from app.auth import require_auth

def return_html(accept_header: str):
    """
    Check if the Accept header requires an HTML before any
    JSON requirement

    Since the API is JSON first, we need to ensure that we
    return HMTL result only if needed and explicitly asked
    """
    html_type_accept = sorted(
        filter(lambda x: x != -1,
               [accept_header.find('text/html'),
                accept_header.find('.html'),
                accept_header.find('.htm')
                ]
    ))
    html_accept = -1 if len(html_type_accept) == 0 else html_type_accept[0]

    json_type_accept = sorted(
        filter(lambda x: x != -1,
               [accept_header.find('application/json'),
                accept_header.find('.json')
                ]
    ))
    json_accept = -1 if len(json_type_accept) == 0 else json_type_accept[0]

    return html_accept != -1 and json_accept == -1 or html_accept != -1 and html_accept < json_accept

@app.route("/")
def hello_world():
    """
    Display the latest posts

    URL parameters:
    - limit: number of posts to load, by default 5
    """
    if return_html(request.headers['Accept']):
        return "<p>Hello, World!</p>"
    app.logger.info('/ route requested')
    limit = request.args.get('limit', 5)
    app.logger.debug(f'With limit {limit}')
    app.logger.info('Fetch posts')
    posts = Post.get_latest_posts(limit).all()
    app.logger.debug(posts)
    return jsonify(posts)

@app.route("/view/")
def view_all_posts():
    """
    Display multiple posts, by default all, with buffering

    URL parameters:
    - limit: number of posts to load, by default 25
    - offset: id of the first post to load from
    """
    app.logger.info('/view/ route requested')
    offset = request.args.get('offset', 0)
    app.logger.debug(f'With offset {offset}')
    limit = request.args.get('limit', 25)
    app.logger.debug(f'With limit {limit}')
    app.logger.info('Fetch posts')
    posts = Post.get_multiple_posts(offset, limit).all()
    app.logger.debug(posts)
    return jsonify(posts)

@app.route("/view/<id>")
def view_post(id):
    """
    Display a given post

    Route arguments:
    - id: the id of the post 
    """
    app.logger.info('/view/<id> requested')
    app.logger.debug(f'With id {id}')
    app.logger.info('Fetch post')
    post = Post.get_post(id)
    app.logger.debug(post)
    if post is None:
        abort(404)
    if return_html(request.headers['Accept']):
        return render_template('view.html', post=post)
    return jsonify(post)

@app.get("/save/")
def get_post_form():
    """
    Display the post creation page
    """
    return "<p>Test login</p>"

@app.post("/save/")
@require_auth
def save_post_form():
    """
    Save a requested post

    Request content:
    - Post data, as a JSON
    - Authentification data
    """
    app.logger.info('/save/ requested')
    post_data = request.json
    app.logger.debug(f'With data {post_data}')
    try:
        new_post = Post(
            author=post_data.get('author'),
            title=post_data.get('title'),
            content=post_data.get('content'),
            date=datetime.now())
        app.logger.info('Add new post')
        app.logger.debug(new_post)
        db.session.add(new_post)
        db.session.commit()
    except exc.IntegrityError:
        app.logger.error('New post creation failed')
        abort(422)
    if return_html(request.headers['Accept']):
        return render_template('view.html', post=Post.get_post(new_post.id))
    return jsonify(new_post)
