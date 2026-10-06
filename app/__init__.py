from flask import Flask, redirect, url_for, request, jsonify
from .extensions import db, migrate, login_manager, csrf
from . import models
from flask_login import current_user
import click

def register_cli(app: Flask):
    @app.cli.command("create-admin")
    @click.option("--username", prompt=True)
    @click.option("--password", prompt=True, hide_input=True, confirmation_prompt=True)
    def create_admin(username, password):
        # 创建管理员账号
        from .models import Admin
        if Admin.query.filter_by(username=username).first():
            click.echo("该账号已存在")
            return
        a = Admin(username=username)
        a.set_password(password)
        db.session.add(a)
        db.session.commit()
        click.echo(f"管理员 {username} 已创建")

def register_extensions(app: Flask):
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)
    
    from .models import User, Admin
    
    @login_manager.user_loader
    def load_user(user_id: str):
        return db.session.get(Admin, int(user_id))

def create_app(config_object='config.Config'):
    app = Flask(__name__)
    app.config.from_object(config_object)

    register_extensions(app)
    
    from .auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix="/auth")
    
    from .routes import main_bp
    app.register_blueprint(main_bp)
    csrf.exempt(main_bp)
    
    register_cli(app)
    
    # 全局登录闸门
    @app.before_request
    def require_login_for_writes():
        if request.method not in ("POST", "PUT", "DELETE", "PATCH"):
            return
        allow = {"auth.login", "static"}
        if request.endpoint in allow or request.endpoint is None:
            return
        if not current_user.is_authenticated:
            # 判断是不是 AJAX/JSON 请求
            wants_json = (
                request.is_json
                or request.path.startswith("/api/")
                or request.accept_mimetypes.best == "application/json"
                or request.headers.get("X-Requested-With") == "XMLHttpRequest"
            )
            if wants_json:
                return jsonify({
                    "error": "请先登录",
                    "login_url": url_for("auth.login", next=request.path),
                }), 401
            # 普通浏览器导航请求（比如提交表单）才重定向
            return redirect(url_for("auth.login", next=request.path))

    return app