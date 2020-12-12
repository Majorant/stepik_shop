import os


class Config:
    DEBUG = False
    SECRET_KEY= os.environ.get("CSRF_KEY")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
