"""REST API for homepage (/.)"""
import flask
import ttrpg


@ttrpg.app.route('/api/v1/')
def get_v1():
    """Return a list of services available."""
    context = {
        
    }
    return flask.jsonify(**context)