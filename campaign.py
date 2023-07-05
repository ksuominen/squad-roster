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
    sql = text("SELECT campaign.id, campaign.name, campaign.description, campaign.gamemaster_id, player.username FROM campaign INNER JOIN player ON gamemaster_id = player.id")
    return db.session.execute(sql).fetchall()

def get_campaign(campaign_id):
    sql = text("SELECT campaign.name, campaign.description, player.username FROM campaign INNER JOIN player ON campaign.gamemaster_id = player.id WHERE campaign.id = :campaign_id")
    return db.session.execute(sql, {"campaign_id":campaign_id}).fetchone()  

def get_player_campaigns(player_id):
    sql = text("SELECT campaign.id FROM campaign INNER JOIN character ON campaign.id = campaign_id INNER JOIN player ON player_id = player.id WHERE player.id = :player_id")
    return db.session.execute(sql, {"player_id":player_id}).fetchall()

def get_all_campaigns_with_playerinfo(player_id):
    sql = text("SELECT DISTINCT ON (campaign.id) campaign.id, campaign.name, campaign.description, campaign.gamemaster_id, player.username, character.id AS players_character_id FROM campaign INNER JOIN player ON campaign.gamemaster_id = player.id LEFT JOIN character ON campaign.id = character.campaign_id AND character.player_id = :player_id")
    return db.session.execute(sql, {"player_id":player_id}).fetchall()

def get_characters(campaign_id):
    sql = text("SELECT character.id, character.name, character.level, class.name as class_name FROM character INNER JOIN campaign ON character.campaign_id = campaign.id INNER JOIN class on character.class_id = class.id WHERE campaign.id = :campaign_id")
    return db.session.execute(sql, {"campaign_id":campaign_id}).fetchall()