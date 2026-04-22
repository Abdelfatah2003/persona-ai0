const api = {
    getApiBase() {
        const path = window.location.pathname;
        if (path.startsWith('/api')) return '';
        const base = document.querySelector('meta[name="api-base"]');
        return base ? base.getAttribute('content') : '/api';
    },

    async analyzePersonality(answers) {
        try {
            const response = await fetch(`/api/personality/analyze`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ answers })
            });
            return response.json();
        } catch (error) {
            console.error('API Error:', error);
            return null;
        }
    },

    async analyzeText(text) {
        try {
            const response = await fetch(`/api/personality/analyze-text`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ text })
            });
            return response.json();
        } catch (error) {
            console.error('API Error:', error);
            return null;
        }
    },

    async getCareerRecommendations(traits) {
        try {
            const response = await fetch(`/api/recommendations/careers`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(traits)
            });
            return response.json();
        } catch (error) {
            console.error('API Error:', error);
            return null;
        }
    },

    async getSimilarUsers(userId, traits) {
        try {
            const response = await fetch(`/api/recommendations/users`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ userId, traits })
            });
            return response.json();
        } catch (error) {
            console.error('API Error:', error);
            return null;
        }
    },

    async savePersonality(userId, traits) {
        try {
            const response = await fetch(`/api/personality/save`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ userId, ...traits })
            });
            return response.ok;
        } catch (error) {
            console.error('API Error:', error);
            return false;
        }
    }
};