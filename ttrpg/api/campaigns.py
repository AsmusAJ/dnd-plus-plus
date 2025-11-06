import flask
import ttrpg
import ttrpg.api.authenticate

@ttrpg.app.route('api/v1/campaigns/', methods=['GET'])
def get_campaigns():
    conn = ttrpg.model.get_db()

    username = ttrpg.api.authenticate.authenticate()

    if not username: 
        return flask.jsonify({"message": "Forbidden", "status_code": 403}), 403

    campaign_query = conn.execute(
        "SELECT cp.campaign_id, c.page_id, c.owner_username, c.created, p.page_title "
        "FROM CampaignPlayers cp "
        "JOIN Campaigns c ON cp.campaign_id = c.campaign_id "
        "JOIN Pages p ON c.page_id = p.page_id "
        "WHERE (cp.username = ?) ",
        (username,)
    )

    campaigns = campaign_query.fetchall()

    results = [
        {
            "page_id": campaign["page_id"],
            "campaign_id": campaign["campaign_id"],
            "owner_username": campaign["owner_username"],
            "page_title": campaign["page_title"],
            "created": campaign["created"]
        }
        for campaign in campaigns
    ]

    response = {
        "campaigns": results
    }
    return flask.jsonify(**response)

@ttrpg.app.route('api/v1/campaign/<int:campaign_id_url_slug/', methods=['GET'])
def get_campaign(campaign_id_url_slug):
    conn = ttrpg.model.get_db()

    username = ttrpg.api.authenticate.authenticate()

    # Checks if user is logged in
    if not username: 
        return flask.jsonify({"message": "Forbidden", "status_code": 403}), 403

    permission_query = conn.execute(
        "SELECT username "
        "FROM CampaignPlayers "
        "WHERE username = ? AND campaign_id = ? ",
        (username, campaign_id_url_slug)
    ).fetchone()

    # Checks if user has access to campaign
    if username != permission_query["username"]:
        return flask.jsonify({"message": "Forbidden.", "status_code": 403}), 403
