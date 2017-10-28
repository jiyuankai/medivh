from flask import render_template, url_for, redirect, request, flash
from flask_login import login_required, current_user
from . import manage
from .. import db
from ..models import User, Blog, Comment
from ..decorators import admin_required
from .forms import ChangePasswordForm, BlogForm

# 修改密码
@manage.route('/change-password', methods = ['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.password = form.password.data
            db.session.add(current_user)
            db.session.commit()
            flash('密码修改成功')
            return redirect(url_for('main.index'))
        else:
            flash('密码错误')
    return render_template('manage/change_password.html', form=form)

# 文章管理
@manage.route('/blogs')
@admin_required
@login_required
def manage_blogs():
    page = request.args.get('page', 1, type=int)
    pagination = Blog.query.order_by(Blog.create_at.desc()).paginate(
        page, per_page=10, error_out=False)
    blogs = pagination.items
    return render_template('manage/manage_blogs.html', blogs=blogs, 
                            pagination=pagination)

# 写文章
@manage.route('/create-blog', methods = ['GET', 'POST'])
@admin_required
@login_required
def create_blog():
    form = BlogForm()
    if form.validate_on_submit():
        blog = Blog(name=form.name.data, summary=form.summary.data, 
                    content=form.content.data, 
                    author=current_user._get_current_object())
        db.session.add(blog)
        db.session.commit()
        return redirect(url_for('main.blog', id=blog.id))
    return render_template('manage/create_blog.html', form=form)

# 编辑文章
@manage.route('/edit-blog/<int:id>', methods = ['GET', 'POST'])
@admin_required
@login_required
def edit_blog(id):
    blog = Blog.query.get_or_404(id)
    form = BlogForm()
    if form.validate_on_submit():
        blog.name = form.name.data
        blog.summary = form.summary.data
        blog.content = form.content.data
        db.session.add(blog)
        db.session.commit()
        return redirect(url_for('main.blog', id=blog.id))
    form.name.data = blog.name
    form.summary.data = blog.summary
    form.content.data = blog.content
    return render_template('manage/edit_blog.html', form=form)

# 删除文章
@manage.route('/delete-blog/<int:id>')
@admin_required
@login_required
def delete_blog(id):
    blog = Blog.query.get_or_404(id)
    db.session.delete(blog)
    db.session.commit()
    flash('文章已删除')
    return redirect(url_for('manage.manage_blogs'))

# 评论管理
@manage.route('/comments')
@admin_required
@login_required
def manage_comments():
    page = request.args.get('page', 1, type=int)
    pagination = Comment.query.order_by(Comment.create_at.desc()).paginate(
        page, per_page=10, error_out=False)
    comments = pagination.items
    return render_template('manage/manage_comments.html', comments=comments, 
                            pagination=pagination)

# 屏蔽评论



# 用户管理
@manage.route('/users')
@admin_required
@login_required
def manage_users():
    page = request.args.get('page', 1, type=int)
    pagination = User.query.order_by(User.create_at.desc()).paginate(
        page, per_page=10, error_out=False)
    users = pagination.items
    return render_template('manage/manage_users.html', users=users, 
                            pagination=pagination)
