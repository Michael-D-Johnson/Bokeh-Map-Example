import os

BASEDIR = '/Users/mjohns44/Code/Civis/Civis'

DB_DIR = os.path.join(BASEDIR,'db')

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(DB_DIR, 'transportation.db')
