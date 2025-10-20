document.addEventListener('DOMContentLoaded', function() {
    // Form validation for login and register
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(event) {
            const username = form.querySelector('input[name="username"]');
            const password = form.querySelector('input[name="password"]');
            const role = form.querySelector('select[name="role"]');

            if (username && username.value.trim() === '') {
                event.preventDefault();
                alert('Por favor, preencha o campo de usuário.');
                return;
            }
            if (password && password.value.trim() === '') {
                event.preventDefault();
                alert('Por favor, preencha o campo de senha.');
                return;
            }
            if (role && role.value === '') {
                event.preventDefault();
                alert('Por favor, selecione um papel.');
                return;
            }
        });
    });

    // Confirmation dialog for delete resource
    const deleteForms = document.querySelectorAll('form[action*="/resources/delete/"]');
    deleteForms.forEach(form => {
        form.addEventListener('submit', function(event) {
            if (!confirm('Tem certeza que deseja excluir este recurso?')) {
                event.preventDefault();
            }
        });
    });

    // Auto-dismiss flash messages after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.classList.add('fade');
            alert.addEventListener('transitionend', () => alert.remove());
        }, 5000);
    });
});