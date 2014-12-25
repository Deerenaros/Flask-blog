from flask import redirect, abort, request, session
from flask.ext.login import current_user, login_required, login_user, logout_user
from datetime import datetime
import json, requests

from app import *
from models import *
from forms import *
from usefull import *

from sqlalchemy.exc import IntegrityError

APP_ID = "4686567"
SECRET = "f9CWp3eRmepC3gjzxKx1"
VK = "https://oauth.vk.com"
PERMS = "email,nohttps"
REDIRECT = "http://vesn.info/vk_auth"
RESP = "code"
VER = "5.27"

log_url = "%s/authorize?client_id=%s&scope=%s&redirect_uri=%s&response_type=%s&v=%s"
auth_url = "%s/access_token?client_id=%s&client_secret=%s&code=%s&redirect_uri=%s"


def dd(**kwargs):
	kwargs.update(user=lambda: load_user(session["user"]), is_owning=is_owning)
	return kwargs

@app.route("/login")
def login():
	return redirect(log_url % (VK, APP_ID, PERMS, REDIRECT, RESP, VER))


@app.route("/vk_auth", methods=["GET", "POST"])
def auth():
	code = request.args.get("code")
	print code
	resp = requests.get(auth_url % (VK, APP_ID, SECRET, code, REDIRECT)).json()
	print resp
	if "error_description" in resp:
		return "Authorize failed"
	u = User(token=resp["access_token"], mail=resp["email"], id=resp["user_id"], group="user")
	db.session.add(u)
	db.session.commit()
	session["user"] = u.id
	return redirect("/")


@app.route("/", methods=["GET", "POST"])
@app.route("/index", methods=["GET", "POST"])
@app.route("/posts", methods=["GET", "POST"])
@templated("index.html")
def index():
	"""
	This function had been connected with flask's router by decorating itself with 'app.route'. While decorated
	flask tranlsates all parameters from url (with syntax: '/some/url/<parameter>') into function
	arguments (right here function does not have any paramaters) while calling.
	Also it decorated with templating decorator, which do dirty work (call render_template with putting into
	arguments from ddionary if nessesary and other).

	index() just render main page with posts on them and login form, and, if it's POST request right now, validating
	form and checking user's password.
	@rtype: dd
	@return: return a python's ddionary (map structure) with parameters in dd items, which would be translated
	into jinja templater.
	"""
	return dd(title="Home", posts=reversed(Post.query.all()))


@app.route("/users")
@templated("users.html")
@admin_required
def list_users():
	"""
	Just listing users
	@return: ddionary with key 'users' pointing on iterable object through all users.
	"""
	return dd(title="Userlist", users=User.query.all())


@app.route("/users/<mail>")
@templated("user.html")
@admin_required
def view_user(mail):
	"""
	Just more info about user
	@type mail: basestring
	@param mail: Here is a example, how url parametring works.
	@return: dd with 'user' key pointing to requests user or aborting with default 404 error page returning.
	"""
	u = User.query.get(mail)
	if u is None:
		abort(404)
	return dd(user=u)


@app.route("/signup", methods=["GET", "POST"])
@templated("signup.html")
def signup_user():
	"""
	Signup-page with validating on POST request and commiting new user if all data is valid.
	@return: If validated and signed up - redirecting to index-page, if trying to add existing user,
	refresh page with message, otherwise - rendiring page with form (like simply GET request).
	"""
	return "Do not work"
	form = RegForm()
	try:
		if form.validate_on_submit():
			user = User(grup="user", regd=datetime.now())
			form.populate_obj(user)
			db.session.add(user)
			db.session.commit()
			return redirect("/index")
		return dd(title="Tell us about you...", form=form)
	except IntegrityError:
		return dd(title="Tell us about you...", form=form, message="User with such email already exists")


@app.route("/users/<mail>", methods=["DELETE"])
@templated("user.html")
@admin_required
def del_user(mail):
	"""
	Try delete a user
	@param mail: with this mail.
	@return: "OK"
	"""
	try:
		u = User.query.get(mail)
		if u is not None:
			db.session.delete(u)
			db.session.commit()
		else:
			return "NOT EXISTS"
		return "OK"
	except:
		return "FAIL"


@app.route("/posts/<id>")
@templated("view.html")
def view_post(id):
	"""
	View full post
	@param id: with this id.
	@return: if post does not exists - abort to 404 page, otherwise - rendiring view.html template.
	"""
	viewing = Post.query.get(id)
	if viewing is None:
		abort(404)
	return dd(post=viewing)


@app.route("/manage/<id>", methods=["DELETE"])
@owning_required
def del_post(id):
	"""
	Try delete a post
	@param id: with this id.
	@return: redirect to /index page.
	"""
	try:
		deleting = Post.query.get(id)
		if deleting is not None:
			db.session.delete(deleting)
			db.session.commit()
		else:
			return "NOT EXISTS"
		return "OK"
	except:
		return "FAIL"


@app.route("/manage/<id>", methods=["GET", "POST"])
@templated("manage.html")
@owning_required
def edit_post(id):
	"""
	On GET view entry filled up to form, on POST - refreshing exists object (if post do not exists must
	fail on owning check).
	@return: redirect to /index while edited or rendiring manage.html with filled up entry to a form.
	"""
	editing = Post.query.get(id)
	if editing is None:
		abort(404)
	form = PostForm(obj=editing)
	if form.validate_on_submit():
		form.populate_obj(editing)
		db.session.commit()
		return redirect("/index")
	return dd(title="Edit exists post", btn="Change", form=form)


@app.route("/manage", methods=["GET", "POST"])
@templated("manage.html")
#@login_required
def create_post():
	"""
	Just like edit_post but with empty post and creating new on POST (if form validated).
	@return: redirect to index on POST if success, otherwise - rendiring manage.html with clear form.
	"""
	form = PostForm()
	if form.validate_on_submit():
		creating = Post(time=datetime.now())
		creating.user_mail = current_user.mail
		form.populate_obj(creating)
		db.session.add(creating)
		db.session.commit()
		return redirect("/index")
	return dd(title="Create new post", btn="Post", form=form)


@app.route("/logout")
@login_required
def logout():
	"""
	...hm, obviously - logout current user
	@return: redirect to /index page.
	"""
	session["user"] = None
	return redirect("/index")
