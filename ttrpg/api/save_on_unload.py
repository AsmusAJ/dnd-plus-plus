import Flask, request
import sqlite3
import ttrpg

@ttrpg.app.route('/save_notes_on_unload', methods=['POST'])
def save_notes_on_unload():
    data = request.get_json()
    notes = data.get('notes', '')

    # In a real app, you'd want to associate the notes with a user ID
    user_id = 1 # Example, ideally this comes from user session

    # Save to SQLite
    conn = sqlite3.connect('your_database.db')
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO notes (user_id, note_text)
        VALUES (?, ?)
        ON CONFLICT(user_id) DO UPDATE SET note_text=excluded.note_text
    """, (user_id, notes))
    conn.commit()
    conn.close()

    return '', 204  # No content needed
