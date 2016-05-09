#!/usr/bin/env python

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config.from_envvar('CIVIS_CONFIG')

db = SQLAlchemy(app)

from app import models,views
