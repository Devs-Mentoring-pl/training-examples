from flask import (
    render_template, redirect, url_for,
    Blueprint, request, session
)

login_blueprint = Blueprint("login", __name__)
dashboard_blueprint = Blueprint("dashboard", __name__)
logout_blueprint = Blueprint("logout", __name__)


@login_blueprint.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        nickname = request.form.get("nickname")
        if nickname:
            session.permanent = True
            session["nick"] = nickname
            return redirect(url_for("dashboard.dashboard_page"))
    return render_template("login.html")


@dashboard_blueprint.route("/dashboard")
def dashboard_page():
    if "nick" not in session:
        return redirect(url_for("login.login"))
    return render_template("dashboard.html")


@logout_blueprint.route("/logout")
def logout():
    session.pop("nick", None)
    return redirect(url_for("login.login"))
