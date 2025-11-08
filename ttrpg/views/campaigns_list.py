import flask
import ttrpg

@ttrpg.app.route('/users/<user_url_slug>/campaigns/')
def show_camapigns(user_url_slug):

    conn = ttrpg.mode.get_db()

    # if 'username' not in flask.session:
    #     return flask.redirect("/accounts/login/")
    # username = flask.session['username']

    username = "asmusaj"

    conn = ttrpg.model.get_db()


    campaign_query = conn.execute(
        "SELECT cp.campaign_id, c.page_id, p.owner_username, c.created, p.page_title "
        "FROM CampaignPlayers cp "
        "JOIN Campaigns c ON cp.campaign_id = c.campaign_id "
        "JOIN Pages p ON c.page_id = p.page_id "
        "WHERE (cp.username = ?) "
        "ORDER BY c.created DESC ",
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
    