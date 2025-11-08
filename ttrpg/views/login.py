import flask
import ttrpg

@ttrpg.app.route('/login/', methods=['POST'])
def login():
    """Account login."""
    flask.session['username'] = flask.request.form['username']
    return flask.redirect('/')