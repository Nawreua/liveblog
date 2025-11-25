"""
The main submodule, defining all Flask routes
"""

from datetime import datetime

from flask import render_template, request

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

    Arguments:
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
    """
    post_data = request.json
    new_post = Post(
        author=post_data['author'],
        title=post_data['title'],
        content=post_data['content'],
        date=datetime.now())
    db.session.add(new_post)
    db.session.commit()
    return render_template('view.html', post=Post.query.get(new_post.id))