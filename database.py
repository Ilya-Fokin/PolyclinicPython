from datetime import date, timedelta, datetime

import pymysql

import Models
from Validation import *
from Models import *


def get_cursor():
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='Ilya468279135',
                                 db='polyclinic',
                                 charset='utf8mb4', )
    return connection.cursor()


def getData(query):
    try:
        connection = pymysql.connect(host='localhost',
                                     user='root',
                                     password='Ilya468279135',
                                     db='polyclinic',
                                     charset='utf8mb4', )
        cursor = connection.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        print(rows)
        cursor.close()
        return rows
    except Exception as ex:
        print(ex)


def setData(query):
    global cursor
    try:
        connection = pymysql.connect(host='localhost',
                                     user='root',
                                     password='Ilya468279135',
                                     db='polyclinic',
                                     charset='utf8mb4', )
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()
        print(cursor.fetchall())
        cursor.close()
    except Exception as ex:
        print(ex)


def getUserByIdForLogin(user_id):
    cursor = getUserById(user_id)
    user = Models.User(cursor[0], cursor[1], cursor[2], cursor[3])
    user_cor = {'id': user.id, 'login': user.login, 'password': user.password, 'role': user.role}
    return user_cor


def getUserById(user_id):
    try:
        cursor = get_cursor()
        cursor.execute(f"""select user.id, login, password, role.role from user 
        inner join user_role on user.id = user_id and user.id = '{user_id}' inner join role on role_id = role.id;""")
        res = cursor.fetchone()
        if not res:
            print("User not found")
            return False
        else:
            return res
    except pymysql.Error as e:
        print("MySql Error" + str(e))
    return False


def getUserByLogin(login):
    cursor = get_cursor()
    res = cursor.execute(f"""select user.id, login, password, role.role from user 
            inner join user_role on user.id = user_id and login = '{login}' inner join role on role_id = role.id;""")
    res = cursor.fetchone()
    if res:
        user = Models.User(res[0], res[1], res[2], res[3])
        return user
    else:
        print("User not found")
        return False


def check_user_login(login):
    if getUserByLogin(login) is User:
        print("User is exist")
        return True
    else:
        print("User not found")
        return False


def get_user_id(login):
    res = getData(f"select id from user where login = '{login}'")
    return res[0][0]


def get_role_id(role):
    res = getData(f"select id from role where role = '{role}'")
    return res[0][0]


def createUser(login, password, role):
    if not check_user_login(login):
        if role == 'admin':
            setData(f"""insert into user(login, password) value('{login}', '{password}')""")
            setData(f"""insert into user_role(user_id, role_id) 
            value({get_user_id(login)}, {get_role_id('admin')})""")
            return True
        else:
            if role == 'doctor':
                setData(f"""insert into user(login, password) value('{login}', '{password}')""")
                setData(f"""insert into user_role(user_id, role_id) 
                value({get_user_id(login)}, {get_role_id('doctor')})""")
                return True
    else:
        return "Login is exist"


def getRoleUser(user_id):
    cursor = get_cursor()
    res = cursor.execute(f"""select role from role join user_role on user_id = '{user_id}' and role.id = role_id""")
    res = cursor.fetchone()
    if res:
        return res[0]
    else:
        return False


def checkSpecialties(specialization):
    cursor = get_cursor()
    res = cursor.execute(f"""select * from specialization where specialization = '{specialization}'""")
    res = cursor.fetchone()
    print(res)
    if res:
        print("Specialization is exist")
        return True
    else:
        print("Specialization not exist")
        return False


def addSpecialization(specialization):
    if not (checkSpecialties(specialization)) and validate_full_name(specialization):
        print(specialization)
        setData(f"""insert into specialization(specialization) values ('{specialization}')""")
    else:
        print("Specialization is exist or incorrect word")
        return False


def getAllSpecializations():
    res = getData(f"""select * from specialization""")
    listSpecialization = []
    for elem in res:
        listSpecialization.append(elem[1])
        print(elem[1])
    return listSpecialization


def get_specialization_id(specialization):
    cursor = get_cursor()
    if checkSpecialties(specialization) is True:
        cursor.execute(f"""select id from specialization where specialization = '{specialization}'""")
        id = cursor.fetchone()
        return id[0]
    else:
        return False


def createDoctor(login, password, full_name, specialization, experience):
    if createUser(login, password, 'doctor') is True and validate_full_name(full_name):
        if checkSpecialties(specialization) is True:
            setData(f"""insert into doctor(full_name, specialization_id, experience, user_id) value ('{full_name}', 
            {get_specialization_id(specialization)}, '{experience}', {get_user_id(login)})""")
            return True
        else:
            return "Specialization not exist"
    else:
        return "Error creating user"


def get_doctor_by_id(user_id):
    cursor = get_cursor()
    cursor.execute(f"""select doctor.id, full_name, experience, specialization, user_id 
    from doctor join specialization on specialization.id = specialization_id where doctor.user_id = {user_id};""")
    result = cursor.fetchone()
    if result:
        doctor = {'id': result[0], 'full_name': result[1], 'experience': result[2],
                  'specialization': result[3], 'user_id': result[4]}
        return doctor
    else:
        return False


