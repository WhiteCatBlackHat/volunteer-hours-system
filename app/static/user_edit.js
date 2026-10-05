async function submitEditUserForm() {
    const newUsername = document.getElementById('username').value.trim();
    const originalUsername = document.getElementById('edit-user-form').dataset.originalUsername;
    const resultDiv = document.getElementById('result');
    resultDiv.innerHTML = '';
    
    if (!newUsername || newUsername === originalUsername) {
        const errorMessage = document.createElement('p');
        errorMessage.textContent = '请填写一个新的参与者名。';
        errorMessage.classList.add('error-message');
        resultDiv.appendChild(errorMessage);
        return;
    }
    
    const res = await fetch(`/user/edit/${originalUsername}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ new_username: newUsername })
    });
    
    const data = await res.json();
    if (res.ok) {
        resultDiv.innerHTML = '<p class="success-message">参与者信息更新成功！</p>';
        setTimeout(() => { window.location.href = '/'; }, 1000);
    } else {
        const errorMessage = document.createElement('p');
        errorMessage.textContent = data.error || '更新参与者信息时发生错误。';
        errorMessage.classList.add('error-message');
        resultDiv.appendChild(errorMessage);
    }
}