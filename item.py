from db import db
from sqlalchemy.sql import text

def add_item(name, description):
    sql = text("INSERT INTO item (name, description) VALUES (:name,:description)")
    db.session.execute(sql, {"name":name, "description":description})
    db.session.commit()

def get_all_items():
    sql = text("SELECT id, name, description FROM item ORDER BY name")
    return db.session.execute(sql).fetchall()