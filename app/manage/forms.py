from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, PasswordField
from wtforms.validators import Required, EqualTo
from flask_pagedown.fields import PageDownField

# 修改密码
class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('旧密码', validators=[Required()])
    password = PasswordField('新密码', validators=[
        Required(), EqualTo('password2', message='两次输入密码不一致')])
    password2 = PasswordField('确认密码', validators=[Required()])
    submit = SubmitField('确认修改')

# 创建/编辑博客
class BlogForm(FlaskForm):
	name = StringField('标题', validators=[Required()])
	label = StringField("分类", validators=[Required()])
	summary = TextAreaField('摘要', validators=[Required()])
	content = PageDownField('内容', validators=[Required()])
	submit = SubmitField('发表文章')