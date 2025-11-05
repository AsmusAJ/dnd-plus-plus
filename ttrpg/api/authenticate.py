import hashlib
import flask
import ttrpg

def authenticate():

    if "username" in flask.session:
        return flask.session["username"]

    auth = flask.request.authorization

    if not auth or not auth.username or not auth.password:
        return None

    db_connect = ttrpg.model.get_db()
    user_query = db_connect.execute(
        "SELECT username, password "
        "FROM Users "
        "WHERE usernae = ?",
        (auth.username,)
    )
    user = user_query.fetchone()

    if user: 
        user_db_password = user['password']
        algorithm, salt, db_hash = user_db_password.split('$')

        login_attempt_hash = hashlib.sha512((salt + auth.password).encode()).hexdigest()

        if login_attempt_hash == db_hash:
            # login success
            flask.session["username"] = auth.username
            return auth.username

    return None