from flask import render_template, url_for, redirect, request, flash
from flask_login import login_required, current_user
from . import manage
from .. import db
from ..models import User, Blog
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

# 创建博客
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
    return render_template('manage/create_blog.html', form=form)