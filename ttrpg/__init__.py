"""Init."""
import flask

app = flask.Flask(__name__)

app.config.from_object('ttrpg.config')

app.config.from_envvar('TTRPG_SETTINGS', silent=True)
