from app import db
from datetime import datetime


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

	@property
	def cut(self):
		return self.html[0:min(400, len(self.html))]

	@staticmethod
	def add(**kwargs):
		db.session.add(Post(**kwargs))


# take a quest about sqlite politics (restrict, cascade)
class User(db.Model):
	"""
	This is a class represents a model-object for user entity.
	@type mail: string
	@param mail: This is a primary key, that mean registred user's e-mail.
	@type abut: string
	@param abut: Something about user, that he had wrote at registration.
	@type regd: datetime
	@param regd: Date & time of registration.
	@type brth: datetime
	@param brth: Birthsday.
	@type auth: bool
	@param auth: Is user authenticated.
	@type grup: string
	@param grup: Just a string for group classification. Simply. Hard. Works.
	@type posts: relationship
	@param posts: backref for connecting users with posts.
	"""

	admin = None

	mail = db.Column(db.String(36), primary_key=True)
	abut = db.Column(db.String(10**6))
	regd = db.Column(db.DateTime, default=datetime.now)
	brth = db.Column(db.DateTime)
	pswd = db.Column(db.String(36))
	auth = db.Column(db.Boolean)
	grup = db.Column(db.String(16))
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
	"""
	Simply function what had to call at running in order to create admin. If one do no exists.
	"""
	User.admin = filter(lambda u: u.grup == "admin", User.query.all())

	if len(User.admin) == 0:
		mail = raw_input("Type admin's e-mail: ")
		pswd = raw_input("Type admin's password: ")
		db.session.add(User(mail=mail, pswd=pswd, grup="admin"))
		db.session.commit()
	else:
		User.admin = admin[0]
