from flask import flash, render_template, request, redirect, url_for
from flask_login import (
    LoginManager,
    login_required,
    login_user,
    logout_user,
)
from login import app, db
from login.models import User


login_manager = LoginManager()
login_manager.__init__(app)
login_manager.login_view = "login_page"


def add_user(username: str, password: str) -> None:
    user = User(username=username, password=password)
    db.session.add(user)
    db.session.commit()
    flash("User is created")


@app.route("/")
@app.route("/index.html")
def index() -> str:
    return render_template("index.html")


@app.route("/dashboard")
@login_required
def dashboard() -> str:
    return render_template("dashboard.html")


@app.route("/login", methods=["GET", "POST"])
def login_page() -> str:
    if request.method == "POST" and "username" in request.form:
        user = User.query.filter_by(
            username=request.form.get("username")
        ).first()
        if user:
            if user.password == request.form.get("password"):
                login_user(user)
                return redirect(url_for("dashboard"))
        return "Invalid username or password"
    return render_template("login.html")


@app.route("/logout")
@login_required
def logout_page() -> str:
    logout_user()
    return redirect(url_for("index"))


@app.route("/create_user", methods=["GET", "POST"])
def create_user() -> str:
    if request.method == "POST" and "username" in request.form:
        username = request.form.get("username")
        password = request.form.get("password")
        add_user(username, password)
    return render_template("create_user.html")


@login_manager.user_loader
def load_user(user_id: str):
    return User.query.get(int(user_id))
