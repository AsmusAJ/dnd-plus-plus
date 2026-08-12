import datetime
import uuid

import ttrpg


def test_campaign_owner_can_create_session():
    owner = f"owner_{uuid.uuid4().hex[:8]}"
    email = f"{owner}@example.com"
    session_date = "2026-02-14"

    with ttrpg.app.app_context():
        conn = ttrpg.model.get_db()
        conn.execute(
            "INSERT OR IGNORE INTO Users (username, email, password) VALUES (?, ?, ?)",
            (owner, email, "unused"),
        )
        page_id = conn.execute(
            "INSERT INTO Pages (page_title, owner_username) VALUES (?, ?)",
            ("Session Campaign", owner),
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

    response = client.post(
        f"/users/{owner}/campaign/{campaign_id}/session/create",
        data={"date": session_date},
        follow_redirects=False,
    )

    assert response.status_code == 302
    assert response.headers["Location"] == f"/users/{owner}/campaign/{campaign_id}/"

    with ttrpg.app.app_context():
        conn = ttrpg.model.get_db()
        row = conn.execute(
            "SELECT date FROM Sessions WHERE campaign_id = ? ORDER BY session_id DESC LIMIT 1",
            (campaign_id,),
        ).fetchone()
        assert row is not None
        assert row["date"] == session_date
