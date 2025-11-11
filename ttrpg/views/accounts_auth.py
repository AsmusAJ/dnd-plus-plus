import flask
import ttrpg


@ttrpg.app.route('/accounts/auth/')
def accounts_auth():
    """Authorize account."""
    # Connect to database
    if 'username' in flask.session:
        return flask.Response(status="200")

    return flask.abort(403)