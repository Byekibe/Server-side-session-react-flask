import mysql.connector
from mysql.connector import errorcode
from dotenv import load_dotenv
load_dotenv()
import os

user=os.getenv("USER")
host = os.getenv("HOST")
password = os.getenv("PASSWORD")
database = os.getenv("DATABASE")

def connect_mysql():
    try:
        conn = mysql.connector.connect(user=user, host=host, password=password, database=database)
        print("Connected successfully")
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    return conn

def insert_to_db(cursor, conn, first_name, last_name, email, hashed_password):
    sql_command = "INSERT INTO Users (firstName, lastName, email, password) VALUES(%s, %s, %s, %s)"
    values = (first_name, last_name, email, hashed_password)

    cursor.execute(sql_command, values)

    conn.commit()

    print(cursor.rowcount, "record inserted.")


def login_to_app(cursor, email):
    sql_command = "SELECT * FROM Users WHERE email=%s"
    value = [email]
    cursor.execute(sql_command, value)
    if cursor is not None:
        data = cursor.fetchone()

    return {"user": data}