def get_doctor_by_doctor_id(doctor_id):
    cursor = get_cursor()
    cursor.execute(f"""select doctor.id, full_name, experience, specialization, user_id 
        from doctor join specialization on specialization.id = specialization_id where doctor.id = {doctor_id};""")
    result = cursor.fetchone()
    if result:
        doctor = {'id': result[0], 'full_name': result[1], 'experience': result[2],
                  'specialization': result[3], 'user_id': result[4]}
        return doctor
    else:
        return False


def change_doctor_info(doctor_id, full_name, experience, specialization):
    cursor = get_cursor()
    cursor.execute(f"""select id from specialization where specialization = '{specialization}'""")
    spec = cursor.fetchone()
    doctor = get_doctor_by_doctor_id(doctor_id)
    if doctor:
        setData(f"""update doctor set full_name = '{full_name}', experience = {experience}, 
        specialization_id = {spec[0]} where id = {doctor_id}""")


def add_work_schedule(doctor_id, date_work, start_time, finish_time):
    if check_the_doctor_schedule(doctor_id, date_work):
        delete_work_schedule(doctor_id, date_work)

    period = timedelta(hours=0, minutes=20)
    start_time = datetime.strptime(start_time, '%H:%M')
    finish_time = datetime.strptime(finish_time, '%H:%M')
    times = []
    while start_time <= finish_time:
        times.append(str(start_time))
        start_time += period
    for time in times:
        print(time)
        setData(f"""insert into work_schedule(doctor_id, date, time) value({doctor_id}, "{date_work}", "{time}")""")


def get_all_doctor_schedule(doctor_id):
    result = getData(f"""select id, date, time from work_schedule where doctor_id = {doctor_id}""")
    times = []
    for elem in result:
        times.append({'id': elem[0], 'date': elem[1], 'time': elem[2]})
    return times


def get_all_schedule_today(doctor_id):
    today = date.today()
    result = getData(f"""select work_schedule.id, work_schedule.date, work_schedule.time, doc_appointments.patient_id, patient.full_name 
    from work_schedule left join doc_appointments on work_schedule.doctor_id = doc_appointments.doctor_id 
    and work_schedule.date = doc_appointments.date and work_schedule.time = doc_appointments.time 
    left join patient on doc_appointments.patient_id = patient.id
    where work_schedule.doctor_id = {doctor_id} and work_schedule.date = '{today}'""")
    list_schedule = []
    if result:
        for elem in result:
            list_schedule.append({"id": elem[0], "date": elem[1], "time": elem[2],
                                  "patient_id": elem[3], "patient_name": elem[4]})
    return list_schedule


def check_the_doctor_schedule(doctor_id, date):
    result = getData(f"""select work_schedule.id, work_schedule.date, work_schedule.time, doc_appointments.patient_id, patient.full_name 
    from work_schedule left join doc_appointments on work_schedule.doctor_id = doc_appointments.doctor_id 
    and work_schedule.date = doc_appointments.date and work_schedule.time = doc_appointments.time 
    left join patient on doc_appointments.patient_id = patient.id
    where work_schedule.doctor_id = {doctor_id} and work_schedule.date = '{date}';""")

    times = []
    if result:
        for elem in result:
            times.append(
                {'id': elem[0], 'date': elem[1], 'time': elem[2], 'patient_id': elem[3], 'patient_name': elem[4]})
        return times
    else:
        return times


def get_schedule_by_id(id):
    cursor = get_cursor()
    cursor.execute(f"""select * from work_schedule where id = {id}""")
    result = cursor.fetchone()
    schedule = {}
    if result:
        schedule = {'id': result[0], 'doctor_id': result[1], 'date': result[2], 'time': result[3]}
    return schedule


def get_all_specialists(specialization):
    result = getData(f"""select * from doctor join specialization on doctor.specialization_id = specialization.id 
    and specialization.specialization = '{specialization}'""")
    list_doctors = []
    if result:
        for doctor in result:
            list_doctors.append(
                {'id': doctor[0], 'full_name': doctor[1], 'specialization_id': doctor[2], 'experience': doctor[3],
                 'user_id': doctor[4]})
        return list_doctors
    else:
        return list_doctors


def get_all_doctors():
    result = getData("select * from doctor")
    list_doctors = []
    if result:
        for doctor in result:
            list_doctors.append(
                {'id': doctor[0], 'full_name': doctor[1], 'specialization_id': doctor[2], 'experience': doctor[3],
                 'user_id': doctor[4]})
            print(doctor)
        return list_doctors
    else:
        return list_doctors


def get_all_patients():
    result = getData("select * from patient")
    list_patients = []
    print(result)
    for patient in result:
        list_patients.append(
            {'id': patient[0], 'full_name': patient[1], 'date_of_birth': patient[2], 'address': patient[3]})
        print(patient)
    return list_patients


