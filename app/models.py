from app import app, db
from datetime import datetime
from flask.ext.social import Social
from flask.ext.social.datastore import SQLAlchemyConnectionDatastore

class Post(db.Model):
	"""
	This is a class represents a model-object for a post entity.
		- id (integer): This is a primary key, self creating index by simply counter.
		- title (string): title
		- html (string): content
		- time (datetime): timestamp at creating
		- user_mail (string): this is foreign key that connects with user entity, ondelete param set as RESTRICT for
			restrict deleting, which mean while trying delete a user object, sqlalchemy do not try to delete all
			connected posts with one
	"""
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(120))
	html = db.Column(db.String(10**6))
	time = db.Column(db.DateTime, default=datetime.now)
	user_mail = db.Column(db.String(36), db.ForeignKey("user.mail", ondelete="RESTRICT"))
	is_authenticated = True

	@property
	def cut(self):
		return self.html[0:min(400, len(self.html))]

	@staticmethod
	def add(**kwargs):
		db.session.add(Post(**kwargs))


# take a quest about sqlite politics (restrict, cascade)
class User(db.Model):
	id = db.Column(db.String(36), primary_key=True)
	token = db.Column(db.String(36))
	mail = db.Column(db.String(36))
	group = db.Column(db.String(16))
	posts = db.relationship("Post", backref="user", lazy="dynamic")


	def get_id(self):
		return unicode(self.mail)

	def is_authenticated(self):
		return bool(self.auth)

	def is_anonymous(self):
		return False

	def is_active(self):
		return True


def prepare_models():
	pass
"""	""
	Simply function what had to call at running in order to create admin. If one do no exists.
	""
	User.admin = filter(lambda u: u.grup == "admin", User.query.all())

	if len(User.admin) == 0:
		mail = raw_input("Type admin's e-mail: ")
		pswd = raw_input("Type admin's password: ")
		db.session.add(User(mail=mail, pswd=pswd, grup="admin"))
		db.session.commit()
	else:
		User.admin = admin[0]
"""