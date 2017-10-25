from functools import wraps
from flask import abort
from flask_login import current_user

def admin_required(func):
	@wraps(func)
	def wrapper(*args, **kw):
		if not current_user.is_administrator():
			abort(403)
		return func(*args, **kw)
	return wrapper
