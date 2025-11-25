"""
The main submodule, defining all Flask routes
"""

from datetime import datetime

from flask import render_template, request, abort
from sqlalchemy import exc

from app import app, db
from app.models import Post
from app.auth import require_auth

@app.route("/")
def hello_world():
    """
    Display the main page
    """
    return "<p>Hello, World!</p>"

@app.route("/view/")
def view_all_posts():
    """
    Display all posts
    """
    return "<p>FIXME</p>"

@app.route("/view/<id>")
def view_post(id):
    """
    Display a given post

    Route arguments:
    - id: the id of the post 
    """
    return render_template('view.html', post=Post.query.get(id))

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
    post_data = request.json
    try:
        new_post = Post(
            author=post_data.get('author'),
            title=post_data.get('title'),
            content=post_data.get('content'),
            date=datetime.now())
        db.session.add(new_post)
        db.session.commit()
    except exc.IntegrityError:
        abort(422)
    return render_template('view.html', post=Post.query.get(new_post.id))