import os

BASEDIR = '.'

DB_DIR = os.path.join(BASEDIR,'db')

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(DB_DIR, 'transportation.db')
