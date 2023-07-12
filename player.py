from db import db
from flask import session, request, abort
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.sql import text

def username_taken(username):
    sql = text("SELECT id FROM player WHERE username=:username")
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    return True if user else False

def register(username, password):
    hash_value = generate_password_hash(password)
    try:
        sql = text("INSERT INTO player (username, password) VALUES (:username,:password)")
        db.session.execute(sql, {"username":username, "password":hash_value})
        db.session.commit()
    except Exception:
        return False
    return login(username, password)

def login(username, password):
    sql = text("SELECT id, username, password, is_admin FROM player WHERE username=:username")
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if not user:
        return False
    if check_password_hash(user.password, password):
        session["user_id"] = user.id
        session["user_name"] = user.username
        session["is_admin"] = user.is_admin
        return True
    return False
        
def logout():
    del session["user_id"]
    del session["user_name"]
    del session["is_admin"]
