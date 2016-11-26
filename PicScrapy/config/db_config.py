from peewee import *
import sqlite3
import os

db_path = os.path.join(os.path.dirname(__file__),os.pardir,os.pardir,'pic.db')
print (db_path)

def get_db():

    return SqliteDatabase(db_path)
    #return PostgresqlDatabase('PicScrapy',host='127.0.0.1',port=5432,user='postgres',password='1234567a')

def get_sqlite_db():
    return sqlite3.connect(db_path)