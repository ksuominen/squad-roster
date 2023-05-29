from db import db
from sqlalchemy.sql import text
from flask import session

def create_campaign(name, description):
    gamemaster_id = session["user_id"]
    sql = text("INSERT INTO campaign (name, description, gamemaster_id) VALUES (:name,:description,:gamemaster_id)")
    db.session.execute(sql, {"name":name, "description":description, "gamemaster_id":gamemaster_id})
    db.session.commit()

def get_all_gm_campaigns(player_name):
    sql = text("SELECT id FROM player WHERE username = :player_name")
    player_id = db.session.execute(sql, {"player_name":player_name}).fetchone()[0]
    sql = text("SELECT name, description FROM campaign WHERE gamemaster_id = :player_id")
    return db.session.execute(sql, {"player_id":player_id}).fetchall()

def get_all_campaigns():
    sql = text("SELECT name, description, username FROM campaign INNER JOIN player ON gamemaster_id = player.id")
    return db.session.execute(sql)
