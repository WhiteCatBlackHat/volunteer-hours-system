function init() {
    // console.log('Initializing script...');
    document.querySelectorAll('.edit-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            location.href = '/edit/' + btn.dataset.taskId;
            alert('编辑功能尚未实现。');
        });
    });
    document.querySelectorAll('.delete-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            if (confirm('确定要删除任务 ' + btn.dataset.taskName + ' 吗？')) {
                alert('删除功能尚未实现。');
            }
        });
    });
}
document.addEventListener('DOMContentLoaded', init);