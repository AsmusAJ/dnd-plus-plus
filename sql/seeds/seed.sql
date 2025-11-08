INSERT INTO Users (username, email, password)
VALUES 
('asmusaj', 'asmusaj@gmail.com', 'MattIsCute'),
('Matt', 'mattness@gmail.com', 'BakuDeku15'),
('truck', 'truckerman@gmail.com', 'whoamIWhere1sTh1s'),
('3v31YN3', 'cahee@gmail.com', 'chickenFinger1!');

INSERT INTO Pages (page_title, owner_username)
VALUES
('Scorn (Campaign)', 'asmusaj'),
('Truckers Paradise (Campaign)', 'truck'),
('Scarlord (player character)', 'asmusaj'),
('Matt-Chan (player character)', 'asmusaj'),
('ASMR Goddess (player character)', 'Matt'),
('Bastion (player character)', 'truck'),
('Chet (player character)', 'truck'),
('Keeper of the Crypt (player character)', '3v31YN3'),
('Scorn NPCS', 'asmusaj'),
('Scorn Places of Interest', 'asmusaj'),
('The Gandy Dancer', 'asmusaj');


INSERT INTO Campaigns (owner_username, page_id)
VALUES
('asmusaj', 1),
('truck', 2);

INSERT INTO CampaignPlayers (campaign_id, username)
VALUES
(1, 'asmusaj'),
(1, 'Matt'),
(1, 'truck'),
(2, 'asmusaj'),
(2, 'truck'),
(2, '3v31YN3');

INSERT INTO Characters (page_id)
VALUES
(3),
(4),
(5),
(6),
(7),
(8);

INSERT INTO Sessions (campaign_id)
VALUES
(1),
(1),
(1),
(2);

INSERT INTO Boxes (page_id, show_all_players)
VALUES
(1, 1), -- box for map for scorn (currently no image file is there)
(1, 1), -- box for npcs in scorn
(9, 1), -- box for 1st npc in scorn
(9, 1), -- box for 2nd npc in scorn
(9, 1), -- box for 3rd npc in scorn
(1, 0), -- box for Secret Plotlines in Scorn
(1, 1), -- box for places of interest in scorn
(10, 1), -- box for 1st place of interest in scorn
(10, 1), -- box for 2nd place of interest in scorn
(11, 1), -- box for Gandy Dancer NPCS                  10
(3, 1), -- box for scarlord
(3, 1), -- box for scarlord
(4, 1), -- box for matt-chan
(5, 1), -- box for asmr goddess
(6, 1), -- box for Bastion                             15
(7, 1), -- box for Chet
(8, 1), -- box for keeper
(2, 1); -- box for truckers paradise

INSERT INTO Images (image_id, box_id)
VALUES
(1, 3);

INSERT INTO Texts (box_id, page_id_forward, text_content, leaf)
VALUES
(2, 9, 'NPCS', 0),
(3, 1, 'John the Barkeeper', 1),
(4, 1, 'Teresa the Alchemist', 1),
(5, 1, 'John Hopkins', 1),
(6, 1, 
'Yeah so basically everything is a mimic
The food is also made of chum'
, 1), -- secret plotline in scorn
(7, 10, 'Places of Interest', 0),
(8, 11, 'The Gandy Dancer', 0),
(9, 1, 'The Market', 1),
(10, 1, 'John Markel, Timothy Chalamet, Tom Brady', 1),
(11, 1, 'Elven', 1),
(12, 1, 'Magic user', 1),
(13, 1, 'Bosco', 1),
(14, 1, 'Breadsticks', 1),
(15, 1, 'Taste', 1),
(16, 1, 'rly', 1),
(17, 1, 'good', 1),
(18, 1, 'Under Construction little doggy, yeehaw', 1);







