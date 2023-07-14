from db import db
from sqlalchemy.sql import text

def add_item(name, description):
    sql = text("INSERT INTO item (name, description) VALUES (:name,:description)")
    db.session.execute(sql, {"name":name, "description":description})
    db.session.commit()

def edit_item(id, name, description):
    sql = text("UPDATE item SET name=:name, description=:description WHERE id=:id")
    db.session.execute(sql, {"id":id, "name":name, "description":description})
    db.session.commit()

def get_all_items():
    sql = text("SELECT id, name, description FROM item ORDER BY name")
    return db.session.execute(sql).fetchall()

def exists(name):
    sql = text("SELECT id FROM item WHERE name=:name")
    result = db.session.execute(sql, {"name":name}).fetchone()
    return True if result else False

def item_exists(item_id):
    sql = text("SELECT id FROM item WHERE id=:item_id")
    result = db.session.execute(sql, {"item_id":item_id}).fetchone()
    return True if result else False