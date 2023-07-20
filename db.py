from app import app
from flask_sqlalchemy import SQLAlchemy
from os import getenv

app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
# Uncomment this when deploying to fly.io
# .replace(
#    "://", "ql://", 1
# )
db = SQLAlchemy(app)
