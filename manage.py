from db import db
from werkzeug.security import generate_password_hash
from sqlalchemy.sql import text
import player


def create_admin(username="Timppa", password="peruna"):
    if player.username_taken(username):
        print("Sorry, but the username is already in use. Please try another username!")
        return
    hash_value = generate_password_hash(password)
    try:
        sql = text(
            "INSERT INTO player (username, password, is_admin) VALUES (:username,:password,:is_admin)"
        )
        db.session.execute(
            sql, {"username": username, "password": hash_value, "is_admin": "t"}
        )
        db.session.commit()
        print("Admin created succesfully!")
    except Exception:
        print("An error occured")
        return False
