const API_BASE = window.location.origin;

function getApiUrl(path) {
    return `${API_BASE}${path}`;
}

async function apiCall(endpoint, options = {}) {
    try {
        const response = await fetch(getApiUrl(endpoint), {
            ...options,
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            }
        });
        return response;
    } catch (error) {
        console.error('API Error:', error);
        throw error;
    }
}