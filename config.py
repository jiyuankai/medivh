import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN') or 'jiyuankai920902@126.com'
    FLASKY_MAIL_SENDER = 'Myblog Admin <422925090@qq.com>'
    FLASKY_MAIL_SUBJECT_PREFIX = '[MyBlog]'
    FLASKY_POSTS_PER_PAGE = 6

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:password@localhost:3306/myblog_dev'

class TestingCofig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
    'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:Jyk92292@localhost:3306/myblog'

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)

    
config = {
    'development': DevelopmentConfig,
    'testing': TestingCofig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}        