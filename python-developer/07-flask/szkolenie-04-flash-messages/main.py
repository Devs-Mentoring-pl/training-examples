from flask import Flask, flash, redirect, url_for, render_template, request, session

app = Flask(__name__)
app.secret_key = "super_tajny_klucz"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username == "admin" and password == "haslo123":
            if "logged_in" in session:
                flash("Jesteś już zalogowany!", "warning")
                return redirect(url_for("dashboard"))

            session["logged_in"] = True
            session["username"] = username
            flash("Zalogowano pomyślnie!", "success")
            return redirect(url_for("dashboard"))
        else:
            flash("Nieprawidłowa nazwa użytkownika lub hasło!", "danger")
            return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/dashboard")
def dashboard():
    if "logged_in" not in session:
        flash("Musisz się najpierw zalogować!", "warning")
        return redirect(url_for("login"))
    return render_template("dashboard.html", username=session["username"])


@app.route("/logout")
def logout():
    if "logged_in" in session:
        session.pop("logged_in", None)
        session.pop("username", None)
        flash("Wylogowano pomyślnie!", "success")
    else:
        flash("Nie jesteś zalogowany!", "warning")
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
