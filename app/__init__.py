from argparse import ArgumentParser

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

parser = ArgumentParser(prog='liveblog',
                        description='A small sized blog')
parser.add_argument('--debug', help='Launch the application in Debug Mode', action='store_true')
args = parser.parse_args()

if args.debug:
    from app.configuration import DebugConfig
    app.config.from_object(DebugConfig)
else:
    from app.configuration import Config
    app.config.from_object(Config)

db = SQLAlchemy(app)

if args.debug:
    from app.models import Post
    with app.app_context():
        db.drop_all()
        db.create_all()

        db.session.add(Post(author='Erwan', title='Test post', content='Un exemple de post'))
        db.session.commit()

        print(Post.query.all())

from app import views