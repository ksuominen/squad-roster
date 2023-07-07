from db import db
from sqlalchemy.sql import text
from flask import session
import character as c

def create_campaign(name, description):
    gamemaster_id = session["user_id"]
    sql = text("INSERT INTO campaign (name, description, gamemaster_id) VALUES (:name,:description,:gamemaster_id)")
    db.session.execute(sql, {"name":name, "description":description, "gamemaster_id":gamemaster_id})
    db.session.commit()

def get_all_gm_campaigns(player_name):
    sql = text("SELECT campaign.id, campaign.name, campaign.description FROM campaign INNER JOIN player ON campaign.gamemaster_id = player.id WHERE player.username = :player_name")
    return db.session.execute(sql, {"player_name":player_name}).fetchall()

def get_all_campaigns():
    sql = text("SELECT campaign.id, campaign.name, campaign.description, campaign.gamemaster_id, player.username FROM campaign INNER JOIN player ON gamemaster_id = player.id")
    return db.session.execute(sql).fetchall()

def get_campaign(campaign_id):
    sql = text("SELECT campaign.id, campaign.name, campaign.description, player.username FROM campaign INNER JOIN player ON campaign.gamemaster_id = player.id WHERE campaign.id = :campaign_id")
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

def is_player_in_campaign(player_id, campaign_id):
    sql = text("SELECT DISTINCT ON (campaign.id) campaign.id, campaign.gamemaster_id, character.id AS players_character_id FROM campaign INNER JOIN player ON campaign.gamemaster_id = player.id LEFT JOIN character ON campaign.id = character.campaign_id AND character.player_id = :player_id WHERE campaign.id = :campaign_id")
    result = db.session.execute(sql, {"player_id":player_id, "campaign_id":campaign_id}).fetchone()
    return True if result.gamemaster_id == player_id or result.players_character_id else False

def add_character_to_campaign(character_id, campaign_id):
    sql = text("UPDATE character SET campaign_id = :campaign_id WHERE id = :character_id")
    db.session.execute(sql, {"character_id":character_id, "campaign_id":campaign_id})
    db.session.commit()

def remove_character_from_campaign(character_id, campaign_id):
    characters_player_id = c.get_characters_player_id(character_id).player_id
    sql = text("SELECT gamemaster_if FROM campaign WHERE campaign_id =:campaign_id")
    campaign_gm_id = db.session.execute(sql, {"campaign_id":campaign_id}).fetchone()
    user_id = session.get("user_id")
    if not user_id: 
        return False
    if user_id == characters_player_id or user_id == campaign_gm_id:
        sql = text("UPDATE character SET campaign_id = NULL WHERE id = :character_id")
        db.session.execute(sql, {"character_id":character_id})
        db.session.commit()
        return True
