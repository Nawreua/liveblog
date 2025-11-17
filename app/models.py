from app import db

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(64))
    title = db.Column(db.String(250))
    content = db.Column(db.Text)
    date = db.Column(db.DateTime)