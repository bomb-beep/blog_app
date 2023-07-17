from .db import get_db
from werkzeug.security import generate_password_hash,check_password_hash

def add_user(name,password,admin = 0):
	try:
		db = get_db()
		db.execute("INSERT INTO brukere (brukernavn, passord, er_admin) VALUES (?,?,?)",
					(name,generate_password_hash(password),admin))
		db.commit()
	except db.IntegrityError:
		return f"Username {name} is already registered"
	else:
		return None
	
def set_admin(id,admin):
	print(admin,id)
	db = get_db()
	db.execute("UPDATE brukere SET er_admin = ? WHERE id = ?",(admin,id))
	db.commit()
    
def login_user(name,password):
	user = get_db().execute("SELECT * FROM brukere "
							"WHERE brukernavn = ?",
							(name,)).fetchone()
	if user is None:
		return "Incorrect username"
	if check_password_hash(user["passord"],password):
		return user
	else:
		return "Incorrect password"
	
def get_user(id):
	user = get_db().execute(
		"SELECT * FROM brukere "
		"WHERE id = ?",
		(id,)
	).fetchone()
	return user

def get_user_from_name(name):
	user = get_db().execute(
		"SELECT * FROM brukere "
		"WHERE brukernavn = ?",
		(name,)
	).fetchone()
	return user