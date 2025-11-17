from flask import render_template

from app import app
from app.models import Post

"""
The main submodule, defining all Flask routes
"""

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
