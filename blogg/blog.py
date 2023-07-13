from flask import (Blueprint,g,request,flash,render_template,redirect,url_for,abort)
from backend.blog import get_all_posts,add_post,get_post,get_comments_from_post,add_comment
from blogg.auth import login_required,admin_required

bp = Blueprint("blog",__name__,"/blog")

@bp.route("/")
def index():
    return render_template("blog/index.html",posts = get_all_posts())

@bp.route("/<int:id>",methods=("GET",))
def show_post(id):
	post = get_post(id)
	comments = get_comments_from_post(id)
	if not post:
		return abort(404,f"Post {id} does not exist")

	return render_template("blog/show_post.html",post=post,comments=comments)

@bp.route("/create",methods=("GET","POST"))
@admin_required
def create():
	if request.method == "POST":
		title = request.form["title"]
		body = request.form["body"]
		error = None
		
		if not title:
			error = "Title required"
		
		if not error:
			add_post(title,body,g.user)

			return redirect(url_for("index"))
		else:
			flash(error)

	return render_template("blog/create.html")

@bp.route("/<int:id>/comment",methods=("GET","POST"))
@login_required
def create_comment(id):
	post = get_post(id)
	if request.method=="POST":
		body=request.form["body"]
		error=None

		if not body:
			error = "No content"

		if not error:
			add_comment(body,post,g.user)

			return redirect(url_for("blog.show_post",id=id))
		else:
			flash(error)
	return render_template("blog/create_comment.html",post=post)

@bp.route("/update/<int:id>")
@login_required
def update(id):
	pass