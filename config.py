import os
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Connect to the database


# TODO IMPLEMENT DATABASE URL
SQLALCHEMY_DATABASE_URI = 'postgres://kglxeccpqyvjym:db4c80e5f915ef03dfc6a09e96fb1ce8b790d0d714c6ff69aedccf95cb723171@ec2-3-228-235-79.compute-1.amazonaws.com:5432/df9k8ltv4qqp4l'

# Alter Postgresql dialect name in heroku
if SQLALCHEMY_DATABASE_URI.startswith("postgres://"):
    SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace("postgres://", "postgresql://", 1)

SQLALCHEMY_TRACK_MODIFICATIONS = False