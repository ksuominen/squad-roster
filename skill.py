from db import db
from sqlalchemy.sql import text

def add_skill(name, description, level):
    sql = text("INSERT INTO skill (name, description, level) VALUES (:name,:description,:level)")
    db.session.execute(sql, {"name":name, "description":description, "level":level})
    db.session.commit()

def edit_skill(id, name, description, level):
    sql = text("UPDATE skill SET name=:name, description=:description, level=:level WHERE id=:id")
    db.session.execute(sql, {"id":id, "name":name, "description":description, "level":level})
    db.session.commit()

def get_skill(skill_id):
    sql = text("SELECT * FROM skill WHERE id=:skill_id")
    return db.session.execute(sql, {"skill_id":skill_id}).fetchone()

def get_all_skills():
    sql = text("SELECT id, name, description, level FROM skill ORDER BY name")
    return db.session.execute(sql).fetchall()

def skill_exists(skill_id):
    sql = text("SELECT id FROM skill where id=:skill_id")
    result = db.session.execute(sql, {"skill_id":skill_id}).fetchone()
    return True if result else False

def get_trained_skills():
    sql = text("SELECT id, name, description FROM skill WHERE LOWER(level) = 'trained'")
    return db.session.execute(sql).fetchall()

def get_expert_skills():
    sql = text("SELECT id, name, description FROM skill WHERE LOWER(level) = 'expert'")
    return db.session.execute(sql).fetchall()

def get_master_skills():
    sql = text("SELECT id, name, description FROM skill WHERE LOWER(level) = 'master'")
    return db.session.execute(sql).fetchall()

def get_available_skills(character_id):
    sql = text("SELECT skill.id, skill.name FROM skill WHERE NOT EXISTS (SELECT 1 FROM character_skill WHERE character_id=:character_id AND skill.id=skill_id)")
    return db.session.execute(sql, {"character_id":character_id}).fetchall()