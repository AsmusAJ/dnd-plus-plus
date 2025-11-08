"""Init."""
import flask

app = flask.Flask(__name__)

app.config.from_object('ttrpg.config')

app.config.from_envvar('TTRPG_SETTINGS', silent=True)

import ttrpg.views  # noqa: E402  pylint: disable=wrong-import-position
import ttrpg.model  # noqa: E402  pylint: disable=wrong-import-position
import ttrpg.api  # noqa: E402  pylint: disable=wrong-import-position
