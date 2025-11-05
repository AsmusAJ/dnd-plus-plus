import flask
import ttrpg
import ttrpg.api.authenticate

@ttrpg.app.route('api/v1/characters/', methods=['GET'])
def get_characters():
    conn = ttrpg.model.get_db()

    username = ttrpg.api.authenticate.authenticate()

    if not username: 
        return flask.jsonify({"message": "Forbidden", "status_code": 403}), 403

    character_query = conn.execute(
        "SELECT c.character_id, c.page_id, c.owner_id, c.created, p.page_title "
        "FROM Characters c " 
        "JOIN Pages p ON c.page_id = p.page_id "
        "WHERE (c.owner_id = ?) ",
        (username,)
    )

    characters = character_query.fetchall()

    results = [
        {
            "page_id": character["page_id"],
            "character_id": character["character_id"],
            "owner_id": character["owner_id"],
            "page_title": character["page_title"],
            "created": character["created"]
        }
        for character in characters
    ]

    response = {
        "characters": results
    }
    return flask.jsonify(**response)