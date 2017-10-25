from . import db, login_manager
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, LoginManager, current_user, AnonymousUserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from markdown import markdown
import bleach

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index = True)
    username = db.Column(db.String(64), unique=True, index = True)
    password_hash = db.Column(db.String(128))
    admin = db.Column(db.Boolean, default=False)
    image = db.Column(db.String(64))
    create_at = db.Column(db.DateTime, default=datetime.utcnow)
    blogs = db.relationship('Blog', backref='author', lazy= 'dynamic')
    comments = db.relationship('Comment', backref='author', lazy= 'dynamic')

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_administrator(self):
        return self.admin

class AnonymousUser(AnonymousUserMixin):
    def is_administrator(self):
        return False

login_manager.anonymous_user = AnonymousUser

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Blog(db.Model):
    __tablename__ = 'blogs'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    summary = db.Column(db.Text)
    summary_html = db.Column(db.Text)
    content = db.Column(db.Text)
    content_html = db.Column(db.Text)
    create_at = db.Column(db.DateTime, default=datetime.utcnow, index = True)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    comments = db.relationship('Comment', backref='blog', lazy= 'dynamic')

    @staticmethod
    def on_changed_summary(target, value, oldvalue, initiator):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
                        'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
                        'h1', 'h2', 'h3', 'p']
        target.summary_html = bleach.linkify(bleach.clean(
            markdown(value, output_format = 'html'), 
            tags = allowed_tags, strip = True))

    @staticmethod
    def on_changed_content(target, value, oldvalue, initiator):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
                        'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
                        'h1', 'h2', 'h3', 'p']
        target.content_html = bleach.linkify(bleach.clean(
            markdown(value, output_format = 'html'), 
            tags = allowed_tags, strip = True))


db.event.listen(Blog.summary, 'set', Blog.on_changed_summary)
db.event.listen(Blog.content, 'set', Blog.on_changed_content)

class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    diabled = db.Column(db.Boolean)
    content = db.Column(db.Text)
    create_at = db.Column(db.DateTime, default=datetime.utcnow, index = True)
    blog_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    author_id = db.Column(db.Integer, db.ForeignKey('blogs.id'))


