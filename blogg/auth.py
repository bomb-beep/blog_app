from flask import (Blueprint,g,request,flash,render_template,redirect,url_for,session,abort)
from backend.auth import add_user,login_user,get_user
import functools

bp = Blueprint("auth",__name__,"/auth")

@bp.route("/register",methods=("GET","POST"))
def register():
	if request.method == "POST":
		username = request.form["username"]
		password = request.form["password"]

		error = None
		if not username:
			error = "Username is required"
		elif not password:
			error = "Password is required"

		if not error:
			error = add_user(username,password)

		if not error:
			user = login_user(username,password)
			
			session.clear()
			session["user_id"] = user["id"]
			
			return redirect(url_for("index"))

		flash(error)


	return render_template("auth/register.html")

@bp.route("/login",methods=("GET","POST"))
def login():
	if request.method=="POST":
		username = request.form["username"]
		password = request.form["password"]

		error = None
		if not username:
			error = "Username is required"
		elif not password:
			error = "Password is required"

		user = login_user(username,password)

		if type(user) == str:
			error = user
		else:
			session.clear()
			session["user_id"] = user["id"]

		if not error:
			return redirect(url_for("index"))

		if error:
			flash(error)

	return render_template("auth/login.html")

@bp.route("/logout")
def logout():
	session.clear()

	return redirect(url_for("index"))

@bp.before_app_request
def load_logged_in_user():
	user_id = session.get("user_id")

	if user_id is None:
		g.user = None
	else:
		g.user = get_user(user_id)
		if g.user == None:
			return abort(403)
		
def login_required(view):
	@functools.wraps(view)
	def wrapped_view(**kwargs):
		if g.user is None:
			return abort(401)
		else:
			return view(**kwargs)
		
	return wrapped_view

def admin_required(view):
	@functools.wraps(view)
	def wrapped_view(**kwargs):
		if g.user is None:
			return abort(401)
		elif g.user["er_admin"] == 0:
			return abort(403)
		else:
			return view(**kwargs)
		
	return wrapped_view