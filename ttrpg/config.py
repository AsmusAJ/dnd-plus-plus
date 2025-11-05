"""TTRPG development configuration."""

import pathlib

# Root
APPLICATION_ROOT = '/'

# Secret key for encrypting cookies
SECRET_KEY = (b'\x8d\xecH\xb8\x85wp\x82\x04\xa0\x8eH4\xa5\xdb\xd1\xe9jFO[\x9bY#')
SESSION_COOKIE_NAME = 'login'

# File Upload to var/uploads/
TTRPG_ROOT = pathlib.Path(__file__).resolve().parent.parent
UPLOAD_FOLDER = TTRPG_ROOT/'var'/'uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg',])
MAX_CONTENT_LENGTH = 16 * 1024 * 1024

# Database file is var/ttrpg.sqlite3
DATABASE_FILENAME = TTRPG_ROOT/'var'/'ttrpg.sqlite3'
