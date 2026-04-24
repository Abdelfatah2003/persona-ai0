const API_BASE = 'https://persona-ai0.onrender.com';

const API = {
    async health() {
        const res = await fetch(`${API_BASE}/api/health`);
        return res.json();
    },
    
    async register(data) {
        const res = await fetch(`${API_BASE}/api/auth/register`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        return res.json();
    },
    
    async login(data) {
        const res = await fetch(`${API_BASE}/api/auth/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        return res.json();
    },
    
    async analyze(data) {
        const res = await fetch(`${API_BASE}/api/personality/analyze`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        return res.json();
    },
    
    async savePersonality(data) {
        const res = await fetch(`${API_BASE}/api/personality/save`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        return res.json();
    },
    
    async getPersonality(email) {
        const res = await fetch(`${API_BASE}/api/personality/get/${encodeURIComponent(email)}`);
        return res.json();
    },
    
    async getUser(email) {
        const res = await fetch(`${API_BASE}/api/auth/user/${encodeURIComponent(email)}`);
        return res.json();
    },
    
    async getCareers(traits) {
        const res = await fetch(`${API_BASE}/api/recommendations/careers`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(traits)
        });
        return res.json();
    },
    
    async getSimilarUsers(email) {
        const res = await fetch(`${API_BASE}/api/recommendations/users/${encodeURIComponent(email)}`);
        return res.json();
    }
};

window.api = API;