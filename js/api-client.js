const API = {
    _users: JSON.parse(localStorage.getItem('api_users') || '{}'),
    _personalities: JSON.parse(localStorage.getItem('api_personalities') || '{}'),
    
    _save() {
        localStorage.setItem('api_users', JSON.stringify(this._users));
        localStorage.setItem('api_personalities', JSON.stringify(this._personalities));
    },
    
    async health() {
        return { status: 'healthy', message: 'Client-side API running' };
    },
    
    async register(data) {
        const email = data.email?.toLowerCase();
        if (!email || !data.password) {
            return { error: 'Email and password required' };
        }
        if (this._users[email]) {
            return { error: 'Email already registered' };
        }
        const userId = `user_${Object.keys(this._users).length + 1}`;
        this._users[email] = {
            id: userId,
            email,
            password: data.password,
            name: data.name || email.split('@')[0]
        };
        this._save();
        return {
            success: true,
            user: { id: userId, email, name: this._users[email].name },
            token: `token_${userId}`
        };
    },
    
    async login(data) {
        const email = data.email?.toLowerCase();
        const user = this._users[email];
        if (!user || user.password !== data.password) {
            return { error: 'Invalid credentials' };
        }
        return {
            success: true,
            user: { id: user.id, email: user.email, name: user.name },
            token: `token_${user.id}`
        };
    },
    
    _calculateTraits(answers) {
        return {
            openness: Math.round(sum(answers.slice(0, 10)) / 10 * 20),
            conscientiousness: Math.round(sum(answers.slice(10, 20)) / 10 * 20),
            extraversion: Math.round(sum(answers.slice(20, 30)) / 10 * 20),
            agreeableness: Math.round(sum(answers.slice(30, 40)) / 10 * 20),
            neuroticism: Math.round(sum(answers.slice(40, 50)) / 10 * 20)
        };
    },
    
    _getType(traits) {
        const types = [];
        if (traits.openness > 60) types.push("Explorer");
        if (traits.conscientiousness > 60) types.push("Achiever");
        if (traits.extraversion > 60) types.push("Socializer");
        if (traits.agreeableness > 60) types.push("Helper");
        if (traits.neuroticism < 40) types.push("Stabilizer");
        return types.slice(0, 2).join(" & ") || "Balanced";
    },
    
    async analyze(data) {
        const answers = data.answers;
        if (!answers || answers.length !== 50) {
            return { error: 'Need 50 answers' };
        }
        const traits = this._calculateTraits(answers);
        return { success: true, traits, personality_type: this._getType(traits) };
    },
    
    async savePersonality(data) {
        const email = data.email?.toLowerCase();
        if (!email) return { error: 'Email required' };
        const traits = data.traits || {};
        this._personalities[email] = { email, traits, personality_type: this._getType(traits) };
        this._save();
        return { success: true };
    },
    
    async getPersonality(email) {
        const pers = this._personalities[email?.toLowerCase()];
        if (!pers) return { error: 'Not found', personality: null };
        return { success: true, personality: pers };
    },
    
    async getUser(email) {
        const user = this._users[email?.toLowerCase()];
        if (!user) return { error: 'Not found' };
        return { success: true, user: { id: user.id, email: user.email, name: user.name } };
    },
    
    async getCareers(data) {
        const t = data.traits || {};
        const careers = [];
        if (t.openness > 50) careers.push({ name: "Data Scientist", match_score: 92, description: "Analyze data", skills: ["Python", "ML"] });
        if (t.conscientiousness > 50) careers.push({ name: "Software Engineer", match_score: 88, description: "Build software", skills: ["JavaScript"] });
        if (t.openness > 60 && t.conscientiousness > 60) careers.push({ name: "AI/ML Engineer", match_score: 90, description: "AI systems", skills: ["TensorFlow"] });
        if (t.extraversion > 60) careers.push({ name: "Product Manager", match_score: 85, description: "Lead products", skills: ["Leadership"] });
        if (!careers.length) careers.push({ name: "Generalist", match_score: 70, description: "Versatile role", skills: ["Communication"] });
        return { success: true, careers: careers.slice(0, 4) };
    },
    
    async getSimilarUsers(email) {
        const current = this._personalities[email?.toLowerCase()];
        if (!current) return { error: 'User not found' };
        const similar = [];
        for (const [e, p] of Object.entries(this._personalities)) {
            if (e === email) continue;
            const sim = 100 - Math.abs(current.traits.openness - p.traits.openness) * 0.5;
            if (sim > 70) {
                similar.push({
                    email: e,
                    name: this._users[e]?.name || e.split('@')[0],
                    similarity: Math.round(sim),
                    ...p.traits
                });
            }
        }
        return { success: true, similar_users: similar.sort((a, b) => b.similarity - a.similarity).slice(0, 5) };
    }
};

function sum(arr) { return arr.reduce((a, b) => a + (b || 0), 0); }

window.api = API;