const API_BASE_URL = 'http://localhost:8000/api/v1';

class API {
    static getHeaders() {
        const headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        };
        const token = localStorage.getItem('access_token');
        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }
        return headers;
    }

    static async request(endpoint, options = {}) {
        const url = `${API_BASE_URL}${endpoint}`;
        const headers = this.getHeaders();

        // If body is FormData, remove Content-Type to let browser set it
        if (options.body instanceof FormData) {
            delete headers['Content-Type'];
        }

        const config = {
            ...options,
            headers: {
                ...headers,
                ...options.headers
            }
        };

        try {
            const response = await fetch(url, config);

            if (response.status === 401) {
                // Unauthorized - clear token and redirect to login
                localStorage.removeItem('access_token');
                window.location.href = 'login.html';
                return;
            }

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.detail || 'Something went wrong');
            }

            return data;
        } catch (error) {
            console.error('API Request Failed:', error);
            throw error;
        }
    }

    static async get(endpoint) {
        return this.request(endpoint, { method: 'GET' });
    }

    static async post(endpoint, body) {
        // Handle both JSON and FormData
        const isFormData = body instanceof FormData;
        return this.request(endpoint, {
            method: 'POST',
            body: isFormData ? body : JSON.stringify(body)
        });
    }

    static logout() {
        localStorage.removeItem('access_token');
        window.location.href = 'index.html';
    }

    static isAuthenticated() {
        return !!localStorage.getItem('access_token');
    }
}
