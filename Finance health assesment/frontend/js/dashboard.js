document.addEventListener('DOMContentLoaded', () => {
    // Redirect if not authenticated
    if (!API.isAuthenticated()) {
        window.location.href = 'login.html';
        return;
    }

    const logoutBtn = document.getElementById('logoutBtn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', (e) => {
            e.preventDefault();
            API.logout();
        });
    }

    loadDashboardData();
    setupForms();
});

async function loadDashboardData() {
    try {
        const user = await API.get('/users/me');
        document.getElementById('userName').textContent = user.full_name || user.email;

        // Fetch user's companies (assuming an endpoint exists or we fetch companies for user)
        // Since we don't have a direct "get all companies" endpoint in the snippets I saw, 
        // I will assume there might be one or I'll implement the "Create Company" flow first. 
        // Wait, looking at assessments.py, it takes company_id. 
        // I'll add a 'Mock' load for now or try to fetch if I can invoke an endpoint.
        // Actually, looking at the code I saw:
        // assessments.py -> get /{company_id}
        // financials.py -> get /{company_id}
        // I don't see a "list companies" endpoint. Use a placeholder or assume ID 1 for demo if no list exists.
        // But better, let's look at `app/api/endpoints/companies.py`? 
        // I haven't seen that file. I'll need to create a company first.

        // For this demo, let's keep it simple: List is empty initially.
        // We will implement "Add Company" which calls POST /companies/ (if it exists)
        // Wait, I saw models/company.py imported but didn't view endpoints/companies.py.
        // Let's assume standard REST.

        // Changing strategy: I'll try to fetch companies. If fail, show empty state.
        // Since I can't confirm the endpoint, I'll assume GET /companies/ comes from a router I didn't see details of but is likely there.
        // If not, I'll add a note.
        // Actually, I should probably check if endpoints/companies.py exists. 
        // `ls app/api/endpoints` showed: assessments, auth, financials, users. NO companies.py!
        // This is a gap in backend. 
        // User asked for frontend for the *existing* backend.
        // If there is no endpoint to create a company, I can't really do much.
        // However, `assessments.py` queries `Company`.
        // I'll assume for the sake of this task I might need to create a company via a seed script or add the endpoint.
        // BUT, I'm just making the frontend.
        // I will implement the Frontend assuming the backend *should* have it.
        // If it fails, I'll report it.
        // actually, I'll add a "Create Company" modal that *tries* to POST to /companies/.

        // HACK: For the purpose of the "create frontend" task, if the backend lacks the endpoint, 
        // I will simulate it or ask user. 
        // BUT, looking at `financials.py`, it takes `company_id`.
        // I'll assumme the user knows their company ID or I'll try to hit `/companies/`.

        // Let's try to list companies assuming GET /companies/ exists.
        const companies = await API.get('/companies/');
        renderCompanies(companies);

    } catch (error) {
        console.warn('Could not load companies. Endpoint might be missing.', error);
        document.getElementById('companiesList').innerHTML = `
            <div class="col-12 text-center p-5">
                <p class="text-muted">Could not load companies. The backend might be missing a 'companies' endpoint.</p>
                <button class="btn btn-primary-custom" data-bs-toggle="modal" data-bs-target="#addCompanyModal">
                    Add Company
                </button>
            </div>
        `;
    }
}

function renderCompanies(companies) {
    const list = document.getElementById('companiesList');
    list.innerHTML = '';

    if (companies.length === 0) {
        list.innerHTML = `
            <div class="col-12 text-center p-5">
                <p class="text-muted">No companies found. Add one to get started.</p>
                <button class="btn btn-primary-custom" data-bs-toggle="modal" data-bs-target="#addCompanyModal">
                    Add Company
                </button>
            </div>
        `;
        return;
    }

    companies.forEach(company => {
        const card = document.createElement('div');
        card.className = 'col-md-6 col-lg-4';
        card.innerHTML = `
            <div class="card card-custom h-100">
                <div class="card-body">
                    <h5 class="fw-bold mb-2">${company.name}</h5>
                    <p class="text-muted small mb-3">${company.industry || 'Industry not specified'}</p>
                    
                    <div class="d-grid gap-2">
                        <button onclick="viewAssessment(${company.id})" class="btn btn-outline-primary btn-sm">
                            View Assessment
                        </button>
                        <button onclick="openUploadModal(${company.id})" class="btn btn-outline-secondary btn-sm">
                            Upload Financials
                        </button>
                    </div>
                </div>
            </div>
        `;
        list.appendChild(card);
    });
}

async function setupForms() {
    // Add Company
    const addCompanyForm = document.getElementById('addCompanyForm');
    if (addCompanyForm) {
        addCompanyForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const name = document.getElementById('companyName').value;
            const industry = document.getElementById('industry').value;

            try {
                // Assuming POST /companies/ endpoint
                await API.post('/companies/', { name, industry });

                // Close modal and reload
                const modal = bootstrap.Modal.getInstance(document.getElementById('addCompanyModal'));
                modal.hide();
                loadDashboardData();
            } catch (error) {
                alert('Failed to create company: ' + error.message);
            }
        });
    }

    // Upload Financials
    const uploadForm = document.getElementById('uploadForm');
    if (uploadForm) {
        uploadForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const companyId = document.getElementById('uploadCompanyId').value;
            const fileInput = document.getElementById('financialFile');
            const file = fileInput.files[0];

            if (!file) return;

            const formData = new FormData();
            formData.append('file', file);

            try {
                await API.post(`/financials/upload/${companyId}`, formData);
                alert('File uploaded successfully!');
                const modal = bootstrap.Modal.getInstance(document.getElementById('uploadModal'));
                modal.hide();
                // Optionally refresh assessment
            } catch (error) {
                alert('Upload failed: ' + error.message);
            }
        });
    }
}

// Global functions for inline onclick handlers
window.openUploadModal = (companyId) => {
    document.getElementById('uploadCompanyId').value = companyId;
    new bootstrap.Modal(document.getElementById('uploadModal')).show();
};

window.viewAssessment = async (companyId) => {
    try {
        // Try to generate or fetch assessment
        // First, let's try to generate it fresh
        const assessment = await API.post(`/assessments/${companyId}/generate`);
        showAssessmentResult(assessment);
    } catch (error) {
        alert('Could not generate assessment. Please ensure financial data is uploaded.');
    }
};

function showAssessmentResult(assessment) {
    const modalHtml = `
        <div class="modal fade" id="resultModal" tabindex="-1">
            <div class="modal-dialog modal-lg">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title fw-bold">Assessment Results</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        <div class="row text-center mb-4">
                            <div class="col-md-6">
                                <p class="text-muted mb-1">Overall Score</p>
                                <h2 class="display-4 fw-bold text-primary">${assessment.overall_score}</h2>
                            </div>
                            <div class="col-md-6">
                                <p class="text-muted mb-1">Risk Level</p>
                                <h2 class="display-4 fw-bold risk-level-${assessment.risk_level.toLowerCase()}">${assessment.risk_level}</h2>
                            </div>
                        </div>
                        <div class="bg-light p-3 rounded">
                            <pre class="mb-0" style="white-space: pre-wrap;">${JSON.stringify(assessment.details, null, 2)}</pre>
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                    </div>
                </div>
            </div>
        </div>
    `;

    // Remove existing if any
    const existing = document.getElementById('resultModal');
    if (existing) existing.remove();

    document.body.insertAdjacentHTML('beforeend', modalHtml);
    new bootstrap.Modal(document.getElementById('resultModal')).show();
}
