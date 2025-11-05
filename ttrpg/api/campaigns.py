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
        "SELECT cp.campaign_id, c.page_id, c.owner_id, c.created, p.page_title "
        "FROM CampaignPlayers cp "
        "JOIN Campaigns c ON cp.campaign_id = c.campaign_id "
        "JOIN Pages p ON c.page_id = p.page_id "
        "WHERE (cp.user_id = ?) ",
        (username,)
    )

    campaigns = campaign_query.fetchall()

    results = [
        {
            "page_id": campaign["page_id"],
            "campaign_id": campaign["campaign_id"],
            "owner_id": campaign["owner_id"],
            "page_title": campaign["page_title"],
            "created": campaign["created"]
        }
        for campaign in campaigns
    ]

    response = {
        "campaigns": results
    }
    return flask.jsonify(**response)