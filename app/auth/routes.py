from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from urllib.parse import urlsplit
from . import auth_bp
from .forms import LoginForm
from ..models import Admin

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    
    form = LoginForm()
    if form.validate_on_submit():
        admin = Admin.query.filter_by(username=form.username.data).first()
        if admin is None or not admin.check_password(form.password.data):
            flash("账号密码错误", "danger")
            return redirect(url_for("auth.login"))
        if not admin.is_active:
            flash("该账号已禁用", "warning")
            return redirect(url_for("auth.login"))
        
        login_user(admin, remember=form.remember.data)
        next_page = request.args.get("next")
        
        if next_page:
            parts = urlsplit(next_page)
            if (parts.scheme or parts.netloc
                    or not parts.path.startswith("/")
                    or parts.path.startswith("//")):
                next_page = None
            else:
                next_page = parts.path or None
        return redirect(next_page or url_for("main.home"))
    
    return render_template("auth/login.html", form=form)

@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("已退出登录", "info")
    return redirect(url_for("auth.login"))