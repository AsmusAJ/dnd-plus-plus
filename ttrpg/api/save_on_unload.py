import flask
import sqlite3
import ttrpg

@ttrpg.app.route('/api/v1/save_on_unload', methods=['POST'])
def save_on_unload():
    data = flask.request.get_json()
    texts = data.get('texts', [])

    # Save to SQLite
    conn = ttrpg.model.get_db()
    cursor = conn.cursor()

    for text in texts:
        textId = text['id']
        textContent = text['text']
        cursor.execute("UPDATE Texts SET text_content=? WHERE text_id=?", (textContent, textId))
    conn.commit()
    conn.close()

    #We use this because page is unloaded so user cant use response anyway
    return '', 204  
