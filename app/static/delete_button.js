async function deleteUser(username) {
    if (confirm(`确定要删除参与者 ${username} 吗？`)) {
        const res = await fetch(`/user/delete/${username}`, { 
            method: 'DELETE',
            credentials: 'same-origin'
        });
        const data = await res.json();
        if (!res.ok) {
            alert(`删除参与者 ${username} 时发生错误：` + data.error);
        }
        location.href = '/';
    }
}
async function deleteTask(taskId, taskName) {
    if (confirm(`确定要删除任务 ${taskName} 吗？`)) {
        const res = await fetch(`/task/delete/${taskId}`, { 
            method: 'DELETE',
            credentials: 'same-origin'
        });
        const data = await res.json();
        if (!res.ok) {
            alert(`删除任务 ${taskName} 时发生错误：` + data.error);
        }
        location.href = '/';
    }
}