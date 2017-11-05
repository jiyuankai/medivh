from flask import render_template, url_for, redirect, request, flash
from flask_login import login_required, current_user
from . import manage
from .. import db
from ..models import User, Blog, Comment, Label
from ..decorators import admin_required
from .forms import ChangePasswordForm, BlogForm
import logging
logging.basicConfig(level=logging.INFO)

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
                            pagination=pagination, page=page)

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
        labels = form.label.data.split(';')
        for label in labels:
            if label:
                # 找标签是否存在
                lab = Label.query.filter_by(name=label).first()
                # 若不存在，则新建标签
                if lab is None:
                    newlab = Label(name=label)
                    newlab.blogs.append(blog)
                    db.session.add(newlab)
                else:
                    lab.blogs.append(blog)
                    db.session.add(lab)
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
        # 暴力修改，先删掉所有标签，再把标签栏里全部新增
        for l in blog.labels.all():
            l.blogs.remove(blog)
            db.session.add(l)
            # 清理无内容标签
            if l.blogs.count() == 0:
                db.session.delete(l)
        db.session.commit()
        # 加标签
        labels = form.label.data.split(';')
        for label in labels:
            # 判断标签名存在
            if label:
                # 标签在数据库是否存在
                lab = Label.query.filter_by(name=label).first()
                # 创建新的分类标签
                if lab is None:
                    newlab = Label(name=label)
                    newlab.blogs.append(blog)
                    db.session.add(newlab)
                else:
                    lab.blogs.append(blog)
                    db.session.add(lab)         
        db.session.commit()
        return redirect(url_for('main.blog', id=blog.id))
    form.name.data = blog.name
    # blog.labels.all() 返回多个labels，获取他们的name，并转换成以;链接的str
    form.label.data = ';'.join([lab.name for lab in blog.labels.all()])
    form.summary.data = blog.summary
    form.content.data = blog.content
    return render_template('manage/edit_blog.html', form=form)

# 删除文章
@manage.route('/delete-blog/<int:id>')
@admin_required
@login_required
def delete_blog(id):
    blog = Blog.query.get_or_404(id)
    if blog.comments.all():
        for c in blog.comments.all():
            db.session.delete(c)
    # 将标签中的此文章删除
    if blog.labels.all():
        for lab in blog.labels.all():
            lab.blogs.remove(blog)
            db.session.add(lab)
            # 清理无内容标签
            if lab.blogs.count() == 0:
                db.session.delete(lab)
    db.session.delete(blog)
    db.session.commit()
    flash('文章已删除')
    return redirect(url_for('manage.manage_blogs',
                            page=request.args.get('page', 1, type=int)))

# 我的收藏
@manage.route('/collections')
@login_required
def manage_collections():
    page = request.args.get('page', 1, type=int)
    pagination = current_user.collections.paginate(
        page, per_page=10, error_out=False)
    blogs = pagination.items
    return render_template('manage/manage_collections.html', blogs=blogs, 
                    pagination=pagination, page=page)

# 收藏
@manage.route('/collections/enable/<int:id>')
@login_required
def enable_collect(id):
    blog = Blog.query.get_or_404(id)
    user = current_user._get_current_object()
    if not blog.is_collected(user):
        user.collections.append(blog)
        db.session.add(user)
        db.session.commit()
        flash('收藏成功')
    else:
        flash('请勿重复收藏')
    # 在文章详情页操作   
    if request.args.get('info', None) == 'blog':
        return redirect(url_for('main.blog', id=id))
    if request.args.get('info', None) == 'manage':
        return redirect(url_for('manage.manage_collections', 
                                page=request.args.get('page', 1, type=int)))    
    
# 取消收藏
@manage.route('/collections/disable/<int:id>')
@login_required
def disable_collect(id):
    blog = Blog.query.get_or_404(id)
    user = current_user._get_current_object()
    if blog.is_collected(user):
        user.collections.remove(blog)
        db.session.add(user)
        db.session.commit()
        flash('取消收藏')
    else:
        flash('并未收藏该文章')
    # 在文章详情页操作
    if request.args.get('info', None) == 'blog':
        return redirect(url_for('main.blog', id=id))
    if request.args.get('info', None) == 'manage':
        return redirect(url_for('manage.manage_collections', 
                                page=request.args.get('page', 1, type=int)))  

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
                            pagination=pagination, page=page)

# 恢复评论
@manage.route('/comment/enable/<int:id>')
@admin_required
@login_required
def enable_comment(id):
    comment = Comment.query.get_or_404(id)
    comment.disabled = False
    db.session.add(comment)
    db.session.commit()
    flash('已恢复该评论')
    if request.args.get('info', '') == 'blog':
        return redirect(url_for('main.blog', id=comment.blog.id, 
                                page=request.args.get('page', 1, type=int)))
    return redirect(url_for('manage.manage_comments', 
                            page=request.args.get('page', 1, type=int)))
# 屏蔽评论
@manage.route('/comment/disable/<int:id>')
@admin_required
@login_required
def disable_comment(id):
    comment = Comment.query.get_or_404(id)
    comment.disabled = True
    db.session.add(comment)
    db.session.commit()
    flash('已屏蔽该评论')
    if request.args.get('info', '') == 'blog':
        return redirect(url_for('main.blog', id=comment.blog.id, 
                                page=request.args.get('page', 1, type=int)))
    return redirect(url_for('manage.manage_comments', 
                            page=request.args.get('page', 1, type=int)))

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
                            pagination=pagination, page=page)


# 封禁用户
@manage.route('/user/disable/<int:id>')
@admin_required
@login_required
def disable_user(id):
    user = User.query.get_or_404(id)
    user.disabled = True
    db.session.add(user)
    db.session.commit()
    flash('用户已封禁')
    return redirect(url_for('manage.manage_users',
                            page=request.args.get('page', 1, type=int)))

# 解禁用户
@manage.route('/user/enable/<int:id>')
@admin_required
@login_required
def enable_user(id):
    user = User.query.get_or_404(id)
    user.disabled = False
    db.session.add(user)
    db.session.commit()
    flash('用户已解禁')
    return redirect(url_for('manage.manage_users',
                            page=request.args.get('page', 1, type=int)))

