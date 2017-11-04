from flask_login import login_required, current_user
from flask import url_for, render_template, current_app, redirect, request, flash
from . import main
from .. import db
from ..models import Blog, Comment, Label
from .forms import CreateCommentForm

@main.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    label = Label.query.filter_by(name=request.args.get('label', '')).first()
    if label is not None:
        pagination = label.blogs.order_by(Blog.create_at.desc()).paginate(
            page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'], error_out=False)
        blogs = pagination.items
        labels = Label.query.all()
        return render_template('index.html', blogs=blogs, labels=labels, pagination=pagination)
    pagination = Blog.query.order_by(Blog.create_at.desc()).paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'], 
        error_out=False)
    blogs = pagination.items
    labels = Label.query.all()
    return render_template('index.html', blogs=blogs, labels=labels, pagination=pagination)

@main.route('/blog/<int:id>', methods=['GET', 'POST'])
def blog(id):
    blog = Blog.query.get_or_404(id)
    form = CreateCommentForm()
    if form.validate_on_submit():
        comment = Comment(
            content = form.content.data,
            blog = blog,
            author = current_user._get_current_object())
        db.session.add(comment)
        db.session.commit()
        flash('评论已提交')
        return redirect(url_for('main.blog', id=blog.id))
    page = request.args.get('page', 1, type=int)
    pagination = blog.comments.order_by(Comment.create_at.desc()).paginate(
        page, per_page=6, error_out=False)
    comments = pagination.items
    return render_template('blog.html', blog=blog, comments=comments, 
                            pagination=pagination, form=form, page=page)
