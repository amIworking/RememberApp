import sqlite3
from sqlite3 import Error

def create_connect(path):
    connection = None
    try:
        connection = sqlite3.connect(path)
        print("Connection was successful")
    except Error as e:
        print(f"{e}")
    return connection

