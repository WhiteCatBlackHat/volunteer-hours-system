async function submitEditUserForm() {
    const newUsername = document.getElementById('username').value.trim();
    const originalUsername = document.getElementById('edit-user-form').dataset.originalUsername;
    const resultDiv = document.getElementById('result');
    resultDiv.innerHTML = '';
    resultDiv.hidden = false;
    const submitButton = document.getElementById('submit');
    submitButton.disabled = true;
    
    if (!newUsername || newUsername === originalUsername) {
        const errorMessage = document.createElement('p');
        errorMessage.textContent = '编辑参与者信息时发生错误：请填写一个新的参与者名';
        errorMessage.classList.add('error-message');
        resultDiv.appendChild(errorMessage);
        return;
    }
    
    const res = await fetch(`/user/edit/${originalUsername}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        credentials: "same-origin",
        body: JSON.stringify({ new_username: newUsername })
    });
    
    const data = await res.json();
    if (res.ok) {
        resultDiv.innerHTML = '<p class="success-message">参与者信息更新成功！</p>';
        if(window.clearUnsavedChanges) window.clearUnsavedChanges();
        setTimeout(() => { window.location.href = '/'; }, 1000);
    } else {
        const errorMessage = document.createElement('p');
        errorMessage.textContent = `编辑参与者信息时发生错误：${data.error}`;
        errorMessage.classList.add('error-message');
        resultDiv.appendChild(errorMessage);
        submitButton.disabled = false;
    }
}

document.addEventListener('DOMContentLoaded', () => { document.getElementById('result').hidden = true; });