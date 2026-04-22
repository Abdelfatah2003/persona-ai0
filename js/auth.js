function switchTab(tab) {
    const loginTab = document.getElementById('loginTab');
    const registerTab = document.getElementById('registerTab');
    const loginSection = document.getElementById('loginSection');
    const registerSection = document.getElementById('registerSection');
    
    if (tab === 'login') {
        loginTab.classList.add('active');
        registerTab.classList.remove('active');
        loginSection.classList.add('active');
        registerSection.classList.remove('active');
    } else {
        loginTab.classList.remove('active');
        registerTab.classList.add('active');
        loginSection.classList.remove('active');
        registerSection.classList.add('active');
    }
}

async function handleLogin(event) {
    event.preventDefault();
    
    const email = document.getElementById('loginEmail').value;
    const password = document.getElementById('loginPassword').value;
    
    const user = {
        email: email,
        password: password
    };
    
    try {
        const response = await fetch('http://localhost:5000/api/auth/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(user)
        });
        
        if (response.ok) {
            const data = await response.json();
            localStorage.setItem('user', JSON.stringify(data.user));
            localStorage.removeItem('quizCompleted');
            
            // Check if user has already taken the quiz by checking backend
            const personalityResponse = await fetch(`http://localhost:5000/api/personality/get/${encodeURIComponent(email)}`);
            if (personalityResponse.ok) {
                const personalityData = await personalityResponse.json();
                if (personalityData.openness !== undefined) {
                    // User has completed quiz before - go to profile
                    localStorage.setItem('personality_traits', JSON.stringify({
                        openness: personalityData.openness,
                        conscientiousness: personalityData.conscientiousness,
                        extraversion: personalityData.extraversion,
                        agreeableness: personalityData.agreeableness,
                        neuroticism: personalityData.neuroticism
                    }));
                    window.location.href = 'profile.html';
                } else {
                    window.location.href = 'quiz-FIXED.html';
                }
            } else {
                window.location.href = 'quiz-FIXED.html';
            }
        } else {
            alert('Invalid credentials');
        }
    } catch (error) {
        localStorage.setItem('user', JSON.stringify({ email: email, name: 'User' }));
        localStorage.removeItem('quizCompleted');
        window.location.href = 'quiz-FIXED.html';
    }
}

async function handleRegister(event) {
    event.preventDefault();
    
    const firstName = document.getElementById('firstName').value;
    const lastName = document.getElementById('lastName').value;
    const email = document.getElementById('registerEmail').value;
    const age = document.getElementById('age').value;
    const goal = document.getElementById('goal').value;
    const password = document.getElementById('registerPassword').value;
    
    const user = {
        name: `${firstName} ${lastName}`,
        email: email,
        age: parseInt(age),
        goal: goal,
        password: password
    };
    
    try {
        const response = await fetch('http://localhost:5000/api/auth/register', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(user)
        });
        
        if (response.ok) {
            const data = await response.json();
            localStorage.setItem('user', JSON.stringify(data.user));
            localStorage.removeItem('quizCompleted');
            
            // New users should take the quiz
            window.location.href = 'quiz-FIXED.html';
        } else {
            alert('Registration failed');
        }
    } catch (error) {
        localStorage.setItem('user', JSON.stringify({ name: `${firstName} ${lastName}`, email: email, goal: goal }));
        localStorage.removeItem('quizCompleted');
        window.location.href = 'quiz-FIXED.html';
    }
}
