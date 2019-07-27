import os

dbdir = "sqlite:///" + os.path.abspath(os.getcwd()) + "/flask.db"

class Config(object):
    SECRET_KEY = 'my_secret_key'


class DevelopmentConfig(Config):
    DEBUG ='False'
    SQLALCHEMY_DATABASE_URI = dbdir
    SQLALCHEMY_TRACK_MODIFICATIONS = False #se coloca en modo false ya que de lo contrario apareceria un Warning
