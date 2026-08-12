import flask
import ttrpg


@ttrpg.app.route('/api/v1/toggle_box_visibility', methods=['POST'])
def toggle_box_visibility():
    data = flask.request.get_json(silent=True) or {}
    box_id = data.get('box_id')
    username = flask.session.get('username')

    if not username:
        return flask.jsonify({"success": False, "error": "Not logged in."}), 401

    if box_id is None:
        return flask.jsonify({"success": False, "error": "Box ID is required."}), 400

    conn = ttrpg.model.get_db()
    box = conn.execute(
        "SELECT b.box_id, b.show_all_players, p.owner_username "
        "FROM Boxes b "
        "JOIN Pages p ON p.page_id = b.page_id "
        "WHERE b.box_id = ?",
        (box_id,),
    ).fetchone()

    if box is None:
        return flask.jsonify({"success": False, "error": "Box not found."}), 404

    if box["owner_username"] != username:
        return flask.jsonify({"success": False, "error": "Only the page owner can change box visibility."}), 403

    new_visible = 0 if box["show_all_players"] == 1 else 1
    conn.execute(
        "UPDATE Boxes SET show_all_players = ? WHERE box_id = ?",
        (new_visible, box_id),
    )
    conn.commit()

    return flask.jsonify({"success": True, "box_id": box_id, "show_all_players": new_visible})
