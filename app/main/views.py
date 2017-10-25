from flask_login import login_required
from flask import url_for, render_template, current_app, redirect, request
from . import main
from ..models import Blog

@main.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    pagination = Blog.query.order_by(Blog.create_at.desc()).paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'], 
        error_out=False)
    blogs = pagination.items
    return render_template('index.html', blogs=blogs, pagination=pagination)

@main.route('/blog/<int:id>')
def blog(id):
	blog = Blog.query.get_or_404(id)
	return render_template('blog.html', blog=blog)