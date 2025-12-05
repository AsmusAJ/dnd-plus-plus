import flask
import sqlite3
import ttrpg

@ttrpg.app.route('/api/v1/create_box', methods=['POST'])
def create_box():
    data = flask.request.get_json()
    pageId = data.get('page_id')

    # Save to SQLite
    conn = ttrpg.model.get_db()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO Boxes (page_id, show_all_players, box_title) " \
        "VALUES (?, 1, 'Add Title')", (pageId,)
        )

    conn.commit()
    newId = cursor.lastrowid

    cursor.execute(
        "INSERT INTO Texts (box_id, page_id_forward, text_content, leaf) " \
        "VALUES (?, 1, 'Add Content', 1)", (newId,)
        )
    conn.commit()

    return flask.jsonify({"success": True, "box_id": newId}), 201  
