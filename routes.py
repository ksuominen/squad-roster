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
    user_id = session.get("user_id")
    if not user_id:
        return render_template("error.html", message="Sorry, you don't have access to this page.")
    
    characters = character.get_player_characters(user_id)
    gm_campaigns = campaign.get_all_gm_campaigns(user_id)
  
    return render_template("player.html", gm_campaigns = gm_campaigns, characters = characters)

@app.route("/items", methods=["GET"])
def items():
    items = item.get_all_items()
    return render_template("items.html", items=items)

@app.route("/item/add", methods=["GET", "POST"])
def add_item():
    form = f.CreateItemForm(request.form)
    if not session.get("is_admin"):
        return render_template("error.html", message="Only admins can create new items.")
    
    if request.method == "POST" and form.validate():
        if item.exists(form.name.data):
            return render_template("error.html", message="An item already exists with that name.")
        else:
            item.add_item(form.name.data, form.description.data)
            return redirect("/items")
    
    return render_template("item_add.html", form=form)

@app.route("/item/<int:item_id>/edit", methods=["GET", "POST"])
def edit_item(item_id):
    if not session.get("is_admin"):
        return render_template("error.html", message="Sorry, only admins can edit items.")
    
    form = f.CreateItemForm(request.form)
    if request.method =="POST" and form.validate():
        item.edit_item(item_id, form.name.data, form.description.data)
        return redirect(f"/items")
    
    editable_item = item.get_item(item_id)
    form.process(obj=editable_item)
    return render_template("item_edit.html", form=form, item_id=item_id)

@app.route("/skills", methods=["GET"])
def skills():
    trained_skills = skill.get_trained_skills()
    expert_skills = skill.get_expert_skills()
    master_skills = skill.get_master_skills()
    
    return render_template("skill.html", trained_skills=trained_skills, expert_skills=expert_skills, master_skills=master_skills)

@app.route("/skill/add", methods=["GET", "POST"])
def add_skill():
    form = f.CreateSkillForm(request.form)
    if not session.get("is_admin"):
        return render_template("error.html", message="Only admins can create new skills.")
    if request.method == "POST" and form.validate():
        skill.add_skill(form.name.data, form.description.data, form.level.data)
        return redirect("/skills")
    
    return render_template("skill_add.html", form=form)

@app.route("/skill/<int:skill_id>/edit", methods=["GET", "POST"])
def edit_skill(skill_id):
    if not session.get("is_admin"):
        return render_template("error.html", message="Sorry, only admins can edit skills.")
    
    form = f.CreateSkillForm(request.form)
    if request.method == "POST" and form.validate():
        skill.edit_skill(skill_id, form.name.data, form.description.data, form.level.data)
        return redirect(f"/skills")
    
    editable_skill = skill.get_skill(skill_id)
    form.process(obj=editable_skill)
    return render_template("skill_edit.html", form=form, skill_id=skill_id)
    
@app.route("/classes", methods=["GET", "POST"])
def classes():
    all_classes = mothershipClasses.get_all_classes()
    return render_template("classes.html", classes=all_classes)

@app.route("/class/add", methods=["GET", "POST"])
def add_class():
    form = f.CreateClassForm(request.form)
    if not session.get("is_admin"):
        return render_template("error.html", message="Only admins can create new classes.")
    if request.method == "POST" and form.validate():
        mothershipClasses.add_class(form.name.data, form.stat_adjustment.data, form.trauma_response.data, form.class_skills.data)
        return redirect("/classes")
    
    return render_template("class_add.html", form=form)

@app.route("/class/<int:class_id>/edit", methods=["GET", "POST"])
def edit_class(class_id):
    if not session.get("is_admin"):
        return render_template("error.html", message="Sorry, only admins can edit classes.")
    
    form = f.CreateClassForm(request.form)
    if request.method =="POST" and form.validate():
        mothershipClasses.edit_class(class_id, form.name.data, form.stat_adjustment.data, form.trauma_response.data, form.class_skills.data)
        return redirect(f"/classes")
    
    editable_class = mothershipClasses.get_class(class_id)
    form.process(obj=editable_class)
    return render_template("class_edit.html", form=form, class_id=class_id)
    
@app.route("/campaigns", methods=["GET"])
def campaigns():
    form = f.CreateCampaignForm(request.form)
    if session.get("user_name"):
        player_campaigns = campaign.get_all_campaigns_with_player(session.get("user_id"))
        return render_template("campaigns.html", form=form, campaigns = player_campaigns)
    
    all_campaigns = campaign.get_all_campaigns()
    return render_template("campaigns.html", form=form, campaigns = all_campaigns)

