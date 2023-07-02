from db import db
from sqlalchemy.sql import text

def add_class(name, stat_adjustment, trauma_response, class_skills):
    sql = text("INSERT INTO class (name, stat_adjustment, trauma_response, class_skills) VALUES (:name,:stat_adjustment,:trauma_response,:class_skills)")
    db.session.execute(sql, {"name":name, "stat_adjustment":stat_adjustment, "trauma_response":trauma_response, "class_skills":class_skills})
    db.session.commit()

def get_all_classes():
    sql = text("SELECT id, name, stat_adjustment, trauma_response, class_skills FROM class ORDER BY name")
    return db.session.execute(sql).fetchall()

def get_class(class_id):
    sql = text("SELECT name FROM class WHERE id=:class_id")
    return db.session.execute(sql, {"class_id":class_id}).fetchone()
