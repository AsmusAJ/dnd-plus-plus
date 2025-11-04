"""REST API for Invalid api usage."""
import flask
import ttrpg


class InvalidAPIUsage(Exception):
    """Invalid API Usage."""

    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        """Init."""
        super().__init__()
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        """Message."""
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

@ttrpg.app.errorhandler(InvalidAPIUsage)
def abort_if_wrong_credentials(e):
    """Error checking for wrong credentials."""
    return flask.jsonify(error=str(e)), e.status_code