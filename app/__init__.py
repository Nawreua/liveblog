"""
A module implementing a live blogging application
"""

import logging
from argparse import ArgumentParser, Namespace

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

from app.configuration import Config
app.config.from_object(Config)

db = SQLAlchemy(app)
args = Namespace()

def parse_and_config():
    """
    Parse CLI arguments and configure the app

    The main purpose of this function is to allow
    the usage of pdoc for the application, since
    ArgumentParser can cause issues
    """
    parser = ArgumentParser(prog='liveblog',
                            description='A small sized blog')
    parser.add_argument('--debug', help='Launch the application in Debug Mode', action='store_true')
    parser.add_argument('--clean-database', help='Drop all the database and create it again', action='store_true')
    parser.add_argument('-l', '--log', help='Enable info log', action='store_true')
    args = parser.parse_args()

    if args.debug:
        from app.configuration import DebugConfig
        app.config.from_object(DebugConfig)

    if args.log:
        app.logger.setLevel(logging.INFO)

    if args.clean_database:
        from app.models import Post
        with app.app_context():
            db.drop_all()
            db.create_all()

            from datetime import datetime
            db.session.add(Post(author='Erwan', title='Test post', content='Un exemple de post', date=datetime.now()))
            db.session.commit()

            print(Post.query.all())


from app import views
