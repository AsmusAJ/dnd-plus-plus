import flask
import uuid
import pathlib
import ttrpg

@ttrpg.app.route('/users/<user_url_slug>/character/<int:character_id_url_slug>/', methods=['GET'])
def show_character(character_id_url_slug, user_url_slug):
    conn = ttrpg.model.get_db()

    if 'username' not in flask.session:
        return flask.redirect("/accounts/login/")
    username = flask.session['username']

    if username != user_url_slug: 
        return flask.jsonify({"message": "Forbidden", "status_code": 403}), 403

    #removed as any character should be able to view basic details on a characters
    #permission_query = conn.execute(
    #    "SELECT owner_username "
    #    "FROM Characters "
    #    "WHERE owner_username = ? AND character_id = ? ",
    #    (username, character_id_url_slug,)
    #).fetchone()

    
    # Checks if user has access to character
    #if username != permission_query["owner_username"]:
    #    return flask.jsonify({"message": "Forbidden.", "status_code": 403}), 403

    character = conn.execute(
        "SELECT c.page_id, p.owner_username, p.page_title "
        "FROM Characters c "
        "JOIN Pages p ON c.page_id = p.page_id "
        "WHERE c.character_id = ? ",
        (character_id_url_slug,)
    ).fetchone()

    page_id = character["page_id"]

    owner_username = character["owner_username"]

    page_title = character["page_title"]

    boxes_query = conn.execute(
        "SELECT b.box_id, b.page_id, b.show_all_players, b.box_title, t.text_id, t.text_content, "
        "t.page_id_forward, t.leaf, i.image_id, i.image_file "
        "FROM Boxes b "
        "LEFT JOIN Texts t ON b.box_id = t.box_id "
        "LEFT JOIN Images i ON b.box_id = i.box_id "
        "WHERE b.page_id = ? ",
        (page_id,)
    )

    boxes = boxes_query.fetchall()

    results = [
        {
            "box_id": box["box_id"],
            "box_title": box["box_title"],
            "show_all_players": box["show_all_players"],
            "text_id": box["text_id"],
            "text": box["text_content"],
            "page_id_forward": box["page_id_forward"],
            "leaf": box["leaf"],
            "image_id": box["image_id"],
            "image_file": box["image_file"],            
        }
        for box in boxes
    ]

    response = {
        "page_id": page_id,
        "character_id": character_id_url_slug,
        "user_url_slug": user_url_slug,
        "owner_username": owner_username,
        "page_title": page_title,
        "boxes": results
    }

    return flask.render_template("character_page.html", **response)


@ttrpg.app.route('/character/', methods=['POST'])
def character_operations():
    operation = flask.request.form.get("operation")
    if operation == "upload":
        return handle_upload()
    
def handle_upload():
    fileobj = flask.request.files.get('file')
    if not fileobj.filename:
        return flask.abort(400)

    # Unpack and save file
    filename = fileobj.filename
    path = save_file(fileobj, filename)

    page_id = flask.request.form.get('page_id')

    connection = ttrpg.model.get_db()

    connection.execute(
        "INSERT INTO Boxes (page_id, show_all_players, box_title) "
        "VALUES (?, 1, ?) ",
        (page_id, str(path).split('/')[-1])
    )

    box_with_id = connection.execute(
        "SELECT b.box_id "
        "FROM Boxes b "
        "WHERE b.page_id = ? AND b.box_title = ? ",
        (page_id, str(path).split('/')[-1])
    ).fetchone()

    box_id = box_with_id["box_id"]

    connection.execute(
        "INSERT INTO Images (box_id, image_file) "
        "VALUES (?, ?) ",
        (box_id, str(path))
    )
    return flask.redirect(flask.request.args.get("target", "/"))

def save_file(file, filename):
    """Save file."""
    stem = uuid.uuid4().hex
    suffix = pathlib.Path(filename).suffix.lower()
    uuid_basename = f"{stem}{suffix}"
    path = ttrpg.app.config["UPLOAD_FOLDER"] / uuid_basename
    file.save(path)
    return path