PRAGMA foreign_keys = ON;

CREATE TABLE users (
	user_id INTEGER PRIMARY KEY,
	username VARCHAR(20) NOT NULL,
	email VARCHAR(40) NOT NULL,
	password VARCHAR(256) NOT NULL,
	pfp_filename VARCHAR(64),
);

CREATE TABLE campaigns (
	campaign_id INTEGER PRIMARY KEY,
	map VARCHAR(64) NOT NULL,

);
	
CREATE TABLE campaign_players (
	campaign_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL, 
    PRIMARY KEY(campaign_id, user_id)
    FOREIGN KEY(campaign_id) REFERENCES Campaigns(campaign_id) ON DELETE CASCADE,
	FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
	is_gm INTEGER NOT NULL,
);
	

CREATE TABLE npcs (
	npc_id INTEGER PRIMARY KEY AUTOINCREMENT,
	campaign_id INTEGER,
	npc_name VARCHAR(60),
	npc_art VARCHAR(64),
	character_sheet VARCHAR(64),
    FOREIGN KEY(campaign_id) REFERENCES Campaigns(campaign_id) ON DELETE CASCADE,
);

CREATE TABLE characters (
    character_id INTEGER PRIMARY KEY AUTOINCREMENT,
	npc_name VARCHAR(60),
	npc_art VARCHAR(64),
	character_sheet VARCHAR(64),
);

