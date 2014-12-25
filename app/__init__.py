from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.assets import Environment, Bundle
from flask.ext.login import LoginManager

"""
second lab:
rights with access roles
better authorization (https + serts) or VK.auth
"""

app = Flask(__name__)
app.config.from_object('config')

login_manager = LoginManager()
login_manager.init_app(app)
db = SQLAlchemy(app)
assets = Environment(app)

js = Bundle('js/jquery.min.js', 'js/jquery.restfulizer.js', 'js/moment.min.js', 'kalendae.js',
			filters='jsmin', output='get/packed.js')
css = Bundle('kalendae.css', 'css/faw.css', 'css/main.css', 'css/pure-min.css',
			 filters='cssmin', output='get/packed.css')

assets.register('js', js)
assets.register('css', css)

from app import views, models