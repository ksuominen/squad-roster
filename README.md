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

## Installation

Prerequisites: Python version `3.11.3`, virtualenv version `20.24.0`

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

4. Run the application:

```
flask run
```

## Known caveats

- User cannot change their password or delete their account
- Gamemaster can add characters to their campaign without players' approval
- Only character's name is shown in the select field when adding characters to a campaign (what if there are two characters of same name?)
- Class stat modifications are stored as text and aren't automatically taken into account when creating a character
