import sqlite3
from backend.db import get_db,init_db
from backend.auth import add_user,login_user
from backend.blog import *

print("Backend Test\n")
    
print("Init test database")
init_db()
print("Connecting to database\n")
db = get_db()
assert type(db) == sqlite3.Connection

print("Adding new user 'sjef'")
add_user("sjef","passord123",1)
print(list(db.execute("SELECT * FROM brukere WHERE id = 1").fetchone()))
print("\nLogging in 'sjef'")
user = login_user("sjef","passord123")
assert user["brukernavn"] == "sjef"
print(user["brukernavn"])

print("Creating post")
add_post("Forste innlegg","Innhold\ninnhold",user)
post = get_post(1)
print(list(post))

print("\nAttempting illeagl post")
add_user("bot","passord123",0)
guest_user = login_user("bot","passord123")
assert guest_user["brukernavn"] == "bot"
add_post("Viktig!!","Kjop her!!",guest_user)
assert get_post(2) == None

print("\nCreating comment")
add_comment("XD XD",post,guest_user)
comment = get_comment(1)
assert comment["innhold"] == "XD XD"
print(list(comment))
