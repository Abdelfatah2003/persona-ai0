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
    
    try {
        const data = await api.login({ email, password });
        
        if (data.success) {
            localStorage.setItem('user', JSON.stringify(data.user));
            localStorage.removeItem('quizCompleted');
            
            const persData = await api.getPersonality(email);
            if (persData && persData.success && persData.personality && persData.personality.traits) {
                localStorage.setItem('personality_traits', JSON.stringify(persData.personality.traits));
                window.location.href = 'profile.html';
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
    
    try {
        const data = await api.register({
            name: `${firstName} ${lastName}`,
            email,
            age: parseInt(age),
            goal,
            password
        });
        
        if (data.success) {
            localStorage.setItem('user', JSON.stringify(data.user));
            localStorage.removeItem('quizCompleted');
            window.location.href = 'quiz-FIXED.html';
        } else {
            alert(data.error || 'Registration failed');
        }
    } catch (error) {
        localStorage.setItem('user', JSON.stringify({ name: `${firstName} ${lastName}`, email, goal }));
        localStorage.removeItem('quizCompleted');
        window.location.href = 'quiz-FIXED.html';
    }
}