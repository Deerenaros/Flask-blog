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
    tag = db.Column(db.String(10))

    @property
    def cut(self):
        return self.html[0:min(400, len(self.html))]

    @staticmethod
    def add(**kwargs):
        db.session.add(Post(**kwargs))