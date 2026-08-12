import uuid

import ttrpg


def test_campaign_owner_can_set_game_system():
    owner = f"owner_{uuid.uuid4().hex[:8]}"
    email = f"{owner}@example.com"

    with ttrpg.app.app_context():
        conn = ttrpg.model.get_db()
        conn.execute(
            "INSERT OR IGNORE INTO Users (username, email, password) VALUES (?, ?, ?)",
            (owner, email, "unused"),
        )
        page_id = conn.execute(
            "INSERT INTO Pages (page_title, owner_username) VALUES (?, ?)",
            ("System Campaign", owner),
        ).lastrowid
        campaign_id = conn.execute(
            "INSERT INTO Campaigns (owner_username, page_id, campaign_system) VALUES (?, ?, ?)",
            (owner, page_id, "Custom"),
        ).lastrowid
        conn.execute(
            "INSERT OR IGNORE INTO CampaignPlayers (campaign_id, username) VALUES (?, ?)",
            (campaign_id, owner),
        )
        conn.commit()

    client = ttrpg.app.test_client()
    with client.session_transaction() as sess:
        sess["username"] = owner

    response = client.post(
        f"/users/{owner}/campaign/{campaign_id}/system",
        data={"campaign_system": "Pathfinder 2e"},
        follow_redirects=False,
    )

    assert response.status_code == 302
    assert response.headers["Location"] == f"/users/{owner}/campaign/{campaign_id}/"

    with ttrpg.app.app_context():
        conn = ttrpg.model.get_db()
        row = conn.execute(
            "SELECT campaign_system FROM Campaigns WHERE campaign_id = ?",
            (campaign_id,),
        ).fetchone()
        assert row["campaign_system"] == "Pathfinder 2e"


def test_character_owner_can_set_game_system():
    owner = f"owner_{uuid.uuid4().hex[:8]}"
    email = f"{owner}@example.com"

    with ttrpg.app.app_context():
        conn = ttrpg.model.get_db()
        conn.execute(
            "INSERT OR IGNORE INTO Users (username, email, password) VALUES (?, ?, ?)",
            (owner, email, "unused"),
        )
        page_id = conn.execute(
            "INSERT INTO Pages (page_title, owner_username) VALUES (?, ?)",
            ("System Character", owner),
        ).lastrowid
        character_id = conn.execute(
            "INSERT INTO Characters (page_id, character_system) VALUES (?, ?)",
            (page_id, "Custom"),
        ).lastrowid
        conn.commit()

    client = ttrpg.app.test_client()
    with client.session_transaction() as sess:
        sess["username"] = owner

    response = client.post(
        f"/users/{owner}/character/{character_id}/system",
        data={"character_system": "D&D 5e"},
        follow_redirects=False,
    )

    assert response.status_code == 302
    assert response.headers["Location"] == f"/users/{owner}/character/{character_id}/"

    with ttrpg.app.app_context():
        conn = ttrpg.model.get_db()
        row = conn.execute(
            "SELECT character_system FROM Characters WHERE character_id = ?",
            (character_id,),
        ).fetchone()
        assert row["character_system"] == "D&D 5e"
