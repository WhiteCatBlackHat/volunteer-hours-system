async function init() {
    const taskRes = await fetch('task/list');
    const tasks = await taskRes.json();
    const taskUl = document.getElementById('task-ul');
    tasks.sort((a, b) => (a.start_time != b.start_time ? b.start_time - a.start_time : b.end_time - a.end_time));
    tasks.forEach(task => {
        const li = document.createElement('li');
        li.innerHTML = `
            <p><span>${task.name}</span> <a href="/task/edit/${task.id}" class="edit-btn">编辑</a>&nbsp;<button class="delete-btn" data-task-id="${task.id}" data-task-name="${task.name}">删除</button></p>
            <p>任务时间：<span>${formatDateTime(task.start_time)}</span> ~ <span>${formatDateTime(task.end_time)}</span></p>
            <p>任务内容：<span>${task.description}</span></p>
            <p>志愿时长：<span>${task.hours}</span> 小时</p>
            <p>参与人员：<span>${task.users.map(user => `<a href="/user/${user}">${user}</a>`).join('、')}</span></p>
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
    let lis = [];
    for (const user of users) {
        const li = document.createElement('li');
        const hoursRes = await fetch(`user/${user.username}/total_hours`);
        const hoursJson = await hoursRes.json();
        const hours = hoursJson.total_hours || 0;
        li.innerHTML = `<a href="/user/${user.username}">${user.username}</a>：<span>${hours}</span> 小时 <a href="/user/edit/${user.username}" class="edit-btn">编辑</a>&nbsp;<button class="delete-btn" data-username="${user.username}">删除</button>`;
        lis.push(li);
        li.querySelector('.delete-btn').addEventListener('click', () => { deleteUser(user.username); });
        li.dataset.username = user.username;
    }
    lis.sort((a, b) => a.dataset.username.localeCompare(b.dataset.username));
    lis.forEach(li => statusUl.appendChild(li));
    console.log(lis);
    if (users.length === 0) {
        const li = document.createElement('li');
        li.innerHTML = `<p>暂无志愿时长统计</p>`;
        statusUl.appendChild(li);
    }
}
document.addEventListener('DOMContentLoaded', init);