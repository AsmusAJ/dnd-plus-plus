"""REST API for homepage (/.)"""
import flask
import ttrpg


@ttrpg.app.route('/api/v1/')
def get_v1():
    """Return a list of services available."""
    context = {
        "comments": "/api/v1/comments/",
        "likes": "/api/v1/likes/",
        "posts": "/api/v1/posts/",
        "url": "/api/v1/"
    }
    return flask.jsonify(**context)