@app.route("/campaign/add", methods=["GET", "POST"])
def add_campaign():
    form = f.CreateCampaignForm(request.form)
    user_id = session.get("user_id")
    if not user_id:
        return render_template("error.html", message="You must be logged in to create a campaign.")
    if request.method =="POST" and form.validate():
        campaign.create_campaign(form.name.data, form.description.data, user_id)
        return redirect("/ownpage")
    return render_template("campaign_add.html", form=form)

@app.route("/campaign/<int:campaign_id>/edit", methods=["GET", "POST"])
def edit_campaign(campaign_id):
    user_id = session.get("user_id")
    if not user_id or not campaign.is_gm(user_id, campaign_id):
        return render_template("error.html", message="Sorry, only gamemaster can edit the campaign.")
    
    form = f.CreateCampaignForm(request.form)
    if request.method =="POST" and form.validate():
        campaign.edit_campaign(campaign_id, form.name.data, form.description.data)
        return redirect(f"/campaigns")
    
    editable_campaign = campaign.get_campaign(campaign_id)
    form.process(obj=editable_campaign)
    return render_template("campaign_edit.html", form=form, campaign_id=campaign_id)

@app.route("/campaign/<int:campaign_id>", methods=["GET", "POST"])
def show_campaign(campaign_id):
    campaign_info = campaign.get_campaign(campaign_id)
    user_id = session.get("user_id")
    if not campaign_info:
        return render_template("error.html", message="No such campaign found.")
    
    access_campaign = campaign.has_character_in_campaign(user_id, campaign_id) or campaign.is_gm(user_id, campaign_id)
    
    if not user_id or not access_campaign:
        return render_template("error.html", message="Only gamemaster and players can view this page.")
    
    characters = campaign.get_characters(campaign_id)
    form = f.AddCharacterToCampaignForm(request.form)
    available_characters = campaign.get_available_characters(campaign_id)
    character_list = [(i.id, i.name) for i in available_characters]
    form.character_id.choices = character_list
    is_gm = campaign.is_gm(user_id, campaign_id)
    if request.method == "POST" and is_gm and form.validate():
        campaign.add_character_to_campaign(form.character_id.data, campaign_id)
        characters = campaign.get_characters(campaign_id)
        available_characters = campaign.get_available_characters(campaign_id)
        character_list = [(i.id, i.name) for i in available_characters]
        form.character_id.choices = character_list
        return render_template("campaign.html", form=form, campaign=campaign_info, characters=characters, is_gm=is_gm)
    
    return render_template("campaign.html", form=form, campaign=campaign_info, characters=characters, is_gm=is_gm)

@app.route("/campaign/<int:campaign_id>/remove/<int:character_id>", methods=["POST"])
def remove_campaign_character(campaign_id, character_id):
    character_player_id = character.get_characters_player_id(character_id).player_id
    user_id = session.get("user_id")
    can_remove_character = user_id == character_player_id or campaign.is_gm(user_id, campaign_id)
    if not can_remove_character:
        return render_template("error.html", message="Only character's player or campaign's gamemaster can remove a character from a campaign.")
    campaign.remove_character_from_campaign(character_id)
    return redirect(f"/campaign/{campaign_id}")

@app.route("/campaign/<int:campaign_id>/delete", methods=["POST"])
def remove_campaign(campaign_id):
    user_id = session.get("user_id")
    if not campaign.is_gm(user_id, campaign_id):
        return render_template("error.html", message="Only the gamemaster can delete a campaign.")
    campaign.delete_campaign(campaign_id)
    return redirect("/ownpage")

