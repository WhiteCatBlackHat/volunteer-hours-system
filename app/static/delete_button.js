function deleteUser(username) {
    if (confirm(`确定要删除参与者 ${username} 吗？`)) {
        fetch(`/user/delete/${username}`, { method: 'DELETE' });
        location.href = '/';
    }
}
function deleteTask(taskId, taskName) {
    if (confirm(`确定要删除任务 ${taskName} 吗？`)) {
        fetch(`/task/delete/${taskId}`, { method: 'DELETE' });
        location.href = '/';
    }
}