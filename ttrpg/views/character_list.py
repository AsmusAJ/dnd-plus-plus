import flask
import ttrpg
import ttrpg.api.authenticate

@ttrpg.app.route('/users/<user_url_slug>/characters/')
def show_characters(user_url_slug):
    conn = ttrpg.model.get_db()

    if 'username' not in flask.session:
        return flask.redirect("/accounts/login/")
    username = flask.session['username']

    if username != user_url_slug: 
        return flask.jsonify({"message": "Forbidden", "status_code": 403}), 403

    character_query = conn.execute(
        "SELECT c.character_id, c.page_id, p.owner_username, c.created, p.page_title "
        "FROM Characters c " 
        "JOIN Pages p ON c.page_id = p.page_id "
        "WHERE (p.owner_username = ?) ",
        (username,)
    )

    characters = character_query.fetchall()

    results = [
        {
            "page_id": character["page_id"],
            "character_id": character["character_id"],
            "owner_username": character["owner_username"],
            "page_title": character["page_title"],
            "created": character["created"]
        }
        for character in characters
    ]

    response = {
        "characters": results
    }

    return flask.render_template("char_list.html", **response)
