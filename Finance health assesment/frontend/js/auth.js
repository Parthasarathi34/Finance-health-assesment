document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('loginForm');
    const registerForm = document.getElementById('registerForm');

    if (loginForm) {
        loginForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            const errorDiv = document.getElementById('error-message');

            errorDiv.classList.add('d-none');
            const btn = e.target.querySelector('button[type="submit"]');
            const originalBtnText = btn.innerHTML;
            btn.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Loading...';
            btn.disabled = true;

            try {
                // Determine if we need to use FormData (OAuth2PasswordRequestForm expects form data)
                const formData = new FormData();
                formData.append('username', email); // OAuth2 expects 'username'
                formData.append('password', password);

                const response = await API.post('/auth/login', formData);

                if (response.access_token) {
                    localStorage.setItem('access_token', response.access_token);
                    window.location.href = 'dashboard.html';
                }
            } catch (error) {
                errorDiv.textContent = error.message || 'Login failed. Please check your credentials.';
                errorDiv.classList.remove('d-none');
            } finally {
                btn.innerHTML = originalBtnText;
                btn.disabled = false;
            }
        });
    }

    if (registerForm) {
        registerForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const fullName = document.getElementById('fullName').value;
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            const errorDiv = document.getElementById('error-message');

            errorDiv.classList.add('d-none');
            const btn = e.target.querySelector('button[type="submit"]');
            const originalBtnText = btn.innerHTML;
            btn.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Registration...';
            btn.disabled = true;

            try {
                await API.post('/users/', {
                    email: email,
                    password: password,
                    full_name: fullName,
                    is_active: true
                });

                // On success, redirect to login with a success message (could be improved)
                alert('Registration successful! Please login.');
                window.location.href = 'login.html';
            } catch (error) {
                errorDiv.textContent = error.message || 'Registration failed.';
                errorDiv.classList.remove('d-none');
            } finally {
                btn.innerHTML = originalBtnText;
                btn.disabled = false;
            }
        });
    }
});
