from .extensions import db
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# 管理员账户
class Admin(db.Model, UserMixin):
    __tablename__ = "admin"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    display_name = db.Column(db.String(64), default="")
    is_active_flag = db.Column(db.Boolean, default=True, nullable=False)
    
    def set_password(self, raw: str):
        self.password_hash = generate_password_hash(raw)
        
    def check_password(self, raw: str):
        return check_password_hash(self.password_hash, raw)
    
    @property
    def is_active(self):
        return self.is_active_flag
    
    def __repr__(self):
        return f"<Admin {self.username}>"



# 关联表：User和Task之间的多对多关系
task_users = db.Table(
    'task_users',
    db.Column('task_id', db.Integer, db.ForeignKey('task.id'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True)
)

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    # 反向引用：通过User访问Task
    tasks = db.relationship('Task', secondary=task_users, back_populates='users', lazy='dynamic')

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'tasks': [task.to_dict() for task in self.tasks]
        }

class Task(db.Model):
    __tablename__ = 'task'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    hours = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=True)
    # 反向引用：通过Task访问User
    users = db.relationship('User', secondary=task_users, back_populates='tasks')

    def to_dict(self):
        users = [p.username for p in self.users if p.username]
        return {
            'id': self.id,
            'name': self.name,
            'start_time': self.start_time.isoformat(),
            'end_time': self.end_time.isoformat(),
            'hours': self.hours,
            'users': users,
            'description': self.description
        }