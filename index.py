from flask import render_template, request
from flask_login import LoginManager, login_required, logout_user, login_user

import admin
from config import MyApp
from database import find_by_id, User, save

app = MyApp.app
database = MyApp.database
babel = MyApp.babel
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "/login"


@login_manager.user_loader
def load_user(user_id):
    return find_by_id(User, user_id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return login()


@babel.localeselector
def get_locale():
    return "ru"


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = User.find_by_username(username)
        if user and user.check_password(password):
            login_user(user, remember=True)
            return index()
    return render_template("login.html")


@app.route("/registration", methods=["POST", "GET"])
def registration():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        password_again = request.form.get("password_again")
        user = User.find_by_username(username)
        if user is None and password == password_again:
            user = User(username=username)
            user.set_password(password)
            save(user)
            login_user(user, remember=True)
            return index()
    return render_template("registration.html")


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == '__main__':
    database.create_all()
    admin.config()
    app.run()
