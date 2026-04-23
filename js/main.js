document.addEventListener('DOMContentLoaded', () => {
    initScrollEffects();
    initAuthState();
    updateActiveNavLink();
});

function initAuthState() {
    const user = JSON.parse(localStorage.getItem('user') || '{}');
    const navAuth = document.getElementById('navAuth');
    const navUser = document.getElementById('navUser');
    const userName = document.getElementById('userName');
    const userAvatar = document.getElementById('userAvatar');
    
    if (user && user.email) {
        if (navAuth) navAuth.style.display = 'none';
        if (navUser) navUser.style.display = 'flex';
        if (userName) userName.textContent = user.name ? user.name.split(' ')[0] : user.email.split('@')[0];
        if (userAvatar) userAvatar.textContent = (user.name || user.email).charAt(0).toUpperCase();
    } else {
        if (navAuth) navAuth.style.display = 'flex';
        if (navUser) navUser.style.display = 'none';
    }
}

function handleStartTest() {
    const user = JSON.parse(localStorage.getItem('user') || '{}');
    
    if (user && user.email) {
        const traits = localStorage.getItem('personality_traits');
        if (traits) {
            window.location.href = 'profile.html';
        } else {
            window.location.href = 'quiz-FIXED.html';
        }
    } else {
        window.location.href = 'login.html';
    }
}

function toggleMobileMenu() {
    const navMenu = document.getElementById('navMenu');
    if (navMenu) {
        navMenu.classList.toggle('active');
    }
}

function handleLogout() {
    if (confirm('Are you sure you want to logout?')) {
        localStorage.clear();
        window.location.href = 'index.html';
    }
}

function updateActiveNavLink() {
    const currentPage = window.location.pathname.split('/').pop() || 'index.html';
    document.querySelectorAll('.nav-link').forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('href') === currentPage) {
            link.classList.add('active');
        }
    });
}

function initScrollEffects() {
    const navbar = document.querySelector('.navbar');
    if (!navbar) return;
    
    window.addEventListener('scroll', () => {
        const currentScroll = window.pageYOffset;
        
        if (currentScroll > 50) {
            navbar.style.background = 'rgba(15, 23, 42, 0.95)';
        } else {
            navbar.style.background = 'rgba(15, 23, 42, 0.8)';
        }
    });
}

window.handleStartTest = handleStartTest;
window.toggleMobileMenu = toggleMobileMenu;
window.handleLogout = handleLogout;