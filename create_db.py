#! /usr/bin/env python
from app import app,db
import os.path

SQLALCHEMY_DATABASE_URI = app.config['SQLALCHEMY_DATABASE_URI']

db.create_all()
