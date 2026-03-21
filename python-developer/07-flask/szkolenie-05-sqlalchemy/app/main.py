from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from . import db
from .models import User

main_bp = Blueprint("main", __name__)


@main_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")

        existing_user = User.query.filter_by(name=name).first()

        if existing_user:
            session["user_id"] = existing_user.id
            flash("Zalogowano pomyślnie!", "success")
        else:
            try:
                new_user = User(name=name, email=email)
                db.session.add(new_user)
                db.session.commit()
                session["user_id"] = new_user.id
                flash("Konto utworzone i zalogowano!", "success")
            except Exception:
                db.session.rollback()
                flash("Wystąpił błąd przy tworzeniu konta.", "danger")
                return redirect(url_for("main.login"))

        return redirect(url_for("main.dashboard"))

    return render_template("login.html")


@main_bp.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    user_id = session.get("user_id")
    if not user_id:
        flash("Musisz się zalogować.", "warning")
        return redirect(url_for("main.login"))

    user = db.session.get(User, user_id)

    if request.method == "POST":
        new_email = request.form.get("email")
        if new_email:
            user.email = new_email
            db.session.commit()
            flash("Email zaktualizowany!", "success")

    return render_template("dashboard.html", user=user)


@main_bp.route("/logout")
def logout():
    session.pop("user_id", None)
    flash("Wylogowano.", "info")
    return redirect(url_for("main.login"))
