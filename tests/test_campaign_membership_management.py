import uuid

import ttrpg


def test_owner_can_add_and_remove_other_user_from_campaign():
    owner = f"owner_{uuid.uuid4().hex[:8]}"
    other = f"player_{uuid.uuid4().hex[:8]}"

    with ttrpg.app.app_context():
        conn = ttrpg.model.get_db()
        conn.execute(
            "INSERT OR IGNORE INTO Users (username, email, password) VALUES (?, ?, ?)",
            (owner, f"{owner}@example.com", "unused"),
        )
        conn.execute(
            "INSERT OR IGNORE INTO Users (username, email, password) VALUES (?, ?, ?)",
            (other, f"{other}@example.com", "unused"),
        )
        page_id = conn.execute(
            "INSERT INTO Pages (page_title, owner_username) VALUES (?, ?)",
            ("Membership Campaign", owner),
        ).lastrowid
        campaign_id = conn.execute(
            "INSERT INTO Campaigns (owner_username, page_id, campaign_system) VALUES (?, ?, ?)",
            (owner, page_id, "D&D 5e"),
        ).lastrowid
        conn.execute(
            "INSERT OR IGNORE INTO CampaignPlayers (campaign_id, username) VALUES (?, ?)",
            (campaign_id, owner),
        )
        conn.commit()

    client = ttrpg.app.test_client()
    with client.session_transaction() as sess:
        sess["username"] = owner

    add_response = client.post(
        f"/users/{owner}/campaign/{campaign_id}/players",
        data={"username": other, "action": "add"},
        follow_redirects=False,
    )
    assert add_response.status_code == 302
    assert add_response.headers["Location"] == f"/users/{owner}/campaign/{campaign_id}/"

    with ttrpg.app.app_context():
        conn = ttrpg.model.get_db()
        membership = conn.execute(
            "SELECT username FROM CampaignPlayers WHERE campaign_id = ? AND username = ?",
            (campaign_id, other),
        ).fetchone()
        assert membership is not None

    remove_response = client.post(
        f"/users/{owner}/campaign/{campaign_id}/players",
        data={"username": other, "action": "remove"},
        follow_redirects=False,
    )
    assert remove_response.status_code == 302
    assert remove_response.headers["Location"] == f"/users/{owner}/campaign/{campaign_id}/"

    with ttrpg.app.app_context():
        conn = ttrpg.model.get_db()
        membership = conn.execute(
            "SELECT username FROM CampaignPlayers WHERE campaign_id = ? AND username = ?",
            (campaign_id, other),
        ).fetchone()
        assert membership is None


def test_owner_cannot_remove_self_from_campaign():
    owner = f"owner_{uuid.uuid4().hex[:8]}"

    with ttrpg.app.app_context():
        conn = ttrpg.model.get_db()
        conn.execute(
            "INSERT OR IGNORE INTO Users (username, email, password) VALUES (?, ?, ?)",
            (owner, f"{owner}@example.com", "unused"),
        )
        page_id = conn.execute(
            "INSERT INTO Pages (page_title, owner_username) VALUES (?, ?)",
            ("Membership Campaign", owner),
        ).lastrowid
        campaign_id = conn.execute(
            "INSERT INTO Campaigns (owner_username, page_id, campaign_system) VALUES (?, ?, ?)",
            (owner, page_id, "D&D 5e"),
        ).lastrowid
        conn.execute(
            "INSERT OR IGNORE INTO CampaignPlayers (campaign_id, username) VALUES (?, ?)",
            (campaign_id, owner),
        )
        conn.commit()

    client = ttrpg.app.test_client()
    with client.session_transaction() as sess:
        sess["username"] = owner

    page_response = client.get(f"/users/{owner}/campaign/{campaign_id}/")
    assert page_response.status_code == 200
    assert b"Remove" not in page_response.data

    remove_response = client.post(
        f"/users/{owner}/campaign/{campaign_id}/players",
        data={"username": owner, "action": "remove"},
        follow_redirects=False,
    )
    assert remove_response.status_code == 403
