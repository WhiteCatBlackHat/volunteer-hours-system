async function submitTaskForm() {
    const taskForm = document.getElementById('task-form');
    const taskId = taskForm.dataset.taskId;
    const taskName = document.getElementById('task-name').value.trim();
    const startTime = document.getElementById('task-start-time').value.trim();
    const endTime = document.getElementById('task-end-time').value.trim();
    const description = document.getElementById('task-description').value.trim();
    const hours = document.getElementById('task-hours').value.trim();
    const usernamesTextarea = document.getElementById('username');
    const usernames = usernamesTextarea.value.split('\n').map(name => name.trim()).filter(name => name !== '');
    const resultDiv = document.getElementById('result');
    resultDiv.innerHTML = '';
    resultDiv.hidden = false;
    const submitButton = document.getElementById('submit');
    submitButton.disabled = true;
    
    if (!taskName || !startTime || !endTime || !description || !hours || usernames.length === 0) {
        const errorMessage = document.createElement('p');
        errorMessage.textContent = '编辑任务时发生错误：请填写所有字段，包括至少一个参与者。';
        errorMessage.classList.add('error-message');
        resultDiv.appendChild(errorMessage);
        submitButton.disabled = false;
        return;
    }
    if (startTime >= endTime) {
        const errorMessage = document.createElement('p');
        errorMessage.textContent = '编辑任务时发生错误：开始时间必须早于结束时间。';
        errorMessage.classList.add('error-message');
        resultDiv.appendChild(errorMessage);
        submitButton.disabled = false;
        return;
    }
    
    const res = await fetch(`/task/edit/${taskId}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        credentials: "same-origin",
        body: JSON.stringify({
            name: taskName,
            start_time: startTime,
            end_time: endTime,
            description: description,
            hours: hours,
            usernames: usernames
        })
    });
    const data = await res.json();
    
    if (res.ok) {
        const successMessage = document.createElement('p');
        successMessage.textContent = '任务编辑成功！';
        successMessage.classList.add('success-message');
        resultDiv.appendChild(successMessage);
        if(window.clearUnsavedChanges) window.clearUnsavedChanges();
        setTimeout(() => { window.location.href = '/'; }, 1000);
    } else {
        const errorMessage = document.createElement('p');
        errorMessage.textContent = `编辑任务时发生错误：${data.error}`;
        errorMessage.classList.add('error-message');
        resultDiv.appendChild(errorMessage);
        submitButton.disabled = false;
    }
}

document.addEventListener('DOMContentLoaded', () => { document.getElementById('result').hidden = true; });