@app.route("/character/<int:character_id>", methods=["GET", "POST"])
def show_character(character_id):
    character_info = character.get_character_info(character_id)
    if not character_info:
        return render_template("error.html", message="No such character found.")
    character_campaign = campaign.get_campaign(character_info.campaign_id)
    character_class = mothershipClasses.get_class(character_info.class_id)
    character_skills = character.get_character_skills(character_id)
    character_items = character.get_character_items(character_id)
    user_id = session.get("user_id")

    available_skills = skill.get_available_skills(character_id)
    skill_list = [(i.id, i.name) for i in available_skills]
    add_skill_form = f.AddSkillToCharacterForm(request.form)
    add_skill_form.skill_id.choices = skill_list
    if request.method =="POST" and add_skill_form.add_skill_submit.data and add_skill_form.validate():
        if character_info.player_id != user_id:
            return render_template("error.html", message="Only character's player can add skills to them.")
        if character.has_skill(character_info.id, add_skill_form.skill_id.data):
            return render_template("error.html", message="Character already has that skill!")
        character.add_skill(character_info.id, add_skill_form.skill_id.data)
        return redirect(f"/character/{character_info.id}")

        
    available_items = item.get_all_items()
    item_list = [(i.id, i.name) for i in available_items]
    add_item_form = f.AddItemToCharacterForm(request.form)
    add_item_form.item_id.choices = item_list
    if request.method =="POST" and add_item_form.add_item_submit.data and add_item_form.validate():
        if character_info.player_id != user_id:
            return render_template("error.html", message="Only character's player can add items to them.")
        character.add_item(character_info.id, add_item_form.item_id.data, add_item_form.amount.data)
        return redirect(f"/character/{character_info.id}")

    return render_template("character.html", character=character_info, add_skill_form=add_skill_form, add_item_form=add_item_form, character_class=character_class, character_campaign=character_campaign, skills=character_skills, items=character_items)

@app.route("/character/add", methods=["GET", "POST"])
def add_character():
    form = f.CreateCharacterForm(request.form)
    user_id = session.get("user_id")
    available_classes = mothershipClasses.get_all_classes()
    class_list=[(i.id, i.name) for i in available_classes]
    form.class_id.choices = class_list
    if not user_id:
        return render_template("error.html", message="You must be logged in to create a character.")
    if request.method =="POST" and form.validate():
        character.create_character(form.name.data, form.class_id.data, form.level.data, form.strength.data, form.speed.data, form.intellect.data, \
                                   form.combat.data, form.sanity.data, form.fear.data, form.body.data, form.max_hp.data, \
                                    form.min_stress.data, form.description.data, user_id)
        return redirect("/ownpage")  
    return render_template("character_add.html", form=form)

@app.route("/character/<int:character_id>/edit", methods=["GET", "POST"])
def edit_character(character_id):
    character_info = character.get_character_info(character_id)
    user_id = session.get("user_id")
    can_edit = user_id == character_info.player_id or campaign.is_gm(user_id, character_info.campaign_id)
    if not user_id or not can_edit:
        return render_template("error.html", message="Sorry, you don't have access to this page.")
    
    available_classes = mothershipClasses.get_all_classes()
    class_list=[(i.id, i.name) for i in available_classes]
    form = f.EditCharacterForm(request.form)
    form.name.default = character_info.name
    form.class_id.choices = class_list
    form.class_id.default = character_info.class_id
    if request.method =="POST" and form.validate():
        if form.current_hp.data > form.max_hp.data:
            return render_template("error.html", message="Current hp can't be more than max hp.")
        if form.current_stress.data < form.min_stress.data:
            return render_template("error.html", message="Current stress can't be less than min stress.")

        character.edit_character(character_id, form.name.data, form.class_id.data, form.level.data, form.strength.data, form.speed.data, form.intellect.data, \
                                   form.combat.data, form.sanity.data, form.fear.data, form.body.data, form.max_hp.data, form.current_hp.data, \
                                    form.min_stress.data, form.current_stress.data, form.description.data)
        return redirect(f"/character/{character_id}")
    
    form.process(obj=character_info)
    return render_template("character_edit.html", form=form, character_id = character_info.id, character_name = character_info.name)

@app.route("/character/<int:character_id>/skill/<int:skill_id>", methods=["POST"])
def delete_character_skill(character_id, skill_id):
    character_player_id = character.get_characters_player_id(character_id).player_id
    if session.get("user_id") != character_player_id:
        return render_template("error.html", message="Only character's player can delete skills from them.")
    character.delete_skill(character_id, skill_id)
    return redirect(f"/character/{character_id}")

@app.route("/character/<int:character_id>/item/<int:item_id>", methods=["POST"])
def delete_character_item(character_id, item_id):
    character_player_id = character.get_characters_player_id(character_id).player_id
    if session.get("user_id") != character_player_id:
        return render_template("error.html", message="Only character's player can use items from them.")
    amount = int(request.form["amount"])
    character.delete_item(character_id, item_id, amount)
    return redirect(f"/character/{character_id}")

@app.route("/character/<int:character_id>/delete", methods=["POST"])
def remove_character(character_id):
    character_player_id = character.get_characters_player_id(character_id).player_id
    if session.get("user_id") != character_player_id:
        return render_template("error.html", message="Only character's player delete them.")
    character.delete_character(character_id)
    return redirect("/ownpage")
