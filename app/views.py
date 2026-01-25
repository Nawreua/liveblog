"""
The main submodule, defining all Flask routes
"""

from datetime import datetime

from flask import render_template, request, abort, jsonify
from sqlalchemy import exc

from app import app, db
from app.models import Post
from app.auth import require_auth

def _no_accept_html(req):
    return req.headers['Accept'].find('text/html') == -1

@app.route("/")
def hello_world():
    """
    Display the main page
    """
    return "<p>Hello, World!</p>"

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
    if _no_accept_html(request):
        return jsonify(posts)
    return "<p>FIXME</p>"

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
    if _no_accept_html(request):
        return jsonify(post)
    return render_template('view.html', post=post)

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
    return render_template('view.html', post=Post.get_post(new_post.id))
