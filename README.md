# Squadroster

This is database training project meant for storing information related to a [Mothership](https://www.mothershiprpg.com/) inspired role-playing game. The rules aren't exactly the same as in Mothership (for example new classes can be generated and characters have levels).

Application features include:

- The user can create a username and log in and out.
- Logged in user can create a new character and edit or delete their existing characters.
- Logged in user can add items or skills to their characters or remove them.
- Logged in user can create a new campaign where they are the gamemaster.
- Logged in user sees in their own page a list of their characters and of campaigns where they're the gamemaster.
- Gamemaster can add characters to their campaign or delete the campaign.
- Gamemaster can edit the characters in their campaign.
- Gamemaster and players with characters in the campaign can view the campaign.
- Gamemaster and character's player can remove the character from the campaign.
- Admin can create new items, skills, or classes or edit existing ones.

You can try it at [squad-roster.fly.dev](https://squad-roster.fly.dev/)

## Installation

Prerequisites: Python version `3.11.3`, virtualenv version `20.24.0`, [PostgreSQL](https://www.postgresql.org/download/) installed

1. In the project directory, create a new virtual environment:

```
virtualenv venv
```

2. Activate the virtual environment:

**Linux:**

```
source venv/bin/activate
```

**Windows:**

```
.\venv\Scripts\activate
```

3. Install requirements:

```
pip install -r requirements.txt
```

4. Rename .env.example as .env, set DATABASE_URL and SECRET_KEY as instructed

5. To create an admin, run the following commands in your virtual environment:

```
flask shell
import manage
manage.create_admin("username", "password")
quit()
```

If no username or password is provided, the default ones are used (defined in manage.py)

6. Run the application:

```
flask run
```

## Known caveats

- User cannot change their password or delete their account
- Gamemaster can add characters to their campaign without players' approval
- Only character's name is shown in the select field when adding characters to a campaign (what if there are two characters of same name?)
- Class stat modifications are stored as text and aren't automatically taken into account when creating a character
