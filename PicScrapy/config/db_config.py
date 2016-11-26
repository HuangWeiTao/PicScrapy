from peewee import *
import sqlite3

def get_db():
    return SqliteDatabase('C:\Users\Ken\PycharmProjects\PicScrapy\pic.db')
    #return PostgresqlDatabase('PicScrapy',host='127.0.0.1',port=5432,user='postgres',password='1234567a')

def get_sqlite_db():
    return sqlite3.connect('C:\Users\Ken\PycharmProjects\PicScrapy\pic.db')