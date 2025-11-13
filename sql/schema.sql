PRAGMA foreign_keys = ON;

CREATE TABLE Users (
	username VARCHAR(20) PRIMARY KEY,
	email VARCHAR(40) NOT NULL,
	password VARCHAR(256) NOT NULL,
	pfp_filename VARCHAR(64)
);

CREATE TABLE Pages (
	page_id INTEGER PRIMARY KEY,
	page_title VARCHAR(64) NOT NULL,
	owner_username VARCHAR(20) NOT NULL,
	FOREIGN KEY (owner_username) REFERENCES Users(username) ON DELETE CASCADE

);

CREATE TABLE Campaigns (
	campaign_id INTEGER PRIMARY KEY,
	owner_username VARCHAR(20) NOT NULL,
	page_id INTEGER NOT NULL,
	created DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
	FOREIGN KEY (page_id) REFERENCES Pages(page_id) ON DELETE CASCADE

);

CREATE TABLE CampaignPlayers (
	campaign_id INTEGER NOT NULL,
    username VARCHAR(20) NOT NULL, 
	character_id INTEGER,
    PRIMARY KEY(campaign_id, username)
    FOREIGN KEY(campaign_id) REFERENCES Campaigns(campaign_id) ON DELETE CASCADE,
	FOREIGN KEY (username) REFERENCES Users(username) ON DELETE CASCADE
	FOREIGN KEY(character) REFERENCES Characters(character_id) ON DELETE CASCADE,
);

CREATE TABLE Characters (
	character_id INTEGER PRIMARY KEY,
	page_id INTEGER NOT NULL,
	created DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
	FOREIGN KEY(page_id) REFERENCES Pages(page_id) ON DELETE CASCADE
);

CREATE TABLE Sessions (
	session_id INTEGER PRIMARY KEY,
	campaign_id INTEGER NOT NULL,
	audio_file VARCHAR(64),
	date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
	FOREIGN KEY (campaign_id) REFERENCES Campaigns(campaign_id) ON DELETE CASCADE
);

CREATE TABLE Boxes (
	box_id INTEGER PRIMARY KEY,
	page_id INTEGER NOT NULL,
	show_all_players INTEGER NOT NULL,
	FOREIGN KEY (page_id) REFERENCES Pages(page_id) ON DELETE CASCADE
);

CREATE TABLE Images (
	image_id INTEGER PRIMARY KEY,
	box_id INTEGER NOT NULL,
	image_file VARCHAR(64),
	FOREIGN KEY(box_id) REFERENCES Boxes(box_id) ON DELETE CASCADE
);

CREATE TABLE Texts (
	text_id INTEGER PRIMARY KEY,
	box_id INTEGER NOT NULL,
	page_id_forward INTEGER NOT NULL,
	text_content VARCHAR(1024),
	leaf INTEGER NOT NULL,
	FOREIGN KEY(box_id) REFERENCES Boxes(box_id) ON DELETE CASCADE,
	FOREIGN KEY(page_id_forward) REFERENCES Pages(page_id) ON DELETE CASCADE
);
