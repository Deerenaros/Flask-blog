from functools import wraps
from flask import request, render_template, redirect, abort, session
from flask.ext.login import current_user

from app import *
from models import *

def user(__set=""):
	if __set != "":
		session["user"] = __set
		return None
	if user in session:
		return load_user(session["user"])
	return None

def load_user(userid):
	"""
	This function requered by flask user manager extension, which help on managing user (cookies, ip, authintication,
	and remembering). Need to connect with database.
	@param userid: flask's user id
	@return: Object connected with user id.
	"""
	return User.query.get(userid)


def templated(template=None):
	"""
	Simply but helpfull decorator, wich provide one-string way to declarate template, which must be rendered.
	@param template: template's name, if None - would take from router's path.
	@return: rendered page or something else, if decorated function return not a dict.
	"""
	def decorator(f):
		@wraps(f)
		def decorated_function(*args, **kwargs):
			name = template
			if name is None:
				name = request.endpoint.replace('.', '/') + '.html'
			ctx = f(*args, **kwargs)
			if ctx is None:
				ctx = dict()
			elif not isinstance(ctx, dict):
				return ctx
			return render_template(name, **ctx)
		return decorated_function
	return decorator


def is_owning(user, post):
	"""
	Very simply function which just check, is 'post' owning by 'user'
	@return: just boolean
	"""
	try:
		if user.group == "admin" or (user.mail == post.user_mail):
			return True
	except Exception:
		pass
	return False


def owning_required(f):
	"""
	Decorator, which use 'is_owning' function, and
	@return: follow passed function if True or return 'Access denied!' otherwise.
	"""
	@wraps(f)
	def decorated_function(*args, **kwargs):
		post = Post.query.get(kwargs["id"])
		if is_owning(user(), post):
			return f(*args, **kwargs)
		return "Access denied!"
	return decorated_function


def admin_required(f):
	"""
	Like previous, but now more strong - user must be admin
	"""
	@wraps(f)
	def decorated_function(*args, **kwargs):
		if user().grup == "admin":
			return f(*args, **kwargs)
		return "Access denied!"
	return decorated_function
