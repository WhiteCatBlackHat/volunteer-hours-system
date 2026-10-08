async function submitUserForm() {
    const usernameTextarea = document.getElementById('username');
    const usernames = usernameTextarea.value.split('\n').map(name => name.trim()).filter(name => name !== '');
    const resultDiv = document.getElementById('result');
    resultDiv.innerHTML = '';
    resultDiv.hidden = false;
    const submitButton = document.getElementById('submit');
    submitButton.disabled = true;

    if (usernames.length === 0) {
        const errorMessage = document.createElement('p');
        errorMessage.textContent = '添加参与者时发生错误：请填写至少一个参与者名';
        errorMessage.classList.add('error-message');
        resultDiv.appendChild(errorMessage);
        return;
    }

    let allOk = true, hasOk = false;

    for (const username of usernames) { // 警示后人：forEach 不会等待 async 函数完成
        const res = await fetch('/user/add', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            credentials: "same-origin",
            body: JSON.stringify({ username: username })
        });
        if (!res.ok) {
            const errorData = await res.json();
            const errorMessage = document.createElement('p');
            errorMessage.textContent = `添加参与者 ${username} 时发生错误：${errorData.error}`;
            errorMessage.classList.add('error-message');
            resultDiv.appendChild(errorMessage);
            allOk = false;
        } else {
            hasOk = true;
        }
    }
    
    if (allOk) {
        const successMessage = document.createElement('p');
        successMessage.textContent = '参与者添加成功！';
        successMessage.classList.add('success-message');
        resultDiv.appendChild(successMessage);
        if(window.clearUnsavedChanges) window.clearUnsavedChanges();
        setTimeout(() => { window.location.href = '/'; }, 1000);
    } else {
        submitButton.disabled = false;
        if (hasOk) {
            const partialSuccessMessage = document.createElement('p');
            partialSuccessMessage.textContent = '部分参与者添加成功，请查看上方错误信息';
            partialSuccessMessage.classList.add('success-message');
            resultDiv.appendChild(partialSuccessMessage);
        }
    }
}

document.addEventListener('DOMContentLoaded', () => { document.getElementById('result').hidden = true; });