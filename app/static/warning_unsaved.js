function init() {
    const forms = document.querySelector('form');
    if (!forms) return;
    
    window.hasUnsavedChanges = false;
    function trackChanges(ele) {
        ele.addEventListener('input', () => { hasUnsavedChanges = true; });
        ele.addEventListener('change', () => { hasUnsavedChanges = true; });
    }
    forms.querySelectorAll('input, textarea, select').forEach(trackChanges);
    
    window.addEventListener('beforeunload', (e) => {
        if (!hasUnsavedChanges) return;
        e.preventDefault();
        e.returnValue = '';
        return '';
    });
}
document.addEventListener('DOMContentLoaded', init);