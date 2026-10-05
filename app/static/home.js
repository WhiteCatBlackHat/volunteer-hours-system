async function init() {
    const taskRes = await fetch('task/list');
    const tasks = await taskRes.json();
    const taskUl = document.getElementById('task-ul');
    // console.log(tasks);
    tasks.forEach(task => {
        const li = document.createElement('li');
        li.innerHTML = `
            <p><span>${task.name}</span> <a href="/task/edit/${task.id}" class="edit-btn">编辑</a>&nbsp;<button class="delete-btn" data-task-id="${task.id}" data-task-name="${task.name}">删除</button></p>
            <p>任务时间：<span>${formatDateTime(task.start_time)}</span> ~ <span>${formatDateTime(task.end_time)}</span></p>
            <p>任务内容：<span>${task.description}</span></p>
            <p>志愿时长：<span>${task.hours}</span> 小时</p>
            <p>参与人员：<span>${task.users.join('、')}</span></p>
        `;
        li.querySelector('.delete-btn').addEventListener('click', () => { deleteTask(task.id, task.name); });
        taskUl.appendChild(li);
    });
    if (tasks.length === 0) {
        const li = document.createElement('li');
        li.innerHTML = `<p>暂无任务</p>`;
        taskUl.appendChild(li);
    }
    
    const userRes = await fetch('user/list');
    const users = await userRes.json();
    const statusUl = document.getElementById('status-ul');
    // console.log(users);
    async function fetchUserHours(user) {
        const hoursRes = await fetch(`user/${user.username}/total_hours`);
        const hours = await hoursRes.json();
        return hours['total_hours'] || 0;
    }
    users.forEach(user => {
        const li = document.createElement('li');
        fetchUserHours(user).then(hours => {
            li.innerHTML = `<a href="/user/${user.username}">${user.username}</a>：<span>${hours}</span> 小时 <a href="/user/edit/${user.username}" class="edit-btn">编辑</a>&nbsp;<button class="delete-btn" data-username="${user.username}">删除</button>`;
            statusUl.appendChild(li);
            li.querySelector('.delete-btn').addEventListener('click', () => { deleteUser(user.username); });
        });
    });
    if (users.length === 0) {
        const li = document.createElement('li');
        li.innerHTML = `<p>暂无志愿时长统计</p>`;
        statusUl.appendChild(li);
    }
}
document.addEventListener('DOMContentLoaded', init);