from os import environ
import pymysql.cursors
import pymysql
from flask import jsonify, make_response

db_user = "admin"
db_password = "zOn43219!4321"
db_name = "data_modeling_final"
db_connection_name = "104.198.205.204"

def open_connection():
    try:
        conn = pymysql.connect(host=db_connection_name,
            user=db_user,
            password=db_password,
            db=db_name,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor)
    except pymysql.MySQLError as e:
        print(e)

    return conn


def get_salaries():
    conn1 = open_connection()
    with conn1.cursor() as cursor:
        result = cursor.execute('SELECT * FROM Salary;')
        salaries = cursor.fetchall()
        if result > 0:
            got_salaries = jsonify(salaries)
        else:
            got_salaries = 'No Salaries in DB'
    conn1.close()
    return got_salaries

def get_batters():
    conn1 = open_connection()
    with conn1.cursor() as cursor:
        result = cursor.execute('SELECT * FROM Batter;')
        batters = cursor.fetchall()
        if result > 0:
            got_batters = jsonify(batters)
        else:
            got_batters = 'No Batters in DB'
    conn1.close()
    return got_batters

def get_pitchers():
    conn1 = open_connection()
    with conn1.cursor() as cursor:
        result = cursor.execute('SELECT * FROM Pitcher;')
        pitchers = cursor.fetchall()
        if result > 0:
            got_pitchers = jsonify(pitchers)
        else:
            got_pitchers = 'No Pitchers in DB'
    conn1.close()
    return got_pitchers
