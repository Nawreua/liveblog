"""
A submodule for the database models
"""

import datetime
from dataclasses import dataclass

from sqlalchemy import asc, desc

from app import db

@dataclass
class Post(db.Model):
    """
    The main model of the database, containing user-made posts.

    Model columns:
    - author - String(64): the name of the author, required
    - title - String(250): the title of the post, required
    - content - Text: the main content of the post
    - date - DateTime: the date-time at which the post was made, required
    """
    id:int = db.Column(db.Integer, primary_key=True)
    author:str = db.Column(db.String(64), nullable=False)
    title:str = db.Column(db.String(250), nullable=False)
    content:str = db.Column(db.Text)
    date:datetime.datetime = db.Column(db.DateTime, nullable=False)

    def get_post(id):
        """
        Retrieve a post given an id
        """
        return Post.query.get_or_404(id)

    def get_latest_posts(limit):
        """
        Retrieve a list of posts, sorted
        by descending date-time with a
        limited size
        """
        return Post.query.order_by(desc(Post.date)).\
            limit(limit)

    def get_multiple_posts(offset, limit):
        """
        Retrieve list of posts, from an offset id,
        with a limited size
        """
        return Post.query.order_by(asc(Post.id)).\
            filter(Post.id > offset).limit(limit)
