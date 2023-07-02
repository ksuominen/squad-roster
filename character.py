from db import db
from sqlalchemy.sql import text
from flask import session

def create_character(name, class_id, level, strength, speed, intellect, combat, sanity, fear, body, max_hp, min_stress, description):
    player_id = session["user_id"]
    sql = text("INSERT INTO character (name, class_id, player_id, level, strength, speed, intellect, combat, sanity, fear, body, max_hp, current_hp, min_stress, current_stress, description) \
               VALUES (:name,:class_id,:player_id,:level,:strength,:speed,:intellect,:combat,:sanity,:fear,:body,:max_hp,:max_hp,:min_stress,:min_stress,:description)")
    db.session.execute(sql, {"name":name, "class_id":class_id, "player_id":player_id, "level":level, "strength":strength, "speed":speed,\
                              "intellect":intellect, "combat":combat, "sanity":sanity, "fear":fear, "body":body, "max_hp":max_hp, "current_hp":max_hp, \
                                "min_stress":min_stress, "current_stress":min_stress, "description":description})
    db.session.commit()

def get_player_characters():
    player_id = session["user_id"]
    sql = text("SELECT id, name FROM character WHERE player_id =:player_id")
    return db.session.execute(sql, {"player_id":player_id}).fetchall()

def add_skill(character_id, skill_id):
    sql = text("SELECT id, player_id FROM character WHERE id=:character_id")
    result = db.session.execute(sql, {"character_id":character_id})
    character = result.fetchone()
    sql = text("SELECT id FROM character WHERE id=:skill_id")
    result = db.session.execute(sql, {"skill_id":skill_id})
    skill = result.fetchone()
    if not skill or not character or session["user_id"] != character[1]:
        return False
    sql = text("INSERT INTO character_skill (character_id, skill_id) VALUES (:character_id,:skill_id)")
    db.session.execute(sql, {"character_id":character_id, "skill_id":skill_id})
    db.session.commit()
    return True

def get_character_info(character_id):
    sql = text("SELECT * FROM character WHERE id=:character_id")
    return db.session.execute(sql, {"character_id":character_id}).fetchone()