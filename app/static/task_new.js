async function submitTaskForm() {
    const taskName = document.getElementById('task-name').value.trim();
    const startTime = document.getElementById('task-start-time').value.trim();
    const endTime = document.getElementById('task-end-time').value.trim();
    const description = document.getElementById('task-description').value.trim();
    const hours = document.getElementById('task-hours').value.trim();
    const usernamesTextarea = document.getElementById('username');
    const usernames = usernamesTextarea.value.split('\n').map(name => name.trim()).filter(name => name !== '');
    const resultDiv = document.getElementById('result');
    resultDiv.innerHTML = '';
    const submitButton = document.getElementById('submit');
    submitButton.disabled = true;
    
    if (!taskName || !startTime || !endTime || !description || !hours || usernames.length === 0) {
        const errorMessage = document.createElement('p');
        errorMessage.textContent = '请填写所有字段，包括至少一个参与者。';
        errorMessage.classList.add('error-message');
        resultDiv.appendChild(errorMessage);
        return;
    }
    if (startTime >= endTime) {
        const errorMessage = document.createElement('p');
        errorMessage.textContent = '开始时间必须早于结束时间。';
        errorMessage.classList.add('error-message');
        resultDiv.appendChild(errorMessage);
        return;
    }
    
    const res = await fetch('/task/add', {
        method: 'POST',
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
        successMessage.textContent = '任务添加成功！';
        successMessage.classList.add('success-message');
        resultDiv.appendChild(successMessage);
        setTimeout(() => { window.location.href = '/'; }, 1000);
    } else {
        const errorMessage = document.createElement('p');
        errorMessage.textContent = `添加任务时发生错误：${data.error}`;
        errorMessage.classList.add('error-message');
        resultDiv.appendChild(errorMessage);
        submitButton.disabled = false;
    }
}