def get_patient(full_name, date_of_birth):
    cursor = get_cursor()
    cursor.execute(f"""select * from patient where full_name = '{full_name}' and date_of_birth = '{date_of_birth}'""")
    result = cursor.fetchone()
    patient = {}
    if result:
        patient = {'id': result[0], 'full_name': result[1], 'address': result[2]}
    return patient


def add_appointment(patient_id, doctor_id, date, time):
    setData(
        f"""insert into doc_appointments(doctor_id, patient_id, date, time) value({doctor_id}, {patient_id}, '{date}', 
        '{time}')""")


def create_patient(full_name, date_of_birth, address):
    if validate_full_name(full_name):
        setData(f"""insert into patient(full_name, date_of_birth, address) value('{full_name}', 
        '{date_of_birth}', '{address}')""")
    else:
        print("Error validate")


def convertDate(request_date):
    replace_date = str(request_date).split("-")
    date_of_birth = date(int(replace_date[0]), int(replace_date[1]), int(replace_date[2]))
    print(date_of_birth)
    formatted_date = date_of_birth.strftime('%Y-%m-%d')
    return formatted_date


def get_all_diagnoses():
    result = getData(f"""select * from diagnoses""")
    list_diagnoses = []
    for elem in result:
        list_diagnoses.append({'id': elem[0], 'diagnosis': elem[1], 'description': elem[2]})
    return list_diagnoses


def add_diagnosis(diagnosis, description):
    setData(f"""insert into diagnoses(diagnosis, description) value('{diagnosis}', '{description}')""")


def check_diagnosis(diagnosis):
    cursor = get_cursor()
    cursor.execute(f"""select * from diagnoses where diagnosis = '{diagnosis}'""")
    result = cursor.fetchone()
    if result:
        return True
    else:
        return False


def get_appointments(doctor_id, date_appointment=date.today()):
    from datetime import date
    result = getData(f"""select doctor_id, patient_id, patient.full_name, patient.date_of_birth, date, time
    from doc_appointments join doctor on doctor_id = doctor.id join patient on patient.id = patient_id 
    where doctor_id = {doctor_id} and date = '{date_appointment}'""")
    list_appointments = []
    if result:
        for appointment in result:
            list_appointments.append({'doctor_id': appointment[0], 'patient_id': appointment[1],
                                      'full_name': appointment[2], 'date_of_birth': appointment[3],
                                      'date': appointment[4],
                                      'time': appointment[5]})
    return list_appointments


def get_patient_by_id(patient_id):
    cursor = get_cursor()
    cursor.execute(f"""select * from patient where id = {patient_id}""")
    result = cursor.fetchone()
    patient = {}
    if result:
        patient = {"id": result[0], "full_name": result[1], "date_of_birth": result[2], "address": result[3]}
    return patient


def get_all_patient_appointments(patient_id):
    result = getData(f"""select doc_appointments.id, doctor.full_name, specialization.specialization, patient_id, date, time 
    from doc_appointments join doctor on doctor.id = doctor_id join specialization 
    on specialization.id = doctor.specialization_id where patient_id = '{patient_id}';""")
    list_appointments = []
    if result:
        for elem in result:
            list_appointments.append(
                {"id": elem[0], "doctor_name": elem[1], "specialization": elem[2], 'patient_id': elem[3],
                 "date": elem[4], "time": elem[5]})
    return list_appointments


def delete_patient_appointments(id):
    setData(f"""delete from doc_appointments where id = {id}""")


def get_all_diagnoses_patient(patient_id):
    result = getData(f"""select patient_diagnosis.*, doctor.full_name, diagnosis.diagnosis, diagnosis.description 
    from patient_diagnosis. join doctor on patient_diagnosis.doctor_id = doctor.id 
    join patient on patient_diagnosis.patient_id = {patient_id} 
    join diagnosis on diagnosis.id = patient_diagnosis.diagnosis_id""")
    list_diagnosis = []
    if result:
        for elem in result:
            list_diagnosis.append({"id": elem[0], "patient_id": elem[1], "diagnosis_id": elem[2], "doctor_id": elem[3],
                                   "date_time": elem[4], "doctor_name": elem[5], "diagnosis": elem[6]})
    return list_diagnosis


def make_diagnosis(doctor_id, patient_id, *diagnoses):
    date_time = datetime.now()
    for elem in diagnoses:
        print(elem)
        setData(f"""insert into patient_diagnosis(patient_id, diagnosis_id, doctor_id, date_time) value ({patient_id}, 
        {elem}, {doctor_id}, '{date_time}')""")


def delete_work_schedule(doctor_id, date):
    setData(f"""delete from work_schedule where doctor_id = {doctor_id} and date = '{date}'""")


def patient_edit(id, full_name, date_of_birth, address):
    patient = get_patient_by_id(id)
    if patient:
        setData(f"""update patient set full_name = '{full_name}', date_of_birth = '{date_of_birth}', 
        address = '{address}' where id = {id}""")