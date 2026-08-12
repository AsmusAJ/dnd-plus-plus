import flask
import ttrpg


@ttrpg.app.route('/users/<user_url_slug>/campaign/<int:campaign_id_url_slug>/session/create', methods=['POST'])
def create_session_for_campaign(user_url_slug, campaign_id_url_slug):
    if 'username' not in flask.session:
        return flask.redirect('/accounts/login/')

    username = flask.session['username']
    if username != user_url_slug:
        return flask.jsonify({"message": "Forbidden", "status_code": 403}), 403

    conn = ttrpg.model.get_db()
    permission_query = conn.execute(
        "SELECT username FROM CampaignPlayers WHERE username = ? AND campaign_id = ?",
        (username, campaign_id_url_slug),
    ).fetchone()
    if permission_query is None:
        return flask.jsonify({"message": "Forbidden.", "status_code": 403}), 403

    session_date = flask.request.form.get('date') or flask.request.form.get('session_date')
    if not session_date:
        return flask.abort(400)

    conn.execute(
        "INSERT INTO Sessions (campaign_id, audio_file, date) VALUES (?, ?, ?)",
        (campaign_id_url_slug, None, session_date),
    )
    conn.commit()
    return flask.redirect(f'/users/{username}/campaign/{campaign_id_url_slug}/')


@ttrpg.app.route('/users/<user_url_slug>/campaign/<int:campaign_id_url_slug>/system', methods=['POST'])
def update_campaign_system(user_url_slug, campaign_id_url_slug):
    if 'username' not in flask.session:
        return flask.redirect('/accounts/login/')

    username = flask.session['username']
    if username != user_url_slug:
        return flask.jsonify({"message": "Forbidden", "status_code": 403}), 403

    conn = ttrpg.model.get_db()
    permission_query = conn.execute(
        "SELECT username FROM CampaignPlayers WHERE username = ? AND campaign_id = ?",
        (username, campaign_id_url_slug),
    ).fetchone()
    if permission_query is None:
        return flask.jsonify({"message": "Forbidden.", "status_code": 403}), 403

    campaign_system = flask.request.form.get('campaign_system') or 'Custom'
    conn.execute(
        "UPDATE Campaigns SET campaign_system = ? WHERE campaign_id = ?",
        (campaign_system, campaign_id_url_slug),
    )
    conn.commit()
    return flask.redirect(f'/users/{username}/campaign/{campaign_id_url_slug}/')


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
        "SELECT c.page_id, c.campaign_system, p.owner_username, p.page_title "
        "FROM Campaigns c "
        "JOIN Pages p ON c.page_id = p.page_id "
        "WHERE c.campaign_id = ? ",
        (campaign_id_url_slug,)
    ).fetchone()

    page_id = campaign["page_id"]
    campaign_system = campaign["campaign_system"]

    owner_username = campaign["owner_username"]

    page_title = campaign["page_title"]

    boxes_query = conn.execute(
        "SELECT b.box_id, b.page_id, b.show_all_players, b.box_title, t.text_id, t.text_content, "
        "t.page_id_forward, t.leaf, i.image_id, i.image_file "
        "FROM Boxes b "
        "LEFT JOIN Texts t ON b.box_id = t.box_id "
        "LEFT JOIN Images i ON b.box_id = i.box_id "
        "WHERE b.page_id = ? ",
        (page_id,)
    )

    boxes = boxes_query.fetchall()

    visible_boxes = []
    for box in boxes:
        if box["show_all_players"] == 0 and username != owner_username:
            continue
        visible_boxes.append({
            "box_id": box["box_id"],
            "box_title": box["box_title"],
            "show_all_players": box["show_all_players"],
            "text_id": box["text_id"],
            "text": box["text_content"],
            "page_id_forward": box["page_id_forward"],
            "leaf": box["leaf"],
            "image_id": box["image_id"],
            "image_file": box["image_file"],
        })

    results = visible_boxes

    sessions = conn.execute(
        "SELECT session_id, audio_file, date "
        "FROM Sessions "
        "WHERE campaign_id = ? ",
        (campaign_id_url_slug,)
    ).fetchall()

    sessions_results = [
        {
            "session_id": session["session_id"],
            "audio_file": session["audio_file"],
            "date": session["date"],
        }
        for session in sessions
    ]

    characters = conn.execute(
        "SELECT p.character_id, d.page_title, d.owner_username "
        "FROM CampaignPlayers p "
        "JOIN Characters c ON p.character_id = c.character_id "
        "JOIN Pages d ON c.page_id = d.page_id "
        "WHERE p.campaign_id = ? ",
        (campaign_id_url_slug,)
    ).fetchall()

    characters_results = [
        {
            "character_id": character["character_id"],
            "character_name": character["page_title"],
            "owner_username": character["owner_username"],
        }
        for character in characters
    ]

    response = {
        "page_id": page_id,
        "campaign_id": campaign_id_url_slug,
        "owner_username": owner_username,
        "page_title": page_title,
        "campaign_system": campaign_system,
        "boxes": results,
        "sessions": sessions_results,
        "characters": characters_results
    }

    return flask.render_template("campaign_page.html", **response)
