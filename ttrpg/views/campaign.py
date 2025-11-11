import flask
import ttrpg

@ttrpg.app.route('/users/<user_url_slug>/campaign/<int:campaign_id_url_slug>/', methods=['GET'])
def show_campaign(user_url_slug, campaign_id_url_slug):
    conn = ttrpg.model.get_db()

    if 'username' not in flask.session:
        return flask.redirect("/accounts/login/")
    
    username = flask.session['username']


    if username != user_url_slug: 
        return flask.jsonify({"message": "Forbidden", "status_code": 403}), 403


    permission_query = conn.execute(
        "SELECT username "
        "FROM CampaignPlayers "
        "WHERE username = ? AND campaign_id = ? ",
        (username, campaign_id_url_slug,)
    ).fetchone()

    # Checks if user has access to campaign
    if username != permission_query["username"]:
        return flask.jsonify({"message": "Forbidden.", "status_code": 403}), 403

    campaign = conn.execute(
        "SELECT c.page_id, p.owner_username, p.page_title "
        "FROM Campaigns c "
        "JOIN Pages p ON c.page_id = p.page_id"
        "WHERE c.campaign_id = ? ",
        (campaign_id_url_slug,)
    ).fetchone()

    page_id = campaign["page_id"]

    owner_username = campaign["owner_username"]

    page_title = campaign["page_title"]

    boxes_query = conn.execute(
        "SELECT b.box_id, b.page_id, b.show_all_players, t.text_id, t.text_content, "
        "t.page_id_forward, t.leaf, i.image_id, i.image_file "
        "FROM Boxes b "
        "JOIN Texts t ON b.box_id = t.box_id "
        "JOIN Images i ON b.box_id = i.box_id "
        "WHERE b.page_id = ? ",
        (page_id,)
    )

    boxes = boxes_query.fetchall()

    results = [
        {
            "box_id": box["box_id"],
            "show_all_players": box["show_all_players"],
            "text_id": box["text_id"],
            "text": box["text_content"],
            "page_id_forward": box["page_id_forward"],
            "leaf": box["leaf"],
            "image_id": box["image_id"],
            "image_file": box["image_file"],            
        }
        for box in boxes
    ]

    sessions = conn.execute(
        "SELECT session_id, audio_file "
        "FROM Sessions "
        "WHERE campaign_id = ? "
    ).fetchall()

    response = {
        "page_id": page_id,
        "campaign_id": campaign_id_url_slug,
        "owner_username": owner_username,
        "page_title": page_title,
        "boxes": results,
        "sessions": sessions
    }

    return flask.render_template("campaign_page.html", **response)
