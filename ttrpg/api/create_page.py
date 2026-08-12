import flask
import ttrpg

@ttrpg.app.route('/api/v1/create_page', methods=['POST'])
def create_page():
    data = flask.request.get_json(silent=True) or {}
    page_title = data.get('page_title')
    owner_username = flask.session.get('username')
    box_id = data.get('box_id')

    conn = ttrpg.model.get_db()
    cursor = conn.cursor()

    if not owner_username:
        return flask.jsonify({"success": False, "error": "Not logged in."}), 401

    if not page_title or not box_id:
        return flask.jsonify({"success": False, "error": "Missing required fields."}), 400

    cursor.execute(
        "SELECT 1 FROM Boxes WHERE box_id = ?",
        (box_id,),
    )
    if cursor.fetchone() is None:
        return flask.jsonify({"success": False, "error": "Box not found."}), 404

    cursor.execute(
        "INSERT INTO Pages (page_title, owner_username) VALUES (?, ?)",
        (page_title, owner_username),
    )
    new_id = cursor.lastrowid

    cursor.execute(
        "UPDATE Texts SET page_id_forward = ?, leaf = 0 WHERE box_id = ?",
        (new_id, box_id),
    )

    if cursor.rowcount == 0:
        conn.rollback()
        return flask.jsonify({"success": False, "error": "Box text row not found."}), 404

    conn.commit()
    return flask.jsonify({"success": True, "page_id": new_id}), 201
