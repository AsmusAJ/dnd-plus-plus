import flask
import ttrpg


@ttrpg.app.route('/campaigns/create', methods=['POST'])
def create_campaign_from_homepage():
    if 'username' not in flask.session:
        return flask.redirect('/accounts/login/')

    username = flask.session['username']
    page_title = flask.request.form.get('page_title') or 'New Campaign'
    campaign_system = flask.request.form.get('campaign_system') or 'Custom'

    conn = ttrpg.model.get_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO Pages (page_title, owner_username) VALUES (?, ?)",
        (page_title, username),
    )
    page_id = cursor.lastrowid

    cursor.execute(
        "INSERT INTO Campaigns (owner_username, page_id, campaign_system) VALUES (?, ?, ?)",
        (username, page_id, campaign_system),
    )
    campaign_id = cursor.lastrowid

    cursor.execute(
        "INSERT OR IGNORE INTO CampaignPlayers (campaign_id, username) VALUES (?, ?)",
        (campaign_id, username),
    )
    conn.commit()
    return flask.redirect(f'/users/{username}/campaign/{campaign_id}/')


@ttrpg.app.route('/characters/create', methods=['POST'])
def create_character_from_homepage():
    if 'username' not in flask.session:
        return flask.redirect('/accounts/login/')

    username = flask.session['username']
    page_title = flask.request.form.get('page_title') or 'New Character'
    character_system = flask.request.form.get('character_system') or 'Custom'

    conn = ttrpg.model.get_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO Pages (page_title, owner_username) VALUES (?, ?)",
        (page_title, username),
    )
    page_id = cursor.lastrowid

    cursor.execute(
        "INSERT INTO Characters (page_id, character_system) VALUES (?, ?)",
        (page_id, character_system),
    )
    character_id = cursor.lastrowid
    conn.commit()
    return flask.redirect(f'/users/{username}/character/{character_id}/')


@ttrpg.app.route('/')
def show_homepage():

    
    if 'username' not in flask.session:
        return flask.redirect("/accounts/login/")

    conn = ttrpg.model.get_db()

    username = ttrpg.api.authenticate.authenticate()

    if not username: 
        return flask.jsonify({"message": "Forbidden", "status_code": 403}), 403

    campaign_query = conn.execute(
        "SELECT cp.campaign_id, c.page_id, p.owner_username, c.created, p.page_title, c.campaign_system "
        "FROM CampaignPlayers cp "
        "JOIN Campaigns c ON cp.campaign_id = c.campaign_id "
        "JOIN Pages p ON c.page_id = p.page_id "
        "WHERE (cp.username = ?) "
        "ORDER BY c.created DESC "
        "LIMIT 3",
        (username,)
    )

    campaigns_list = campaign_query.fetchall()

    campaigns = [
        {
            "page_id": campaign["page_id"],
            "campaign_id": campaign["campaign_id"],
            "owner_username": campaign["owner_username"],
            "page_title": campaign["page_title"],
            "created": campaign["created"],
            "system": campaign["campaign_system"]
        }
        for campaign in campaigns_list
    ]

    character_query = conn.execute(
        "SELECT c.character_id, c.page_id, p.owner_username, c.created, p.page_title, c.character_system "
        "FROM Characters c " 
        "JOIN Pages p ON c.page_id = p.page_id "
        "WHERE (p.owner_username = ?) "
        "ORDER BY c.created DESC "
        "LIMIT 3",
        (username,)
    )

    characters_list = character_query.fetchall()

    characters = [
        {
            "page_id": character["page_id"],
            "character_id": character["character_id"],
            "owner_username": character["owner_username"],
            "page_title": character["page_title"],
            "created": character["created"],
            "system": character["character_system"]
        }
        for character in characters_list
    ]

    session_query = conn.execute(
        "SELECT s.date, p.page_title, c.campaign_id "
        "FROM Sessions s " 
        "JOIN Campaigns c ON s.campaign_id = c.campaign_id "
        "JOIN Pages p ON c.page_id = p.page_id "
        "WHERE (p.owner_username = ?) "
        "AND s.date >= DATE('now') "
        "ORDER BY s.date ASC "
        "LIMIT 3",
        (username,)
    )

    session_list = session_query.fetchall()

    sessions = [
        {
            "date": session["date"],
            "page_title": session["page_title"],
            "campaign_id": session["campaign_id"]
        }
        for session in session_list
    ]

    response = {
        "campaigns": campaigns,
        "characters": characters,
        "sessions": sessions
    }
    
    return flask.render_template("homepage.html", **response)
