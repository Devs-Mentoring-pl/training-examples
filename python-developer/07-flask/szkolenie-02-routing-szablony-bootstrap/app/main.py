from flask import Blueprint, render_template

welcome_blueprint = Blueprint('welcome', __name__)
goodbye_blueprint = Blueprint('goodbye', __name__)


@welcome_blueprint.route('/')
def welcome():
    return render_template("welcome.html")


@goodbye_blueprint.route('/goodbye')
def goodbye():
    return render_template("goodbye.html")
