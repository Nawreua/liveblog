from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

from app.configuration import DebugConfig
app.config.from_object(DebugConfig)

db = SQLAlchemy(app)

from app import views