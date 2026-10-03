from datetime import datetime
from .models import Task, User, task_users
from flask import Blueprint, render_template, jsonify, request, current_app
from .extentions import db

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    current_app.logger.debug("Fetching all tasks from the database.")
    tasks = db.session.query(Task).all()
    tasks = [task.to_dict() for task in tasks]
    status = {}
    for task in tasks:
        for user in task['users']:
            status[user] = status.get(user, 0) + task['hours']
    return render_template('index.html', tasks=tasks, status=status)

@main_bp.route('/tasks/list', methods=['GET'])
def list_tasks():
    tasks = Task.query.order_by(Task.start_time.desc()).all()
    return jsonify([task.to_dict() for task in tasks])

@main_bp.route('/users/list', methods=['GET'])
def list_users():
    users = User.query.order_by(User.username).all()
    return jsonify([user.to_dict() for user in users])