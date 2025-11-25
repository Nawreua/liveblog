"""
A submodule for the database models
"""

from app import db

class Post(db.Model):
    """
    The main model of the database, containing user-made posts.

    Model columns:
    - author - String(64): the name of the author, required
    - title - String(250): the title of the post, required
    - content - Text: the main content of the post
    - date - DateTime: the date-time at which the post was made, required
    """
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(64), nullable=False)
    title = db.Column(db.String(250), nullable=False)
    content = db.Column(db.Text)
    date = db.Column(db.DateTime, nullable=False)
