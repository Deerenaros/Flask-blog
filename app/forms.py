from flask.ext.wtf import Form
from wtforms import StringField, TextAreaField, PasswordField, DateField, SelectField
from wtforms.validators import InputRequired, Length, Email, Regexp


# add checkboxes, dates, admins

class PostForm(Form):
	"""
	Object, that could be rendered into html with hidden tag placed in order to CLRF protection.
	Contents post:
		- title (string): post's title, represented by <input type=text />
		- html (string): post's entry, represented by <textarea></textarea>
	"""
	title = StringField("title", validators=[InputRequired()])
	html = TextAreaField("html", validators=[InputRequired()])
#	tags = StringField("tags", validators=[Regexp("[\w\s]*", message="Occasion arises while tried parse tag-list...")])


class RegForm(Form):
	"""
	Object, that could be rendered into html with hidden tag placed in order to CLRF protection.
	Contents user reg. info:
		- mail (string): user's e-mail, represented by <input type=text />
		- pswd (string): user's password, represented by <input type=password />
		- brth (string): user's birthsday, represented by <input type=text />
		- about (string): user's additional info, represented by <textarea></textarea>
	"""
	mail = StringField("mail", validators=[Email(), InputRequired()])
	pswd = PasswordField("pswd", validators=[InputRequired()])
	brth = DateField("brth", validators=[InputRequired()], format='%d/%m/%Y')
	about = TextAreaField("about")


class LoginForm(Form):
	"""
	Object, that could be rendered into html with hidden tag placed in order to CLRF protection.
	Sign in form:
		- mail (string): user's e-mail, represented by <input type=text />
		- pswd (string): user's pswd, represented by <input type=password />
	"""
	mail = StringField("mail", validators=[InputRequired()])
	pswd = StringField("pswd", validators=[InputRequired()])