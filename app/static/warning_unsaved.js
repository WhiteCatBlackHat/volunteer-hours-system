(function () {
    function init() {
        const form = document.querySelector('form');
        if (!form) return;

        window.hasUnsavedChanges = false;

        function trackChanges(ele) {
            ele.addEventListener('input', () => { window.hasUnsavedChanges = true; });
            ele.addEventListener('change', () => { window.hasUnsavedChanges = true; });
        }
        form.querySelectorAll('input, textarea, select').forEach(trackChanges);

        window.addEventListener('beforeunload', (e) => {
            if (!window.hasUnsavedChanges) return;
            e.preventDefault();
            e.returnValue = '';
            return '';
        });

        // 暴露给其他脚本
        window.clearUnsavedChanges = function () {
            window.hasUnsavedChanges = false;
        };
    }

    document.addEventListener('DOMContentLoaded', init);
})();