from . import db, login_manager
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, LoginManager, current_user, AnonymousUserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app, request
from markdown import markdown
import bleach, hashlib


# 收藏功能：Blog和User多对多关系的中间表
collections = db.Table('collections',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('blog_id', db.Integer, db.ForeignKey('blogs.id'))
)

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index = True)
    username = db.Column(db.String(64), unique=True, index = True)
    password_hash = db.Column(db.String(128))
    admin = db.Column(db.Boolean, default=False)
    avatar_hash = db.Column(db.String(64))
    disabled = db.Column(db.Boolean, default=False)
    create_at = db.Column(db.DateTime, default=datetime.utcnow)
    blogs = db.relationship('Blog', backref='author', lazy= 'dynamic')
    comments = db.relationship('Comment', backref='author', lazy= 'dynamic')
    collections = db.relationship('Blog', secondary=collections, 
                                   backref=db.backref('users', lazy='dynamic'),
                                   lazy='dynamic')

    def __init__(self, **kw):
        super(User, self).__init__(**kw)
        if self.email is not None and self.avatar_hash is None:
            self.avatar_hash = hashlib.md5(self.email.encode('utf-8')).hexdigest()
        if self.email == 'admin@admin.com':
        	self.admin = True
        	db.session.add(self)
        	db.session.commit()

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

    # 生成Gravatar头像
    def gravatar(self, size=100, default='identicon', rating='g'):
        if request.is_secure:
            url = 'https://secure.gravatar.com/avatar'
        else:
            url = 'http://www.gravatar.com/avatar'
        hash = self.avatar_hash or hashlib.mp5(self.email.encode('utf-8')).hexdigest()
        return '{url}/{hash}?s={size}&d={default}&r={rating}'.format(
            url=url, hash=hash, size=size, default=default, rating=rating)

    @staticmethod
    def generate_fake(count=100):
        from sqlalchemy.exc import IntegrityError
        from random import seed
        import forgery_py

        seed()
        for i in range(count):
            u = User(email = forgery_py.internet.email_address(),
                     username = forgery_py.internet.user_name(True),
                     password = forgery_py.lorem_ipsum.word(),
                     admin = False)
            db.session.add(u)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()

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

    def is_collected(self, user):
        return self.users.filter_by(id=user.id).first() is not None


    @staticmethod
    def create_about_blog():
        if Blog.query.filter_by(id=998).first() is None:
            u = User.query.filter_by(id=1).first()
            b = Blog(id=998, name='关于本站', summary='', content='', author=u)
            db.session.add(b)
            db.session.commit()

    @staticmethod
    def on_changed_summary(target, value, oldvalue, initiator):
        target.summary_html = bleach.linkify(markdown(value, output_format = 'html'))

    @staticmethod
    def on_changed_content(target, value, oldvalue, initiator):
        target.content_html = bleach.linkify(markdown(value, output_format = 'html'))

    @staticmethod
    def generate_fake(count=100):
        from random import seed, randint
        import forgery_py
        u = User.query.filter_by(id=1).first()

        seed()
        for i in range(count):
            try:
                b = Blog(name = forgery_py.lorem_ipsum.title(1),
                         summary = forgery_py.lorem_ipsum.sentences(randint(3,5)),
                         content = forgery_py.lorem_ipsum.sentences(randint(8,10)),
                         create_at = forgery_py.date.date(True),
                         author = u)
                db.session.add(b)
                db.session.commit()
            except AttributeError:
                pass    

db.event.listen(Blog.summary, 'set', Blog.on_changed_summary)
db.event.listen(Blog.content, 'set', Blog.on_changed_content)

# 分类功能：Blog和Label多对多关系的中间表
classifications = db.Table('classifications', 
    db.Column('blog_id', db.Integer, db.ForeignKey('blogs.id')),
    db.Column('label_id', db.Integer, db.ForeignKey('labels.id'))
)

class Label(db.Model):
    __tablename__= 'labels'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    type = db.Column(db.String(64))
    # 多对多关系模型
    blogs = db.relationship('Blog',
                          secondary=classifications,
                          backref=db.backref('labels', lazy='dynamic'),
                          lazy='dynamic')

    def __init__(self, **kw):
        super(Label, self).__init__(**kw)
        db.session.add(self)
        db.session.commit()
        L = ['danger', 'warning', 'info', 'success', 'primary', 'default']
        if self.type == None:
            index = (self.id + 6) % 6
            self.type = L[index]
            db.session.add(self)
            db.session.commit()

    @staticmethod
    def generate_fake(count=3):
        from random import randint 

        if not Label.query.count():
            L = ['Java', 'Basic', 'Python', 'HTML','Javascript', 'C++', 'PHP', 'SQL',
                 'Flask', 'Django', 'jQuery', 'Ajax']
            for labname in L:
                l = Label(name=labname)
                db.session.add(l)
                db.session.commit()            

        label_count = Label.query.count()
        blogs = Blog.query.all()       
        for b in blogs: 
            for i in range(randint(1,count)):
                l = Label.query.offset(randint(0, label_count - 1)).first()
                l.blogs.append(b)
                db.session.add(l)
                db.session.commit()


class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    create_at = db.Column(db.DateTime, default=datetime.utcnow, index = True)
    disabled = db.Column(db.Boolean, default=False)
    blog_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    author_id = db.Column(db.Integer, db.ForeignKey('blogs.id'))

    @staticmethod
    def generate_fake(count=100):
        from random import seed, randint
        import forgery_py

        seed()
        user_count = User.query.count()
        blog_count = Blog.query.count()
        for i in range(count):
            u = User.query.offset(randint(0, user_count - 1)).first()
            b = Blog.query.offset(randint(0, blog_count - 1)).first()
            c = Comment(content = forgery_py.lorem_ipsum.sentences(randint(1, 2)),
                        create_at = forgery_py.date.date(True),
                        disabled = False,
                        author = u,
                        blog = b)
            db.session.add(c)
            db.session.commit()



