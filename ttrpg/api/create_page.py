import flask
import ttrpg

@ttrpg.app.route('/api/v1/create_page', methods=['POST'])
def create_page():
    data = flask.request.get_json()
    pageTitle = data.get('page_title')
    ownerUsername = flask.session['username']
    boxId = data.get('box_id')

    # Save to SQLite
    conn = ttrpg.model.get_db()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO pages (page_title, owner_username) " \
        "VALUES (?, ?)", (pageTitle, ownerUsername)
        )

    conn.commit()
    newId = cursor.lastrowid

    cursor.execute(
        "UPDATE Texts " \
        "SET page_id_forward = ?, leaf = 0 " \
        "WHERE box_id = ?", (newId, boxId)
        )
    conn.commit()

    return flask.jsonify({"success": True, "page_id": newId}), 201
