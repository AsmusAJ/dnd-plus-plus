import flask
import ttrpg

@ttrpg.app.route('/')
def show_homepage():

    # if 'username' not in flask.session:
    #     return flask.redirect("/accounts/login/")

    username = "asmusaj"

    conn = ttrpg.model.get_db()

    # username = ttrpg.api.authenticate.authenticate()

    # if not username: 
    #     return flask.jsonify({"message": "Forbidden", "status_code": 403}), 403

    campaign_query = conn.execute(
        "SELECT cp.campaign_id, c.page_id, p.owner_username, c.created, p.page_title "
        "FROM CampaignPlayers cp "
        "JOIN Campaigns c ON cp.campaign_id = c.campaign_id "
        "JOIN Pages p ON c.page_id = p.page_id "
        "WHERE (cp.username = ?) "
        "ORDER BY c.created DESC "
        "LIMIT 3",
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
    
    return flask.render_template("homepage.html", **response)