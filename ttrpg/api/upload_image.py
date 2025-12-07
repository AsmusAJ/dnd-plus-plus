import flask
import uuid
import pathlib
import ttrpg

@ttrpg.app.route('/api/v1/upload_image', methods=['POST'])
def upload_image():
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

    box_id = flask.request.form.get('box_id')

    connection = ttrpg.model.get_db()

    print(f"box id = {box_id}")
    print(f"image file = {str(path)}")
    cursor = connection.execute(
        "UPDATE Images "
        "SET image_file = ? " 
        "WHERE box_id = ?",
        (path, box_id,)
    )
    if cursor.rowcount == 0:  # No row was updated! Insert new.
        connection.execute(
            "INSERT INTO Images (box_id, image_file) VALUES (?, ?)",
            (box_id, path)
        )
    return flask.redirect(flask.request.args.get("target", "/"))

def save_file(file, filename):
    """Save file."""
    stem = uuid.uuid4().hex
    suffix = pathlib.Path(filename).suffix.lower()
    uuid_basename = f"{stem}{suffix}"
    path = ttrpg.app.config["UPLOAD_FOLDER"] / uuid_basename
    file.save(path)
    return uuid_basename

@ttrpg.app.route('/uploads/<filename>')
def uploaded_image_route(filename):
    return flask.send_from_directory(
        ttrpg.app.config["UPLOAD_FOLDER"],
        filename
    )
