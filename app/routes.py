from datetime import datetime
from .models import Task, User, event_participants
from flask import Blueprint, render_template, jsonify, request

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    tasks = [
        {
            'id': 1,
            'name': '示例任务 1',
            'start_time': datetime(2026, 10, 1, 8, 0),
            'end_time': datetime(2026, 10, 1, 10, 0),
            'description': '这是一个示例任务',
            'hours': 2,
            'participants': ['张三', '李四'],
        },
        {
            'id': 2,
            'name': '示例任务 2',
            'start_time': datetime(2026, 10, 2, 9, 0),
            'end_time': datetime(2026, 10, 2, 12, 0),
            'description': '这是另一个示例任务',
            'hours': 3,
            'participants': ['王五', '赵六'],
        },
    ]
    status = {}
    for task in tasks:
        for participant in task['participants']:
            status[participant] = status.get(participant, 0) + task['hours']
    return render_template('index.html', tasks=tasks, status=status)

@main_bp.route('/tasks/list', methods=['GET'])
def list_tasks():
    tasks = Task.query.order_by(Task.start_time.desc()).all()
    return jsonify([task.to_dict() for task in tasks])

@main_bp.route('/users/list', methods=['GET'])
def list_users():
    users = User.query.order_by(User.username).all()
    return jsonify([user.to_dict() for user in users])