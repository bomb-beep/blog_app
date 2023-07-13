import sqlite3
import os

path = os.path.dirname(os.path.dirname(__file__))

def get_db():
	database = sqlite3.connect(path+"\\instance\\database.sqlite")
	database.row_factory = sqlite3.Row
	return database

def init_db():
	f = open(path+"\\backend\\schema.sql")
	get_db().executescript(f.read())
	f.close()

# def close_db(e=None):
# 	database.close()

