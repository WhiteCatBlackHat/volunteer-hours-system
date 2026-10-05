from datetime import datetime
from .models import Task, User, task_users
from flask import Blueprint, render_template, jsonify, request, current_app
from .extentions import db

main_bp = Blueprint('main', __name__)

# 美丽的主页
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

# 获取任务列表
@main_bp.route('/task/list', methods=['GET'])
def list_tasks():
    tasks = Task.query.order_by(Task.start_time.desc()).all()
    return jsonify([task.to_dict() for task in tasks])

# 添加任务
@main_bp.route('/task/add', methods=['POST'])
def add_task():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No input data provided'}), 400

    name = data.get('name')
    start_time_str = data.get('start_time')
    end_time_str = data.get('end_time')
    hours = data.get('hours')
    description = data.get('description', '')
    usernames = data.get('usernames', [])

    if not all([name, start_time_str, end_time_str, hours]):
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        start_time = datetime.fromisoformat(start_time_str)
        end_time = datetime.fromisoformat(end_time_str)
    except ValueError:
        return jsonify({'error': 'Invalid date format'}), 400

    task = Task(name=name, start_time=start_time, end_time=end_time, hours=hours, description=description)

    for username in usernames:
        user = User.query.filter_by(username=username).first()
        if user:
            task.users.append(user)
        else:
            return jsonify({'error': f'User {username} not found'}), 404

    db.session.add(task)
    db.session.commit()

    return jsonify(task.to_dict()), 201

# 删除任务
@main_bp.route('/task/delete/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return jsonify({'error': 'Task not found'}), 404

    db.session.delete(task)
    db.session.commit()
    return jsonify({'message': 'Task deleted successfully'}), 200

# 编辑任务
@main_bp.route('/task/edit/<int:task_id>', methods=['PUT'])
def edit_task(task_id):
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No input data provided'}), 400

    task = Task.query.get(task_id)
    if not task:
        return jsonify({'error': 'Task not found'}), 404

    # Update task fields
    task.name = data.get('name', task.name)
    task.description = data.get('description', task.description)

    # Update time fields if provided
    if 'start_time' in data:
        try:
            task.start_time = datetime.fromisoformat(data['start_time'])
        except ValueError:
            return jsonify({'error': 'Invalid start_time format'}), 400

    if 'end_time' in data:
        try:
            task.end_time = datetime.fromisoformat(data['end_time'])
        except ValueError:
            return jsonify({'error': 'Invalid end_time format'}), 400

    # Update hours if provided
    if 'hours' in data:
        task.hours = data['hours']

    db.session.commit()
    return jsonify(task.to_dict()), 200

# 获取参与者列表
@main_bp.route('/user/list', methods=['GET'])
def list_users():
    users = User.query.order_by(User.username).all()
    return jsonify([user.to_dict() for user in users])

# 新建参与者页面
@main_bp.route('/user/new')
def new_user_page():
    return render_template('user_new.html')

# 添加参与者
@main_bp.route('/user/add', methods=['POST'])
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

# 删除参与者
@main_bp.route('/user/delete/<username>', methods=['DELETE'])
def delete_user(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404

    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted successfully'}), 200

# 编辑参与者页面
@main_bp.route('/user/edit/<username>')
def edit_user_page(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404

    return render_template('user_edit.html', user=user)

# 编辑参与者
@main_bp.route('/user/edit/<username>', methods=['PUT'])
def edit_user(username):
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No input data provided'}), 400

    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404

    new_username = data.get('new_username')
    if new_username:
        if User.query.filter_by(username=new_username).first():
            return jsonify({'error': 'Username already exists'}), 400
        user.username = new_username
        db.session.commit()
        return jsonify(user.to_dict()), 200
    else:
        return jsonify({'error': 'No new username provided'}), 400

# 参与者详情页面
@main_bp.route('/user/<username>')
def user_detail_page(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404

    return render_template('user.html', user=user)

# 计算某个参与者的总志愿时长
@main_bp.route('/user/<username>/total_hours', methods=['GET'])
def total_hours(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404

    total_hours = sum(task.hours for task in user.tasks)
    return jsonify({'username': username, 'total_hours': total_hours})