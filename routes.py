from app import app
from flask import render_template, request, redirect, session
import player
import item
import skill
import mothershipClasses
import campaign
import character
import formValidators as f

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    form = f.LoginForm(request.form)

    if request.method == "POST" and form.validate():
        if player.login(form.username.data, form.password.data):
            return redirect("/ownpage")
        else:
            return render_template("error.html", message="Wrong username or password.")
    
    return render_template("login.html", form=form)

@app.route("/register", methods=["GET", "POST"])
def register():
    form = f.RegistrationForm(request.form)
    if request.method == "POST" and form.validate():
        if player.username_taken(form.username.data):
            return render_template("error.html", message="Sorry, but the username is already in use. Please try another username!")
        if player.register(form.username.data, form.password.data):
            return redirect("/ownpage")
        else:
            return render_template("error.html", message="Registration failed.")
    
    return render_template("register.html", form=form)
        
@app.route("/logout")
def logout():
    player.logout()
    return redirect("/")

@app.route("/ownpage", methods=["GET", "POST"])
def ownpage():
    if not session.get("user_name"):
        return render_template("error.html", message="Sorry, you don't have access to this page.")
    
    characters = character.get_player_characters()
    character_list = [(i.id, i.name) for i in characters]
    available_classes = mothershipClasses.get_all_classes()
    class_list=[(i.id, i.name) for i in available_classes]
    available_skills = skill.get_all_skills()
    skill_list = [(i.id, i.name) for i in available_skills]
    available_items = item.get_all_items()
    item_list = [(i.id, i.name) for i in available_items]
    campaign_form = f.CreateCampaignForm(request.form)
    character_form = f.CreateCharacterForm(request.form)
    character_form.class_id.choices = class_list
    add_skill_form = f.AddSkillToCharacterForm(request.form)
    add_skill_form.character_id.choices = character_list
    add_skill_form.skill_id.choices = skill_list
    add_item_form = f.AddItemToCharacterForm(request.form)
    add_item_form.character_id.choices = character_list
    add_item_form.item_id.choices = item_list
    gm_campaigns = campaign.get_all_gm_campaigns(session["user_name"])
    
    if request.method =="POST" and campaign_form.campaign_submit.data and campaign_form.validate():
        campaign.create_campaign(campaign_form.name.data, campaign_form.description.data)
        return redirect("/ownpage")
    if request.method =="POST" and character_form.character_submit.data and character_form.validate():
        character.create_character(character_form.name.data, character_form.class_id.data, character_form.level.data, character_form.strength.data, character_form.speed.data, character_form.intellect.data, \
                                   character_form.combat.data, character_form.sanity.data, character_form.fear.data, character_form.body.data, character_form.max_hp.data, \
                                    character_form.min_stress.data, character_form.description.data)
        return redirect("/ownpage")
    if request.method =="POST" and add_skill_form.add_skill_submit.data and add_skill_form.validate():
        if character.add_skill(add_skill_form.character_id.data, add_skill_form.skill_id.data):
            return redirect("/ownpage")
        else:
            return render_template("error.html", message="Could not add skill.")
        
    if request.method =="POST" and add_item_form.add_item_submit.data and add_item_form.validate():
        if character.add_item(add_item_form.character_id.data, add_item_form.item_id.data, add_item_form.amount.data):
            return redirect("/ownpage")
        else:
            return render_template("error.html", message="Could not add item.")
    
    return render_template("player.html", campaign_form=campaign_form, character_form=character_form, add_skill_form = add_skill_form, add_item_form = add_item_form, gm_campaigns = gm_campaigns, characters = characters)

@app.route("/items", methods=["GET", "POST"])
def items():
    form = f.CreateItemForm(request.form)
    items = item.get_all_items()

    if request.method == "POST" and form.validate() and session.get("is_admin"):
        if item.exists(form.name.data):
            return render_template("error.html", message="An item already exists with that name.")
        else:
            item.add_item(form.name.data, form.description.data)
            return redirect("/items")

    return render_template("items.html", form=form, items=items)

@app.route("/skills", methods=["GET", "POST"])
def skills():
    form = f.CreateSkillForm(request.form)
    trained_skills = skill.get_trained_skills()
    expert_skills = skill.get_expert_skills()
    master_skills = skill.get_master_skills()

    if request.method == "POST" and form.validate() and session.get("is_admin"):
        skill.add_skill(form.name.data, form.description.data, form.level.data)
        return redirect("/skills")
    
    return render_template("skill.html", form=form, trained_skills=trained_skills, expert_skills=expert_skills, master_skills=master_skills)
    
@app.route("/classes", methods=["GET", "POST"])
def classes():
    all_classes = mothershipClasses.get_all_classes()
    form = f.CreateClassForm(request.form)

    if request.method == "POST" and form.validate() and session.get("is_admin"):
        mothershipClasses.add_class(form.name.data, form.stat_adjustment.data, form.trauma_response.data, form.class_skills.data)
        return redirect("/classes")

    return render_template("classes.html", form=form, classes=all_classes)
    
@app.route("/campaigns", methods=["GET"])
def campaigns():
    form = f.CreateCampaignForm(request.form)
    if session.get("user_name"):
        player_campaigns = campaign.get_all_campaigns_with_playerinfo(session.get("user_id"))
        return render_template("campaigns.html", form=form, campaigns = player_campaigns)
    
    all_campaigns = campaign.get_all_campaigns()
    return render_template("campaigns.html", form=form, campaigns = all_campaigns)

@app.route("/character/<int:character_id>", methods=["GET", "POST"])
def show_character(character_id):
    character_info = character.get_character_info(character_id)
    if not character_info:
        return render_template("error.html", message="No such character found.")
    character_campaign = campaign.get_campaign(character_info.campaign_id)
    character_class = mothershipClasses.get_class(character_info.class_id)
    character_skills = character.get_character_skills(character_id)
    character_items = character.get_character_items(character_id)
    return render_template("character.html", character=character_info, character_class=character_class, character_campaign=character_campaign, skills=character_skills, items=character_items)

@app.route("/campaign/<int:campaign_id>", methods=["GET"])
def show_campaign(campaign_id):
    campaign_info = campaign.get_campaign(campaign_id)
    if not campaign_info:
        return render_template("error.html", message="No such campaign found.")
    characters = campaign.get_characters(campaign_id)
    return render_template("campaign.html", campaign=campaign_info, characters=characters)
