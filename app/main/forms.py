from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField
from wtforms.validators import Required

# 创建评论
class CreateCommentForm(FlaskForm):
	content = TextAreaField('说点什么？', validators=[Required()])
	submit = SubmitField('提交评论')
