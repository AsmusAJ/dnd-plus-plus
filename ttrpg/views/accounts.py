import uuid
import hashlib
import pathlib
import flask
import ttrpg 

@ttrpg.app.route("/accounts/", methods=["POST"])
def accounts():
    """Account management."""
    operation = flask.request.form.get("operation")
    if operation == "login":
        return handle_login()
    if operation == "create":
        return handle_create()
    if operation == "delete":
        return handle_delete()
    if operation == "edit_account":
        return handle_edit_account()
    if operation == "update_password":
        return handle_update_password()

    return flask.abort(400)

def hash_password(password, salt=None):
    """Hash password."""
    algorithm = 'sha512'
    if salt is None:
        salt = uuid.uuid4().hex
    hash_obj = hashlib.new(algorithm)
    password_salted = salt + password
    hash_obj.update(password_salted.encode('utf-8'))
    password_hash = hash_obj.hexdigest()
    return "$".join([algorithm, salt, password_hash])


def handle_login():
    """Handle login."""
    username = flask.request.form.get('username')
    password = flask.request.form.get('password')
    if (not username) or (not password):
        return flask.abort(400)

    # Connect to the database
    connection = ttrpg.model.get_db()

    # get db password for comparison
    post_query = connection.execute(
        "SELECT password "
        "FROM Users "
        "WHERE username = ? ",
        (username, )
    )
    db_password = post_query.fetchone()

    if db_password is None:
        return flask.abort(403)

    _, salt, _ = db_password['password'].split('$')
    computed_hash = hash_password(password, salt)

    if computed_hash != db_password['password']:
        return flask.abort(403)

    # session cookie
    flask.session['username'] = username
    return flask.redirect(flask.request.args.get("target", "/"))


def handle_create():
    """Handle create."""
    username = flask.request.form.get('username')
    password = flask.request.form.get('password')
    email = flask.request.form.get('email')
    fileobj = flask.request.files.get('file')
    
    if (not username) or (not password) or (not email):
        return flask.abort(400)
    
    path = "None"
    if fileobj:
        filename = fileobj.filename
        path = save_file(fileobj, filename)

    password_hash = hash_password(password)
    connection = ttrpg.model.get_db()
    connection.execute(
        "INSERT INTO Users (username, email, pfp_filename, password) "
        "VALUES (?, ?, ?, ?) ",
        (username , email, str(path), password_hash)
    )
    flask.session['username'] = username
    return flask.redirect(flask.request.args.get("target", "/"))


def save_file(file, filename):
    """Save file."""
    stem = uuid.uuid4().hex
    suffix = pathlib.Path(filename).suffix.lower()
    uuid_basename = f"{stem}{suffix}"
    path = ttrpg.app.config["UPLOAD_FOLDER"] / uuid_basename
    file.save(path)
    return path


def handle_delete():
    """Handle delete."""
    if 'username' not in flask.session:
        return flask.abort(403)

    connection = ttrpg.model.get_db()
    connection.execute(
        "DELETE FROM Users "
        "WHERE username = ? ",
        (flask.session.get('username'), )
    )
    
    flask.session.clear()
    return flask.redirect(flask.request.args.get("target", "/"))


def handle_edit_account():
    """Handle editing account."""
    if 'username' not in flask.session:
        return flask.abort(403)

    email = flask.request.form.get('email')
    fileobj = flask.request.files.get('file')
    if (not email):
        return flask.abort(400)

    connection = ttrpg.model.get_db()
    if fileobj:
        filename = fileobj.filename
        path = save_file(fileobj, filename)
        connection.execute(
            "UPDATE users "
            "SET email = ?, pfp_filename = ? "
            "WHERE username = ? ",
            (email, path.name, flask.session.get('username'), )
        )
    else:
        connection.execute(
            "UPDATE users "
            "SET email = ? "
            "WHERE username = ? ",
            (email, flask.session.get('username'), )
        )
    return flask.redirect(flask.request.args.get("target", "/"))


def handle_update_password():
    """Handle updating password."""
    if 'username' not in flask.session:
        return flask.abort(403)

    username = flask.session['username']
    password = flask.request.form.get('password')
    new_password1 = flask.request.form.get('new_password1')
    new_password2 = flask.request.form.get('new_password2')

    if not all([username, password, new_password1, new_password2]):
        return flask.abort(400)

    if new_password1 != new_password2:
        return flask.abort(401)

    connection = ttrpg.model.get_db()

    post_query = connection.execute(
        "SELECT password "
        "FROM Users "
        "WHERE username = ? ",
        (username, )
    )
    db_password = post_query.fetchone()

    if db_password is None:
        return flask.abort(403)

    _, salt, _ = db_password['password'].split('$')
    computed_hash = hash_password(password, salt)

    if computed_hash != db_password['password']:
        return flask.abort(403)

    new_password_hash = hash_password(new_password1)
    connection.execute(
        "UPDATE Users "
        "SET password = ? "
        "WHERE username = ? ",
        (new_password_hash, username)
    )
    return flask.redirect(flask.request.args.get("target", "/"))
