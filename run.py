from app import app
from sys import argv

"""
Rly, just start a server!
"""

app.run(debug="--debug" in argv)