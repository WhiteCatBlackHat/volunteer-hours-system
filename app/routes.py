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

@main_bp.route('/tasks/add', methods=['POST'])
def add_task():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No input data provided'}), 400

    name = data.get('name')
    start_time_str = data.get('start_time')
    end_time_str = data.get('end_time')
    hours = data.get('hours')
    description = data.get('description', '')
    user_names = data.get('user_names', [])

    if not all([name, start_time_str, end_time_str, hours]):
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        start_time = datetime.fromisoformat(start_time_str)
        end_time = datetime.fromisoformat(end_time_str)
    except ValueError:
        return jsonify({'error': 'Invalid date format'}), 400

    task = Task(name=name, start_time=start_time, end_time=end_time, hours=hours, description=description)

    for user_name in user_names:
        user = User.query.filter_by(username=user_name).first()
        if user:
            task.users.append(user)
        else:
            return jsonify({'error': f'User {user_name} not found'}), 404

    db.session.add(task)
    db.session.commit()

    return jsonify(task.to_dict()), 201

@main_bp.route('/users/list', methods=['GET'])
def list_users():
    users = User.query.order_by(User.username).all()
    return jsonify([user.to_dict() for user in users])

@main_bp.route('/users/add', methods=['POST'])
def add_user():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No input data provided'}), 400

    username = data.get('username')
    if not username:
        return jsonify({'error': 'Missing required field: username'}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({'error': 'Username already exists'}), 400

    user = User(username=username)
    db.session.add(user)
    db.session.commit()

    return jsonify(user.to_dict()), 201