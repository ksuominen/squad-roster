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
    username = session.get("user_name")
    if not username:
        return render_template("error.html", message="Sorry, you don't have access to this page.")
    
    characters = character.get_player_characters()
    available_classes = mothershipClasses.get_all_classes()
    class_list=[(i.id, i.name) for i in available_classes]
    campaign_form = f.CreateCampaignForm(request.form)
    character_form = f.CreateCharacterForm(request.form)
    character_form.class_id.choices = class_list
    gm_campaigns = campaign.get_all_gm_campaigns(username)
    
    if request.method =="POST" and campaign_form.campaign_submit.data and campaign_form.validate():
        campaign.create_campaign(campaign_form.name.data, campaign_form.description.data)
        return redirect("/ownpage")
    if request.method =="POST" and character_form.character_submit.data and character_form.validate():
        character.create_character(character_form.name.data, character_form.class_id.data, character_form.level.data, character_form.strength.data, character_form.speed.data, character_form.intellect.data, \
                                   character_form.combat.data, character_form.sanity.data, character_form.fear.data, character_form.body.data, character_form.max_hp.data, \
                                    character_form.min_stress.data, character_form.description.data)
        return redirect("/ownpage")    
    return render_template("player.html", campaign_form=campaign_form, character_form=character_form, gm_campaigns = gm_campaigns, characters = characters)

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

    available_skills = skill.get_available_skills(character_id)
    skill_list = [(i.id, i.name) for i in available_skills]
    add_skill_form = f.AddSkillToCharacterForm(request.form)
    add_skill_form.skill_id.choices = skill_list
    if request.method =="POST" and add_skill_form.add_skill_submit.data and add_skill_form.validate():
        if character.add_skill(character_info.id, add_skill_form.skill_id.data):
            return redirect(f"/character/{character_info.id}")
        else:
            return render_template("error.html", message="Could not add skill.")
        
    available_items = item.get_all_items()
    item_list = [(i.id, i.name) for i in available_items]
    add_item_form = f.AddItemToCharacterForm(request.form)
    add_item_form.item_id.choices = item_list
    if request.method =="POST" and add_item_form.add_item_submit.data and add_item_form.validate():
        if character.add_item(character_info.id, add_item_form.item_id.data, add_item_form.amount.data):
            return redirect(f"/character/{character_info.id}")
        else:
            return render_template("error.html", message="Could not add item.")

    return render_template("character.html", character=character_info, add_skill_form=add_skill_form, add_item_form=add_item_form, character_class=character_class, character_campaign=character_campaign, skills=character_skills, items=character_items)

@app.route("/character/<int:character_id>/edit", methods=["GET", "POST"])
def edit_character(character_id):
    character_info = character.get_character_info(character_id)
    user_id = session.get("user_id")
    #todo: gm can edit character
    if not user_id or user_id != character_info.player_id:
        return render_template("error.html", message="Sorry, you don't have access to this page.")
    
    available_classes = mothershipClasses.get_all_classes()
    class_list=[(i.id, i.name) for i in available_classes]
    form = f.EditCharacterForm(request.form)
    form.name.default = character_info.name
    form.class_id.choices = class_list
    form.class_id.default = character_info.class_id
    if request.method =="POST" and form.validate():
        character.edit_character(character_id, form.name.data, form.class_id.data, form.level.data, form.strength.data, form.speed.data, form.intellect.data, \
                                   form.combat.data, form.sanity.data, form.fear.data, form.body.data, form.max_hp.data, form.current_hp.data, \
                                    form.min_stress.data, form.current_stress.data, form.description.data)
        return redirect(f"/character/{character_id}")
    
    return render_template("edit_character.html", form=form, character_id = character_info.id, character_name = character_info.name)

@app.route("/character/<int:character_id>/skill/<int:skill_id>", methods=["POST"])
#todo: can we use delete?
def delete_character_skill(character_id, skill_id):
    character.delete_skill(character_id, skill_id)
    return redirect(f"/character/{character_id}")

@app.route("/character/<int:character_id>/item/<int:item_id>", methods=["POST"])
#todo: can we use delete?
def delete_character_item(character_id, item_id):
    amount = int(request.form["amount"])
    character.delete_item(character_id, item_id, amount)
    return redirect(f"/character/{character_id}")

@app.route("/campaign/<int:campaign_id>", methods=["GET", "POST"])
def show_campaign(campaign_id):
    campaign_info = campaign.get_campaign(campaign_id)
    if not campaign_info:
        return render_template("error.html", message="No such campaign found.")
    
    if not session.get("user_name") or not campaign.is_player_in_campaign(session.get("user_id"), campaign_id):
        return render_template("error.html", message="Only gamemaster and players can view this page.")
    
    characters = campaign.get_characters(campaign_id)
    form = f.AddCharacterToCampaignForm(request.form)
    all_characters = character.get_all_characters()
    character_list = [(i.id, i.name) for i in all_characters]
    form.character_id.choices = character_list
    if request.method == "POST" and session.get("user_name") == campaign_info.username and form.validate():
        campaign.add_character_to_campaign(form.character_id.data, campaign_id)
        characters = campaign.get_characters(campaign_id)
        return render_template("campaign.html", form=form, campaign=campaign_info, characters=characters)
    
    return render_template("campaign.html", form=form, campaign=campaign_info, characters=characters)
