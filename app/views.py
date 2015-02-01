# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from flask import redirect, abort, request, session
from flask.ext.login import current_user, login_required, login_user, logout_user
from datetime import datetime
import json
import requests
import sqlalchemy

from app import *
from models import *
from forms import *
from usefull import *

from sqlalchemy.exc import IntegrityError


def dd(**kwargs):
    kwargs.update(user=user, is_owning=is_owning)
    return kwargs


@app.route("/")
@app.route("/index")
@app.route("/posts")
@templated("index.html")
def index():
    return dd(title="Home", posts=reversed(Post.query.all()))


@app.route("/tag/<name>")
@templated("index.html")
def selected(select):
    return dd(title=select, posts=reversed(filter(lambda p: p.tag == select, Post.query.all())))


@app.route("/posts/<id>")
@templated("view.html")
def view_post(id):
    viewing = Post.query.get(id)
    if viewing is None:
        abort(404)
    return dd(post=viewing)


@app.route("/manage/<id>", methods=["GET", "POST"])
@templated("manage.html")
@owning_required
def edit_post(id):
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
def create_post():
    form = PostForm()
    if form.validate_on_submit():
        creating = Post(time=datetime.now())
        form.populate_obj(creating)
        db.session.add(creating)
        db.session.commit()
        return redirect("/index")
    return dd(title="Create new post", btn="Post", form=form)