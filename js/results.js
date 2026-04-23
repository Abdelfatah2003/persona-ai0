const careersData = [
    {
        name: "Software Engineer",
        description: "Design and build software solutions",
        skills: ["Python", "JavaScript", "Data Structures"],
        match: 95
    },
    {
        name: "Data Scientist",
        description: "Analyze data and build predictive models",
        skills: ["Python", "Machine Learning", "Statistics"],
        match: 92
    },
    {
        name: "AI/ML Engineer",
        description: "Develop artificial intelligence systems",
        skills: ["Deep Learning", "TensorFlow", "NLP"],
        match: 90
    },
    {
        name: "Cybersecurity Analyst",
        description: "Protect systems from security threats",
        skills: ["Network Security", "Penetration Testing"],
        match: 75
    }
];

function calculateTraits(answers) {
    return {
        openness: answers.slice(0, 10).reduce((a, b) => a + b, 0) / 10 * 20,
        conscientiousness: answers.slice(10, 20).reduce((a, b) => a + b, 0) / 10 * 20,
        extraversion: answers.slice(20, 30).reduce((a, b) => a + b, 0) / 10 * 20,
        agreeableness: answers.slice(30, 40).reduce((a, b) => a + b, 0) / 10 * 20,
        neuroticism: answers.slice(40, 50).reduce((a, b) => a + b, 0) / 10 * 20
    };
}

function getRecommendedCareers(traits) {
    const recommended = [];
    
    if (traits.openness > 60 && traits.conscientiousness > 60) {
        recommended.push(careersData[2]);
    }
    if (traits.conscientiousness > 50) {
        recommended.push(careersData[0]);
    }
    if (traits.openness > 50) {
        recommended.push(careersData[1]);
    }
    if (traits.neuroticism > 50 && traits.conscientiousness > 40) {
        recommended.push(careersData[3]);
    }
    
    return recommended.length > 0 ? recommended.slice(0, 3) : careersData.slice(0, 3);
}

function animateTraitBars(traits) {
    setTimeout(() => {
        document.getElementById('opennessBar').style.width = traits.openness + '%';
        document.getElementById('opennessValue').textContent = Math.round(traits.openness) + '%';
        
        document.getElementById('conscientiousnessBar').style.width = traits.conscientiousness + '%';
        document.getElementById('conscientiousnessValue').textContent = Math.round(traits.conscientiousness) + '%';
        
        document.getElementById('extraversionBar').style.width = traits.extraversion + '%';
        document.getElementById('extraversionValue').textContent = Math.round(traits.extraversion) + '%';
        
        document.getElementById('agreeablenessBar').style.width = traits.agreeableness + '%';
        document.getElementById('agreeablenessValue').textContent = Math.round(traits.agreeableness) + '%';
        
        document.getElementById('neuroticismBar').style.width = traits.neuroticism + '%';
        document.getElementById('neuroticismValue').textContent = Math.round(traits.neuroticism) + '%';
    }, 300);
}

function displayCareers(careers) {
    const grid = document.getElementById('careersGrid');
    grid.innerHTML = careers.map(career => `
        <div class="career-card">
            <h4>${career.name}</h4>
            <p>${career.description}</p>
            <div class="skill-list">
                ${career.skills.map(skill => `<span class="skill-tag">${skill}</span>`).join('')}
            </div>
            <span class="match-badge">${career.match}% Match</span>
        </div>
    `).join('');
}

function displaySimilarUsers(users) {
    const grid = document.getElementById('usersGrid');
    grid.innerHTML = users.map(user => `
        <div class="user-card">
            <div class="user-avatar">${user.initials || (user.name || 'U').charAt(0).toUpperCase()}</div>
            <div class="user-info">
                <h4>${user.name}</h4>
                <p>${user.goal || 'No goal set'}</p>
            </div>
        </div>
    `).join('');
}

function showResults(traits, careers = null, similarUsersList = null) {
    document.getElementById('loading').style.display = 'none';
    document.getElementById('resultsContent').style.display = 'block';
    
    animateTraitBars(traits);
    
    const recommendedCareers = careers || getRecommendedCareers(traits);
    displayCareers(recommendedCareers);
    
    if (similarUsersList && similarUsersList.length > 0) {
        displaySimilarUsers(similarUsersList);
    } else {
        document.getElementById('usersGrid').innerHTML = '<p style="color: var(--text-secondary); text-align: center; padding: 2rem;">Be the first to take the quiz! More users will appear here once they complete it.</p>';
    }
}

document.addEventListener('DOMContentLoaded', async () => {
    const answers = JSON.parse(localStorage.getItem('answers'));
    
    if (!answers) {
        window.location.href = 'quiz-FIXED.html';
        return;
    }
    
    const traits = calculateTraits(answers);
    localStorage.setItem('personality_traits', JSON.stringify(traits));
    
    const user = JSON.parse(localStorage.getItem('user'));
    
    let savedTraits = traits;
    
    if (user && user.email) {
        try {
            const saveResponse = await fetch('/api/personality/save', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    email: user.email,
                    traits: traits,
                    answers: answers
                })
            });
            
            if (saveResponse.ok) {
                const saveData = await saveResponse.json();
                savedTraits = saveData.traits || traits;
                console.log('Personality saved:', saveData);
            } else {
                console.error('Failed to save personality:', await saveResponse.text());
            }
        } catch (err) {
            console.error('Error saving personality:', err);
        }
    }
    
    const [careerResult, similarResult] = await Promise.all([
        fetch('/api/recommendations/careers', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(savedTraits)
        }).then(res => res.json()).catch(() => ({ careers: null })),
        user && user.email ? 
            fetch(`/api/recommendations/users/${encodeURIComponent(user.email)}`)
                .then(res => {
                    if (!res.ok) throw new Error('Failed to fetch similar users');
                    return res.json();
                }).catch(err => {
                    console.error('Similar users error:', err);
                    return { similar_users: [] };
                })
            : Promise.resolve({ similar_users: [] })
    ]);
    
    showResults(savedTraits, careerResult.careers, similarResult.similar_users);
    
    document.getElementById('loading').style.display = 'none';
});
