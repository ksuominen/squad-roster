from wtforms import (
    Form,
    StringField,
    PasswordField,
    SelectField,
    IntegerField,
    SubmitField,
    validators,
)


class RegistrationForm(Form):
    username = StringField("Username", [validators.Length(min=4, max=25)])
    password = PasswordField(
        "Password",
        [
            validators.DataRequired(),
            validators.EqualTo("confirm", message="The passwords do not match."),
        ],
    )
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
    level = SelectField(
        "Skill level",
        choices=[("Trained", "Trained"), ("Expert", "Expert"), ("Master", "Master")],
    )


class CreateItemForm(Form):
    name = StringField("Name", [validators.Length(min=4, max=100)])
    description = StringField("Description", [validators.DataRequired()])


class CreateCampaignForm(Form):
    name = StringField("Name", [validators.Length(min=4, max=200)])
    description = StringField("Description")


class CreateCharacterForm(Form):
    name = StringField("Name", [validators.Length(min=4, max=50)])
    class_id = SelectField("Class", coerce=int, validators=[validators.InputRequired()])
    level = IntegerField(
        "Level (at least 1):",
        validators=[
            validators.NumberRange(min=1, message="Level needs to be at least 1")
        ],
    )
    strength = IntegerField(
        "Strength (1-100):",
        validators=[
            validators.NumberRange(
                min=1, max=100, message="Strength needs to be between 1 and 100"
            )
        ],
    )
    speed = IntegerField(
        "Speed (1-100):",
        validators=[
            validators.NumberRange(
                min=1, max=100, message="Speed needs to be between 1 and 100"
            )
        ],
    )
    intellect = IntegerField(
        "Intellect (1-100):",
        validators=[
            validators.NumberRange(
                min=1, max=100, message="Intellect needs to be between 1 and 100"
            )
        ],
    )
    combat = IntegerField(
        "Combat (1-100):",
        validators=[
            validators.NumberRange(
                min=1, max=100, message="Combat needs to be between 1 and 100"
            )
        ],
    )
    sanity = IntegerField(
        "Sanity (1-100):",
        validators=[
            validators.NumberRange(
                min=1, max=100, message="Sanity needs to be between 1 and 100"
            )
        ],
    )
    fear = IntegerField(
        "Fear (1-100):",
        validators=[
            validators.NumberRange(
                min=1, max=100, message="Fear needs to be between 1 and 100"
            )
        ],
    )
    body = IntegerField(
        "Body (1-100):",
        validators=[
            validators.NumberRange(
                min=1, max=100, message="Body needs to be between 1 and 100"
            )
        ],
    )
    max_hp = IntegerField(
        "Max hp (20-100):",
        validators=[
            validators.NumberRange(
                min=20, max=100, message="Max hp needs to be between 20 and 100"
            )
        ],
    )
    min_stress = IntegerField(
        "Min stress (2-20):",
        validators=[
            validators.NumberRange(
                min=2, max=20, message="Min stress needs to be between 2 and 20"
            )
        ],
    )
    description = StringField("Description")


class EditCharacterForm(Form):
    name = StringField("Name", [validators.Length(min=4, max=50)])
    class_id = SelectField("Class", coerce=int, validators=[validators.InputRequired()])
    level = IntegerField(
        "Level (at least 1):",
        validators=[
            validators.NumberRange(min=1, message="Level needs to be at least 1")
        ],
    )
    strength = IntegerField(
        "Strength (1-100):",
        validators=[
            validators.NumberRange(
                min=1, max=100, message="Strength needs to be between 1 and 100"
            )
        ],
    )
    speed = IntegerField(
        "Speed (1-100):",
        validators=[
            validators.NumberRange(
                min=1, max=100, message="Speed needs to be between 1 and 100"
            )
        ],
    )
    intellect = IntegerField(
        "Intellect (1-100):",
        validators=[
            validators.NumberRange(
                min=1, max=100, message="Intellect needs to be between 1 and 100"
            )
        ],
    )
    combat = IntegerField(
        "Combat (1-100):",
        validators=[
            validators.NumberRange(
                min=1, max=100, message="Combat needs to be between 1 and 100"
            )
        ],
    )
    sanity = IntegerField(
        "Sanity (1-100):",
        validators=[
            validators.NumberRange(
                min=1, max=100, message="Sanity needs to be between 1 and 100"
            )
        ],
    )
    fear = IntegerField(
        "Fear (1-100):",
        validators=[
            validators.NumberRange(
                min=1, max=100, message="Fear needs to be between 1 and 100"
            )
        ],
    )
    body = IntegerField(
        "Body (1-100):",
        validators=[
            validators.NumberRange(
                min=1, max=100, message="Body needs to be between 1 and 100"
            )
        ],
    )
    max_hp = IntegerField(
        "Max hp (20-100):",
        validators=[
            validators.NumberRange(
                min=20, max=100, message="Max hp needs to be between 20 and 100"
            )
        ],
    )
    current_hp = IntegerField(
        "Current hp:",
        validators=[
            validators.NumberRange(
                min=0, max=100, message="Current hp needs to be between 0 and max hp"
            )
        ],
    )
    min_stress = IntegerField(
        "Min stress (2-20):",
        validators=[
            validators.NumberRange(
                min=2, max=20, message="Min stress needs to be between 2 and 20"
            )
        ],
    )
    current_stress = IntegerField(
        "Current stress:",
        validators=[
            validators.NumberRange(
                min=2,
                max=20,
                message="Current stress needs to be between min stress and 20",
            )
        ],
    )
    description = StringField("Description")


class AddSkillToCharacterForm(Form):
    skill_id = SelectField("Skill", coerce=int, validators=[validators.InputRequired()])
    add_skill_submit = SubmitField("Add")


class AddItemToCharacterForm(Form):
    item_id = SelectField("Item", coerce=int, validators=[validators.InputRequired()])
    amount = IntegerField(
        "Amount (between 1 and 100):",
        validators=[
            validators.NumberRange(
                min=1, max=100, message="Amount needs to be between 1 and 100"
            )
        ],
    )
    add_item_submit = SubmitField("Add item")


class AddCharacterToCampaignForm(Form):
    character_id = SelectField(
        "Character", coerce=int, validators=[validators.InputRequired()]
    )
