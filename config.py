####################
# Dev Configuration
####################
import os

DEBUG = True
SECRET_KEY = '1234' # make sure to change this

SQLALCHEMY_DATABASE_URI = 'mysql+mysqldb://localhost:''@localhost/test'
# SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
