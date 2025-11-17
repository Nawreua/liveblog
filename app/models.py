from app import db

"""
A submodule for the database models
"""

class Post(db.Model):
    """
    The main model of the database, containing user-made posts.

    Model columns:
    - author - String(64): the name of the author
    - title - String(250): the title of the post
    - content - Text: the main content of the post
    - date - DateTime: the date-time at which the post was made
    """
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(64))
    title = db.Column(db.String(250))
    content = db.Column(db.Text)
    date = db.Column(db.DateTime)