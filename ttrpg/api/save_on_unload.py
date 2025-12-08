import flask
import sqlite3
import ttrpg

@ttrpg.app.route('/api/v1/save_on_unload', methods=['POST'])
def save_on_unload():
    data = flask.request.get_json()
    texts = data.get('texts', [])
    headers = data.get('headers', [])
    page_title = data.get('page_title')
    pageId = data.get('page_id')

    # Save to SQLite
    conn = ttrpg.model.get_db()
    cursor = conn.cursor()

    cursor.execute("UPDATE Pages SET page_title=? WHERE page_id=?", (page_title, pageId))

    for text in texts:
        textId = text['id']
        textContent = text['text']
        cursor.execute("UPDATE Texts SET text_content=? WHERE text_id=?", (textContent, textId))

    for header in headers:
        boxId = header['id']
        title = header['title']
        cursor.execute("UPDATE Boxes SET box_title=? WHERE box_id=?", (title, boxId))
    conn.commit()

    #We use this because page is unloaded so user cant use response anyway
    return '', 204  
