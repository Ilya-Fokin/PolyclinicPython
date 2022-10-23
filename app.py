import flask_login
from flask import Flask
from flask import session, redirect, request, url_for, render_template
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from Validation import *
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date

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
            return redirect(f"""/doctor/{current_user.get_id()}""")
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
            if user:
                if check_password_hash(user.password, request.form.get("password")):
                    user_cor = {'id': user.id, 'login': user.login, 'password': user.password, 'role': user.role}
                    user_login = UserLogin().create(user_cor)
                    login_user(user_login)
                    print(current_user.get_id())
                    print("Вход выполнен")
                    return redirect("/")
                else:
                    return render_template("login.html", error="Invalid login or password")
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
    list_specialization = database.getAllSpecializations()
    message = None
    if request.method == 'GET' and database.getRoleUser(current_user.get_id()) == 'admin':
        return render_template('registration.html', list_specialization=list_specialization)
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
            if request.form.get('full_name') and request.form.get('experience') and request.form.get(
                    'specialization') != "Not Selected":
                result = database.createDoctor(request.form.get("login"),
                                               generate_password_hash(request.form.get("password")),
                                               request.form.get("full_name").title(),
                                               request.form.get("specialization"),
                                               request.form.get("experience"))
                print(result)
                if result is True:
                    return redirect("/")
                else:
                    return render_template("registration.html", list_specialization=list_specialization, message=result)
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
    else:
        return redirect("/")

@app.route('specialists/<specialization>')
def showAllSpecialists(specialization):
    if request.method == 'GET' and database.getRoleUser(current_user.get_id()) == 'admin':
        list_doctors = database.get_all_specialists(specialization)
        if list_doctors:
            return render_template("")

@app.route("/patients")
def patients():
    if database.getRoleUser(current_user.get_id()) == 'admin':
        list_patients = database.get_all_patients()
        return render_template("patients.html", list_patients=list_patients)
    else:
        return redirect("/")


@app.route("/add_patient", methods=['POST', 'GET'])
def add_patient():
    if request.method == 'GET' and database.getRoleUser(current_user.get_id()) == 'admin':
        return render_template("add_patient.html")
    if request.method == 'POST' and database.getRoleUser(current_user.get_id()) == 'admin':
        if request.form.get("full_name") and request.form.get("date_of_birth") and request.form.get("address"):
            date_of_birth = database.convertDate(request.form.get("date_of_birth"))
            database.create_patient(request.form.get("full_name"), request.form.get("date_of_birth"),
                                    request.form.get("address"))
            return redirect("/patients")
        else:
            return render_template("add_patient.html", error="Fill in all fields")
    else:
        return redirect("/")


@app.route("/doctor/<id>")
def doctor_page(id):
    if database.getRoleUser(current_user.get_id()) == 'admin' or database.getRoleUser(
            current_user.get_id()) == 'doctor':
        doctor = database.get_doctor_by_id(id)
        if doctor:
            return render_template("doctor_page.html", doctor=doctor, current_id=current_user.get_id())
        else:
            return redirect("/")


@app.route("/add_work_schedule/", methods=['POST', 'GET'])
def add_work_schedule(id):
    if request.method == 'GET' and (database.getRoleUser(current_user.get_id()) == 'admin' or database.getRoleUser(
            current_user.get_id()) == 'doctor'):
        return render_template("add_work_shedule.html")


@app.route("/work_schedule/<doctor_id>", methods=['POST', 'GET'])
def work_schedule(doctor_id):
    if request.method == 'GET' and (database.getRoleUser(current_user.get_id()) == 'admin' or database.getRoleUser(
            current_user.get_id()) == 'doctor'):
        doctor = database.get_doctor_by_doctor_id(doctor_id)
        list_schedule = database.get_all_doctor_schedule(doctor_id)
        if doctor:
            return render_template("work_schedule.html", doctor=doctor, list_schedule=list_schedule)
    if request.method == 'POST' and (database.getRoleUser(current_user.get_id()) == 'admin' or database.getRoleUser(
            current_user.get_id()) == 'doctor'):
        if request.form.get("date") and request.form.get("start_time") and request.form.get("finish_time"):
            database.add_work_schedule(doctor_id, request.form.get("date"), request.form.get("start_time"), request.form.get("finish_time"))
            return redirect(f"""/work_schedule/{doctor_id}""")
        else:
            return render_template("work_schedule.html", error="Invalid date of time")
    else:
        return redirect(f"""/work_schedule/{doctor_id}""")


if __name__ == '__main__':
    app.run()
