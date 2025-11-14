INSERT INTO Users (username, email, password)
VALUES 
('asmusaj', 'asmusaj@gmail.com', 'sha512$f0aa362200ab4e81ae663c440618015e$567d1461a43e0bc1f7a80a55bbc123a05e0a4d20a6075222d8d1542ab7c7b579a95d64d44f61c2d2f93788350e00583d8ad0c0384b5063b2dc493ec2a9ca7808'),
('Matt', 'mattness@gmail.com', 'sha512$1eef18cb8c744a70853168af5099f7df$91fa5c8a18d99407e9ebd4f2df82b4c1112baa1ed8b89852144f984b5cd5c63082f6eb2260a08d78a9c0324e875fad47082a93c7fc79d030c689c753ffa95445'),
('truck', 'truckerman@gmail.com', 'sha512$ac9274daa0f54327992c8a4d7b77f773$ddaeddb9684dc9c0ae16fc0592b87193d0933f2d63778e496d370c8ad0f15720f8dbc4bfbd3d16e52139fbd552899fe66bced16921e244d2b6178dbbd55cc37b'),
('3v31YN3', 'cahee@gmail.com', 'sha512$ffe5dd0630ac490ea3613c5524a8aa98$72364d059e39ec8b103e0d6a23d2fb7466bc9bc251a578fec1ecd186f1896460a721a3991b78a44c40624f780bcdf2be675f7d018c71d960cc033650ff1e55c6');
/* 
asmusaj password is MattIsCute
Matt password is BakuDeku15
truck password is whoamIWhere1sTh1s
3v31YN3 password is chickenFinger1!
*/

INSERT INTO Pages (page_title, owner_username)
VALUES
('Scorn', 'asmusaj'),
('Truckers Paradise', 'truck'),
('Scarlord', 'asmusaj'),
('Matt-Chan', 'asmusaj'),
('ASMR Goddess', 'Matt'),
('Bastion', 'truck'),
('Chet', 'truck'),
('Keeper of the Crypt', '3v31YN3'),
('Scorn NPCS', 'asmusaj'),
('Scorn Places of Interest', 'asmusaj'),
('The Gandy Dancer', 'asmusaj');


INSERT INTO Campaigns (owner_username, page_id, campaign_system)
VALUES
('asmusaj', 1, "Cyberpunk RED"),
('truck', 2, "Cyberpunk RED");

INSERT INTO CampaignPlayers (campaign_id, username)
VALUES
(1, 'asmusaj');

INSERT INTO CampaignPlayers (campaign_id, username, character_id)
VALUES
(1, 'Matt', 3),
(1, 'truck', 4),
(2, 'asmusaj', 1),
(2, 'truck', 4);

INSERT INTO CampaignPlayers (campaign_id, username)
VALUES
(2, '3v31YN3');

INSERT INTO Characters (page_id, character_system)
VALUES
(3, "Cyberpunk RED"),
(4, "Cyberpunk RED"),
(5, "Cyberpunk RED"),
(6, "Cyberpunk RED"),
(7, "Cyberpunk RED"),
(8, "Cyberpunk RED");

INSERT INTO Sessions (campaign_id, date)
VALUES
(1, '2025-09-03'),
(1, '2025-09-16'),
(1, '2025-09-17'),
(1, '2025-11-15'),
(1, '2025-12-01'),
(1, '2025-12-17'),
(2, '2025-7-08');

INSERT INTO Boxes (page_id, show_all_players, box_title)
VALUES
(1, 1, 'Map'), -- box for map for scorn (currently no image file is there)
(1, 1, 'NPCS'), -- box for npcs in scorn
(9, 1, 'John the Barkeeper'), -- box for 1st npc in scorn
(9, 1, 'Teresa the Alchemist'), -- box for 2nd npc in scorn
(9, 1, 'John Hopkins'), -- box for 3rd npc in scorn
(1, 0, 'Secret Plotlines'), -- box for Secret Plotlines in Scorn
(1, 1, 'Places of Interest'), -- box for places of interest in scorn
(10, 1, 'The Gandy Dancer'), -- box for 1st place of interest in scorn
(10, 1, 'The Market'), -- box for 2nd place of interest in scorn
(11, 1, 'NPCS'); -- box for Gandy Dancer NPCS                  10

INSERT INTO Boxes (page_id, show_all_players)
VALUES
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

INSERT INTO Texts (box_id, page_id_forward, leaf)
VALUES
(2, 9, 0),
(3, 1, 1),
(4, 1, 1),
(5, 1, 1);

INSERT INTO Texts (box_id, page_id_forward, text_content, leaf)
VALUES
(6, 1, 
'Yeah so basically everything is a mimic
The food is also made of chum'
, 1); -- secret plotline in scorn
INSERT INTO Texts (box_id, page_id_forward, leaf)
VALUES
(7, 10, 0),
(8, 11, 0),
(9, 1, 1);

INSERT INTO Texts (box_id, page_id_forward, text_content, leaf)
VALUES
(10, 1, 'John Markel, Timothy Chalamet, Tom Brady', 1),
(11, 1, 'Elven', 1),
(12, 1, 'Magic user', 1),
(13, 1, 'Bosco', 1),
(14, 1, 'Breadsticks', 1),
(15, 1, 'Taste', 1),
(16, 1, 'rly', 1),
(17, 1, 'good', 1),
(18, 1, 'Under Construction little doggy, yeehaw', 1);







