import uuid

import ttrpg


def test_toggle_box_visibility_updates_show_all_players():
    username = f"test_owner_{uuid.uuid4().hex[:8]}"
    email = f"{username}@example.com"

    with ttrpg.app.app_context():
        conn = ttrpg.model.get_db()
        conn.execute(
            "INSERT OR IGNORE INTO Users (username, email, password) VALUES (?, ?, ?)",
            (username, email, "unused"),
        )

        page_id = conn.execute(
            "INSERT INTO Pages (page_title, owner_username) VALUES (?, ?)",
            ("Visibility Test", username),
        ).lastrowid

        box_id = conn.execute(
            "INSERT INTO Boxes (page_id, show_all_players, box_title) VALUES (?, 0, ?)",
            (page_id, "Secret Box"),
        ).lastrowid

        conn.commit()

    client = ttrpg.app.test_client()
    with client.session_transaction() as sess:
        sess["username"] = username

    response = client.post(
        "/api/v1/toggle_box_visibility",
        json={"box_id": box_id},
    )

    assert response.status_code == 200
    payload = response.get_json()
    assert payload["show_all_players"] == 1

    with ttrpg.app.app_context():
        conn = ttrpg.model.get_db()
        row = conn.execute(
            "SELECT show_all_players FROM Boxes WHERE box_id = ?",
            (box_id,),
        ).fetchone()
        assert row["show_all_players"] == 1


def test_hidden_boxes_are_filtered_for_non_owners_on_shared_campaign_pages():
    owner = f"owner_{uuid.uuid4().hex[:8]}"
    player = f"player_{uuid.uuid4().hex[:8]}"

    with ttrpg.app.app_context():
        conn = ttrpg.model.get_db()
        conn.execute(
            "INSERT OR IGNORE INTO Users (username, email, password) VALUES (?, ?, ?)",
            (owner, f"{owner}@example.com", "unused"),
        )
        conn.execute(
            "INSERT OR IGNORE INTO Users (username, email, password) VALUES (?, ?, ?)",
            (player, f"{player}@example.com", "unused"),
        )

        page_id = conn.execute(
            "INSERT INTO Pages (page_title, owner_username) VALUES (?, ?)",
            ("Shared Campaign", owner),
        ).lastrowid

        campaign_id = conn.execute(
            "INSERT INTO Campaigns (owner_username, page_id, campaign_system) VALUES (?, ?, ?)",
            (owner, page_id, "D&D"),
        ).lastrowid

        conn.execute(
            "INSERT INTO CampaignPlayers (campaign_id, username) VALUES (?, ?)",
            (campaign_id, player),
        )

        hidden_box_id = conn.execute(
            "INSERT INTO Boxes (page_id, show_all_players, box_title) VALUES (?, 0, ?)",
            (page_id, "Secret Box"),
        ).lastrowid
        max_text_id = conn.execute(
            "SELECT MAX(text_id) AS max_text_id FROM Texts"
        ).fetchone()["max_text_id"]
        text_id = (max_text_id or 0) + 1
        conn.execute(
            "INSERT INTO Texts (text_id, box_id, page_id_forward, text_content, leaf) VALUES (?, ?, ?, ?, ?)",
            (text_id, hidden_box_id, 1, "hidden", 1),
        )
        conn.commit()

    client = ttrpg.app.test_client()
    with client.session_transaction() as sess:
        sess["username"] = player

    response = client.get(f"/users/{player}/campaign/{campaign_id}/")
    assert response.status_code == 200
    assert "Secret Box" not in response.get_data(as_text=True)
