import uuid

import ttrpg


def test_homepage_can_create_campaign():
    username = f"creator_{uuid.uuid4().hex[:8]}"
    email = f"{username}@example.com"

    with ttrpg.app.app_context():
        conn = ttrpg.model.get_db()
        conn.execute(
            "INSERT OR IGNORE INTO Users (username, email, password) VALUES (?, ?, ?)",
            (username, email, "unused"),
        )
        conn.commit()

    client = ttrpg.app.test_client()
    with client.session_transaction() as sess:
        sess["username"] = username

    response = client.post(
        "/campaigns/create",
        data={"page_title": "My New Campaign", "campaign_system": "D&D 5e"},
        follow_redirects=False,
    )

    assert response.status_code == 302
    campaign_location = response.headers["Location"]
    assert f"/users/{username}/campaign/" in campaign_location

    with ttrpg.app.app_context():
        conn = ttrpg.model.get_db()
        row = conn.execute(
            "SELECT p.page_title, c.owner_username, c.campaign_system "
            "FROM Campaigns c JOIN Pages p ON c.page_id = p.page_id "
            "WHERE c.owner_username = ? ORDER BY c.campaign_id DESC LIMIT 1",
            (username,),
        ).fetchone()
        assert row is not None
        assert row["page_title"] == "My New Campaign"
        assert row["owner_username"] == username
        assert row["campaign_system"] == "D&D 5e"


def test_homepage_can_create_character():
    username = f"creator_{uuid.uuid4().hex[:8]}"
    email = f"{username}@example.com"

    with ttrpg.app.app_context():
        conn = ttrpg.model.get_db()
        conn.execute(
            "INSERT OR IGNORE INTO Users (username, email, password) VALUES (?, ?, ?)",
            (username, email, "unused"),
        )
        conn.commit()

    client = ttrpg.app.test_client()
    with client.session_transaction() as sess:
        sess["username"] = username

    response = client.post(
        "/characters/create",
        data={"page_title": "My New Character", "character_system": "D&D 5e"},
        follow_redirects=False,
    )

    assert response.status_code == 302
    character_location = response.headers["Location"]
    assert f"/users/{username}/character/" in character_location

    with ttrpg.app.app_context():
        conn = ttrpg.model.get_db()
        row = conn.execute(
            "SELECT p.page_title, c.character_system "
            "FROM Characters c JOIN Pages p ON c.page_id = p.page_id "
            "WHERE p.owner_username = ? ORDER BY c.character_id DESC LIMIT 1",
            (username,),
        ).fetchone()
        assert row is not None
        assert row["page_title"] == "My New Character"
        assert row["character_system"] == "D&D 5e"
