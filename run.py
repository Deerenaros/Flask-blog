# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from app import app
from sys import argv

"""
Rly, just start a server!
"""

app.run("0.0.0.0", 80, debug="--debug" in argv)