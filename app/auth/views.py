from flask import render_template, url_for, redirect, request, flash
from flask_login import login_user, login_required, logout_user, current_user
from . import auth
from .. import db
from ..models import User
# from ..email import send_email
from .forms import LoginForm, RegistrationForm

# 登录
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash('您已经登录')
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('用户名或密码有误')
    return render_template('auth/login.html', form=form)

# 注销
@login_required
@auth.route('/logout')
def logout():
    logout_user()
    flash('注销用户已注销')
    return redirect(url_for('main.index'))

# 注册
@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data, 
                    username=form.username.data, 
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('您已成功注册，请登录')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)







