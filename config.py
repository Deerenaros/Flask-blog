# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os

basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "app.db")
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, "db_repository")

CSRF_ENABLED = True
SECRET_KEY = "13b0f162ecdd77aa"
SECURITY_POST_LOGIN = "/profile"