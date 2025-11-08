import flask
import ttrpg

@ttrpg.app.route('/accounts/login/')
def show_accounts_login():
    if 'username' in flask.session:
        return flask.redirect("/")

    context = {}

    return flask.render_template("account_login.html", **context)