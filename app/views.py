"""
The main submodule, defining all Flask routes
"""

from flask import render_template, request

from app import app
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

@app.route("/save/", methods=['GET', 'POST'])
@require_auth
def save_post():
    """
    Save a requested post
    """
    return "<p>Test login</p>"
