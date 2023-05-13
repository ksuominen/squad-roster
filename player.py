from db import db
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.sql import text

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
    sql = text("SELECT id, username, password FROM player WHERE username=:username")
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if not user:
        return False
    else:
        if check_password_hash(user.password, password):
            session["user_id"] = user.id
            session["user_name"] = user.username
            return True
        else:
            return False
        
def logout():
    del session["user_id"]
    del session["user_name"]