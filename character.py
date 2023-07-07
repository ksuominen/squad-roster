from db import db
from sqlalchemy.sql import text
from flask import session

def create_character(name, class_id, level, strength, speed, intellect, combat, sanity, fear, body, max_hp, min_stress, description):
    player_id = session.get("user_id")
    sql = text("INSERT INTO character (name, class_id, player_id, level, strength, speed, intellect, combat, sanity, fear, body, max_hp, current_hp, min_stress, current_stress, description) \
               VALUES (:name,:class_id,:player_id,:level,:strength,:speed,:intellect,:combat,:sanity,:fear,:body,:max_hp,:max_hp,:min_stress,:min_stress,:description)")
    db.session.execute(sql, {"name":name, "class_id":class_id, "player_id":player_id, "level":level, "strength":strength, "speed":speed,\
                              "intellect":intellect, "combat":combat, "sanity":sanity, "fear":fear, "body":body, "max_hp":max_hp, "current_hp":max_hp, \
                                "min_stress":min_stress, "current_stress":min_stress, "description":description})
    db.session.commit()

def get_player_characters():
    player_id = session.get("user_id")
    sql = text("SELECT id, name FROM character WHERE player_id =:player_id")
    return db.session.execute(sql, {"player_id":player_id}).fetchall()

def get_character_info(character_id):
    sql = text("SELECT * FROM character WHERE id=:character_id")
    return db.session.execute(sql, {"character_id":character_id}).fetchone()

def get_characters_player_id(character_id):
    sql = text("SELECT id, player_id FROM character WHERE id=:character_id")
    return db.session.execute(sql, {"character_id":character_id}).fetchone()

def add_skill(character_id, skill_id):
    character = get_characters_player_id(character_id)
    sql = text("SELECT id FROM skill WHERE id=:skill_id")
    skill = db.session.execute(sql, {"skill_id":skill_id}).fetchone()
    if not skill or not character or session.get("user_id") != character.player_id or has_skill(character_id, skill_id):
        return False
    sql = text("INSERT INTO character_skill (character_id, skill_id) VALUES (:character_id,:skill_id)")
    db.session.execute(sql, {"character_id":character_id, "skill_id":skill_id})
    db.session.commit()
    return True

def get_character_skills(character_id):
    sql = text("SELECT name, description, level FROM skill INNER JOIN character_skill ON skill_id = skill.id WHERE character_id=:character_id")
    return db.session.execute(sql, {"character_id":character_id}).fetchall()

def has_skill(character_id, skill_id):
    sql = text("SELECT id FROM character_skill WHERE character_id=:character_id AND skill_id=:skill_id")
    return db.session.execute(sql, {"character_id":character_id, "skill_id":skill_id}).fetchone()

def delete_skill(character_id, skill_id):
    character = get_characters_player_id(character_id)
    has_skill = has_skill(character_id, skill_id)
    if not has_skill or session.get("user_id") != character.player_id:
        return False
    sql = text("DELETE FROM character_skill WHERE character_id=:character_id AND skill_id=:skill_id")
    db.session.execute(sql, {"character_id":character_id, "skill_id":skill_id})
    db.session.commit()
    return True

def add_item(character_id, item_id, amount):
    character = get_characters_player_id(character_id)
    sql = text("SELECT id FROM item WHERE id=:item_id")
    item = db.session.execute(sql, {"item_id":item_id}).fetchone()
    if not item or not character or session.get("user_id") != character.player_id:
        return False
    item_exists = has_item(character_id, item_id)
    if item_exists:
        new_amount = item_exists.amount + amount
        sql = text("UPDATE character_item SET amount = :new_amount WHERE id=:id")
        db.session.execute(sql, {"new_amount":new_amount, "id":item_exists.id})
        db.session.commit()
        return True

    sql = text("INSERT INTO character_item (character_id, item_id, amount) VALUES (:character_id,:item_id,:amount)")
    db.session.execute(sql, {"character_id":character_id, "item_id":item_id, "amount":amount})
    db.session.commit()
    return True

def delete_item(character_id, item_id, amount):
    character = get_characters_player_id(character_id)
    has_item = has_item(character_id, item_id)
    if not has_item or session.get("user_id") != character.player_id:
        return False
    if amount > 1:
        new_amount = amount -1
        sql = text("UPDATE character_item SET amount = :new_amount where character_id = :character_id AND item_id = :item_id")
        db.session.execute(sql, {"new_amount":new_amount, "character_id":character_id, "item_id":item_id})
        db.session.commit()
        return True
    sql = text("DELETE FROM character_item where character_id = :character_id AND item_id = :item_id")
    db.session.execute(sql, {"character_id":character_id, "item_id":item_id})
    db.session.commit()
    return True

def get_character_items(character_id):
    sql = text("SELECT name, description, amount FROM item INNER JOIN character_item ON item_id = item.id WHERE character_id=:character_id")
    return db.session.execute(sql, {"character_id":character_id}).fetchall()

def has_item(character_id, item_id):
    sql = text("SELECT id, amount FROM character_item WHERE character_id=:character_id AND item_id=:item_id")
    return db.session.execute(sql, {"character_id":character_id, "item_id":item_id}).fetchone()

def get_all_characters():
    sql = text("SELECT id, name FROM character")
    return db.session.execute(sql).fetchall()