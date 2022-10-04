import pymysql


def get_connection():
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='Ilya468279135',
                                 db='polyclinic',
                                 charset='utf8mb4', )
    return connection


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
        return rows
    except Exception as ex:
        print(ex)
    finally:
        cursor.close()


def setData(query):
    try:
        connection = pymysql.connect(host='localhost',
                                     user='root',
                                     password='Ilya468279135',
                                     db='polyclinic',
                                     charset='utf8mb4', )
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()
    except Exception as ex:
        print(ex)
    finally:
        cursor.close()
