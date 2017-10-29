from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Length, Email, EqualTo
from wtforms import ValidationError
from ..models import User


# 登录表单
class LoginForm(FlaskForm):
    email = StringField('电子邮箱', validators=[Required(), Length(1, 64), 
                                                Email()])
    password = PasswordField('密码', validators=[Required()])
    remember_me = BooleanField('记住我')
    submit = SubmitField('确认登录')

    def validate_email(SELF, field):
        user = User.query.filter_by(email=field.data).first()
        if user is not None:
            if user.disabled:
                raise ValidationError('该用户已被封禁，请联系管理员')


# 注册表单
class RegistrationForm(FlaskForm):
    email = StringField('电子邮箱', validators=[Required(), Length(1, 64), 
                                                Email()])
    username = StringField('昵称', validators=[Required(), Length(1, 64)])
    password = PasswordField('输入密码', validators=[
        Required(), EqualTo('password2', message='两次输入密码不一致')])
    password2 = PasswordField('确认密码', validators=[Required()])
    submit = SubmitField('注册')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('该邮箱已被注册')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('该名称已被使用')





    