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
        return "User not found"


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
            pass
    else:
        return "Login is exist"
