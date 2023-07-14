CREATE TABLE player (
    id SERIAL PRIMARY KEY,
    username VARCHAR(30) UNIQUE NOT NULL,
    password TEXT NOT NULL,
    is_admin BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE TABLE class (
    id SERIAL PRIMARY KEY,
    name VARCHAR(30) NOT NULL,
    stat_adjustment TEXT NOT NULL,
    trauma_response TEXT NOT NULL,
    class_skills TEXT NOT NULL
);

CREATE TABLE character (
    id SERIAL PRIMARY KEY,
    name VARCHAR(30) NOT NULL,
    class_id INTEGER REFERENCES class NOT NULL,
    player_id INTEGER REFERENCES player NOT NULL,
    level INTEGER NOT NULL,
    strength INTEGER NOT NULL,
    speed INTEGER NOT NULL,
    intellect INTEGER NOT NULL,
    combat INTEGER NOT NULL,
    sanity INTEGER NOT NULL,
    fear INTEGER NOT NULL,
    body INTEGER NOT NULL,
    max_hp INTEGER NOT NULL,
    current_hp INTEGER NOT NULL,
    min_stress INTEGER NOT NULL,
    current_stress INTEGER NOT NULL,
    description TEXT,
    campaign_id INTEGER
);

CREATE TABLE skill (
    id SERIAL PRIMARY KEY,
    name VARCHAR(30) NOT NULL,
    description TEXT NOT NULL,
    level TEXT NOT NULL --integer/enum?
);

CREATE TABLE item (
    id SERIAL PRIMARY KEY,
    name VARCHAR(30) NOT NULL,
    description TEXT NOT NULL
);

CREATE TABLE campaign (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    gamemaster_id INTEGER REFERENCES player NOT NULL
);

CREATE TABLE character_item (
    id SERIAL PRIMARY KEY,
    character_id INTEGER REFERENCES character NOT NULL,
    item_id INTEGER REFERENCES item NOT NULL,
    amount INTEGER NOT NULL
);

CREATE TABLE character_skill (
    id SERIAL PRIMARY KEY,
    character_id INTEGER REFERENCES character NOT NULL,
    skill_id INTEGER REFERENCES skill NOT NULL
);
