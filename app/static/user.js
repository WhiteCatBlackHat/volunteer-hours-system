async function loadUserDetails(username) {
    const totalHoursRes = await fetch(`/user/${username}/total_hours`);
    const totalHoursData = await totalHoursRes.json();
    const totalHours = totalHoursData['total_hours'] || 0;
    document.getElementById('total-hours').textContent = totalHours;
    
    const tasksRes = await fetch(`/task/list`);
    const tasks = await tasksRes.json();
    const userTasks = tasks.filter(task => task.users.includes(username));
    console.log(userTasks);
    
    const taskUl = document.getElementById('task-ul');
    userTasks.forEach(task => {
        const li = document.createElement('li');
        li.innerHTML = `
            <p><span>${task.name}</span></p>
            <p>任务时间：<span>${formatDateTime(task.start_time)}</span> ~ <span>${formatDateTime(task.end_time)}</span></p>
            <p>任务内容：<span>${task.description}</span></p>
            <p>志愿时长：<span>${task.hours}</span> 小时</p>
        `;
        taskUl.appendChild(li);
    });
    
    if (userTasks.length === 0) {
        const li = document.createElement('li');
        li.innerHTML = `<p>暂无任务</p>`;
        taskUl.appendChild(li);
    }
    
    document.querySelector('.delete-btn').addEventListener('click', () => { deleteUser(username); });
}

document.addEventListener('DOMContentLoaded', () => { loadUserDetails(document.getElementById('username').dataset.username); });