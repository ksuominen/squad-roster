from db import db
from sqlalchemy.sql import text

def add_skill(name, description, level):
    sql = text("INSERT INTO skill (name, description, level) VALUES (:name,:description,:level)")
    db.session.execute(sql, {"name":name, "description":description, "level":level})
    db.session.commit()

def get_all_skills():
    sql = text("SELECT id, name, description, level FROM skill ORDER BY name")
    return db.session.execute(sql).fetchall()

def get_trained_skills():
    sql = text("SELECT id, name, description FROM skill WHERE LOWER(level) = 'trained'")
    return db.session.execute(sql).fetchall()

def get_expert_skills():
    sql = text("SELECT id, name, description FROM skill WHERE LOWER(level) = 'expert'")
    return db.session.execute(sql).fetchall()

def get_master_skills():
    sql = text("SELECT id, name, description FROM skill WHERE LOWER(level) = 'master'")
    return db.session.execute(sql).fetchall()