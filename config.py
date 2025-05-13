import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'key-so-secret-you-will-never-get-it'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABSE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    POSTS_PER_PAGE = 25
    MAIL_SERVER = 'localhost'
    MAIL_PORT = 8025