from wtforms import Form, StringField, PasswordField, SelectField, IntegerField, SubmitField, validators
import mothershipClasses as mc

class RegistrationForm(Form):
    username = StringField("Username", [validators.Length(min=4, max=25)])
    password = PasswordField("Password", [
        validators.DataRequired(),
        validators.EqualTo("confirm", message="The passwords do not match.")
    ])
    confirm = PasswordField("Repeat Password")

class LoginForm(Form):
    username = StringField("Username", [validators.Length(min=4, max=25)])
    password = PasswordField("Password", [validators.DataRequired()])

class CreateClassForm(Form):
    name = StringField("Name", [validators.Length(min=4, max=50)])
    stat_adjustment = StringField("Stat adjustments", [validators.DataRequired()])
    trauma_response = StringField("Trauma response", [validators.DataRequired()])
    class_skills = StringField("Class skills", [validators.DataRequired()])

class CreateSkillForm(Form):
    name = StringField("Name", [validators.Length(min=4, max=100)])
    description = StringField("Description", [validators.DataRequired()])
    level = SelectField("Skill level", choices=[("Trained", "Trained"), ("Expert", "Expert"), ("Master", "Master")])

class CreateItemForm(Form):
    name = StringField("Name", [validators.Length(min=4, max=100)])
    description = StringField("Description", [validators.DataRequired()])

class CreateCampaignForm(Form):
    name = StringField("Name", [validators.Length(min=4, max=200)])
    description = StringField("Description")
    campaign_submit = SubmitField("Add new")

class CreateCharacterForm(Form):
    name = StringField("Name", [validators.Length(min=4, max=50)])
    class_id = SelectField("Class", coerce=int, validators=[validators.InputRequired()])
    level = IntegerField("Level (at least 1):", validators=[validators.NumberRange(min=1, message="Invalid length")])
    strength = IntegerField("Strength (between 1 and 100):", validators=[validators.NumberRange(min=1, max=100, message="Invalid length")])
    speed = IntegerField("Speed (between 1 and 100):", validators=[validators.NumberRange(min=1, max=100, message="Invalid length")])
    intellect = IntegerField("Intellect (between 1 and 100):", validators=[validators.NumberRange(min=1, max=100, message="Invalid length")])
    combat = IntegerField("Combat (between 1 and 100):", validators=[validators.NumberRange(min=1, max=100, message="Invalid length")])
    sanity = IntegerField("Sanity (between 1 and 100):", validators=[validators.NumberRange(min=1, max=100, message="Invalid length")])
    fear = IntegerField("Fear (between 1 and 100):", validators=[validators.NumberRange(min=1, max=100, message="Invalid length")])
    body = IntegerField("Body (between 1 and 100):", validators=[validators.NumberRange(min=1, max=100, message="Invalid length")])
    max_hp = IntegerField("Max hp (between 20 and 100):", validators=[validators.NumberRange(min=20, max=100, message="Invalid length")])
    min_stress = IntegerField("Min stress (between 2 and 100):", validators=[validators.NumberRange(min=2, max=100, message="Invalid length")])
    description = StringField("Description")
    character_submit = SubmitField("Add new")

class AddSkillToCharacterForm(Form):
    character_id = SelectField("Character", coerce=int, validators=[validators.InputRequired()])
    skill_id = SelectField("Skill", coerce=int, validators=[validators.InputRequired()])
    add_skill_submit = SubmitField("Add a new skill to character")