import flask

app = flask.Flask(__name__)

@app.route('/')
def home():
    tasks = [
        {'id': 1,'name': '示例任务 1', 'start_time': '2026-10-01 08:00', 'end_time': '2026-10-01 10:00', 'description': '这是一个示例任务', 'hours': 2, 'participants': ['张三', '李四']},
        {'id': 2,'name': '示例任务 2', 'start_time': '2026-10-02 09:00', 'end_time': '2026-10-02 12:00', 'description': '这是另一个示例任务', 'hours': 3, 'participants': ['王五', '赵六']},
    ]
    status = {}
    for task in tasks:
        for participant in task['participants']:
            if participant in status:
                status[participant] += task['hours']
            else:
                status[participant] = task['hours']
    return flask.render_template('index.html', tasks=tasks, status=status)

if __name__ == '__main__':
    app.run(debug=True)