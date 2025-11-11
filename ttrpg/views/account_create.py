import flask
import ttrpg


@ttrpg.app.route('/accounts/create/')
def show_accounts_create():
    if 'username' in flask.session:
        return flask.redirect("/accounts/edit/")

    context = {

    }

    return flask.render_template("account_create.html", **context)