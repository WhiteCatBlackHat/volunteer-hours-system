function deleteUser(username) {
    if (confirm(`确定要删除参与者 ${username} 吗？`)) {
        fetch(`/user/delete/${username}`, { method: 'DELETE' });
        location.href = '/';
    }
}