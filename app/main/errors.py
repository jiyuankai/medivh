from flask import render_template
from . import main

# errorhandler错误处理修饰器，只能作用在当前蓝本中的视图函数
# 故要其全局响应，要在blueprint中使用app_errorhandler注册全局作用域
@main.app_errorhandler(404)
def page_not_found(e):
	return render_template('404.html'), 404

@main.app_errorhandler(500)
def internal_server_error(e):
	return render_template('500.html'), 500

@main.app_errorhandler(403)
def forbidden(e):
	return render_template('403.html'), 403