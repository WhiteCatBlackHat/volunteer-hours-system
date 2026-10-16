async function init() {
    loadTasks();
    
    const userRes = await fetch('user/list');
    const users = await userRes.json();
    const statusUl = document.getElementById('status-ul');
    users.forEach(user => {
        const li = document.createElement('li');
        const hours = user.total_hours || 0;
        li.innerHTML = `<a href="/user/${user.username}">${user.username}</a>：<span>${hours}</span> 小时 <a href="/user/edit/${user.username}" class="edit-btn">编辑</a>&nbsp;<button class="delete-btn" data-username="${user.username}">删除</button>`;
        li.querySelector('.delete-btn').addEventListener('click', () => { deleteUser(user.username); });
        li.dataset.username = user.username;
        statusUl.appendChild(li);
    });
    if (users.length === 0) {
        const li = document.createElement('li');
        li.innerHTML = `<p>暂无志愿时长统计</p>`;
        statusUl.appendChild(li);
    }
}
document.addEventListener('DOMContentLoaded', init);

async function loadTasks(page = 1) {
    const taskRes = await fetch(`task/list?page=${page}`);
    const taskData = await taskRes.json();
    const tasks = taskData.items;
    const taskUl = document.getElementById('task-ul');
    const showMoreTaskBtn = document.getElementById('show-more-task-btn');

    if (taskData.total === 0) {
        const li = document.createElement('li');
        li.innerHTML = `<p>暂无任务</p>`;
        taskUl.appendChild(li);
        showMoreTaskBtn.style.display = 'none';
        return;
    }

    tasks.sort((a, b) => (a.start_time != b.start_time ? b.start_time - a.start_time : b.end_time - a.end_time));
    tasks.forEach(task => {
        const li = document.createElement('li');
        li.innerHTML = `
            <p><span>${task.name}</span> <a href="/task/edit/${task.id}" class="edit-btn">编辑</a>&nbsp;<button class="delete-btn" data-task-id="${task.id}" data-task-name="${task.name}">删除</button></p>
            <p>任务时间：<span>${formatDateTime(task.start_time)}</span> ~ <span>${formatDateTime(task.end_time)}</span></p>
            <p>任务内容：<span>${task.description}</span></p>
            <p>志愿时长：<span>${task.hours}</span> 小时</p>
            <p>参与人员：<span>${task.users.length > 0 ? task.users.map(user => `<a href="/user/${user}">${user}</a>`).join('、') : '无'}</span></p>
        `;
        li.querySelector('.delete-btn').addEventListener('click', () => { deleteTask(task.id, task.name); });
        taskUl.appendChild(li);
    });

    if (taskData.page >= taskData.pages) {
        showMoreTaskBtn.style.display = 'none';
    } else {
        showMoreTaskBtn.style.display = 'block';
        showMoreTaskBtn.onclick = () => { loadTasks(taskData.page + 1); };
    }
}