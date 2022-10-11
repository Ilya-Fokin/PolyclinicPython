import flask_login
from flask import Flask
from flask import session, redirect, request, url_for, render_template
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from Validation import *
from werkzeug.security import generate_password_hash, check_password_hash

import Models
from UserLogin import UserLogin

import database

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
login_manager = LoginManager(app)


@app.route('/')
def index():
    if current_user.get_id():
        if database.getRoleUser(current_user.get_id()) == 'admin':
            return render_template("indexAdmin.html")
    else:
        return redirect("/login")


@login_manager.user_loader
def load_user(login):
    return UserLogin().fromDB(login)


@app.route('/login', methods=['POST', 'GET'])
def login():
    if not current_user.get_id():
        if request.method == 'GET':
            return render_template('login.html')
        if request.method == 'POST':
            user = database.getUserByLogin(request.form.get("login"))
            if user and check_password_hash(user.password, request.form.get("password")):
                user_cor = {'id': user.id, 'login': user.login, 'password': user.password, 'role': user.role}
                user_login = UserLogin().create(user_cor)
                login_user(user_login)
                print(current_user.get_id())
                print("Вход выполнен")
                return redirect("/")
            else:
                return render_template("login.html", error="Invalid login or password")
        return redirect("/")
    else:
        return redirect("/")


@app.route('/logout')
@login_required
def logout():
    if current_user.get_id():
        logout_user()
        print("Logout success")
        return redirect("/login")
    else:
        return redirect("/")


@app.route('/registration', methods=['POST', 'GET'])
def registration():
    if request.method == 'GET' and database.getRoleUser(current_user.get_id()) == 'admin':
        return render_template('registration.html')
    if request.method == 'POST' and database.getRoleUser(current_user.get_id()) == 'admin':
        # Проверка пароля на его сложность
        if validate_password(request.form.get("password")) is True:
            # Если поля Имя/Фамилия, опыт и специальность не введены, создаем админа
            if request.form.get('full_name') == "" and request.form.get('experience') == "" and request.form.get(
                    'specialization') == "Not Selected":
                print("Creating admin...")
                res = database.createUser(request.form.get("login"),
                                          generate_password_hash(request.form.get("password")), "admin")
                if res is True:
                    return redirect("/")
                else:
                    return render_template("registration.html", message=res)
            else:
                pass
        else:
            return render_template("registration.html", message="Incorrect password (a-z, A-Z, >8)")
    return redirect("/")


@app.route('/specialists')
def specialists():
    if database.getRoleUser(current_user.get_id()) == 'admin':
        return render_template("specialist.html", listSpecialization=database.getAllSpecializations())
    else:
        return redirect("/")


@app.route('/add_specialties', methods=['POST', 'GET'])
def addSpecialties():
    if request.method == 'GET' and database.getRoleUser(current_user.get_id()) == 'admin':
        return render_template('add_specialties.html')
    if request.method == 'POST' and database.getRoleUser(current_user.get_id()) == 'admin':
        if not database.checkSpecialties(request.form.get("specialization")):
            database.addSpecialization(request.form.get("specialization").title())
            return redirect("/specialists")
        else:
            return render_template("add_specialties.html", error="Specialization is exist")


if __name__ == '__main__':
    app.run()
