// ============================================================================
// AI Personality Test - Complete Rewrite
// ============================================================================

// State variables
let currentQuestion = 0;
let answers = new Array(50).fill(null);
let questions = [];

// Questions data
const questionsData = {
    en: [
        { text: "I enjoy trying new ideas.", category: "openness" },
        { text: "I like learning unfamiliar topics.", category: "openness" },
        { text: "I have a broad imagination.", category: "openness" },
        { text: "I enjoy art and creativity.", category: "openness" },
        { text: "I always look for new ways to solve problems.", category: "openness" },
        { text: "I appreciate beauty in nature and art.", category: "openness" },
        { text: "I enjoy philosophical discussions.", category: "openness" },
        { text: "I like to explore different cultures.", category: "openness" },
        { text: "I am open to unusual ideas.", category: "openness" },
        { text: "I enjoy daydreaming.", category: "openness" },
        { text: "I plan my tasks in advance.", category: "conscientiousness" },
        { text: "I meet deadlines.", category: "conscientiousness" },
        { text: "I like organization.", category: "conscientiousness" },
        { text: "I am a systematic person.", category: "conscientiousness" },
        { text: "I pay attention to details.", category: "conscientiousness" },
        { text: "I set goals and work towards them.", category: "conscientiousness" },
        { text: "I am reliable and dependable.", category: "conscientiousness" },
        { text: "I prefer structured routines.", category: "conscientiousness" },
        { text: "I am self-disciplined.", category: "conscientiousness" },
        { text: "I dislike procrastination.", category: "conscientiousness" },
        { text: "I enjoy talking to people.", category: "extraversion" },
        { text: "I feel energetic around others.", category: "extraversion" },
        { text: "I like social gatherings.", category: "extraversion" },
        { text: "I am outgoing and friendly.", category: "extraversion" },
        { text: "I enjoy being the center of attention.", category: "extraversion" },
        { text: "I start conversations easily.", category: "extraversion" },
        { text: "I prefer working in teams.", category: "extraversion" },
        { text: "I make friends easily.", category: "extraversion" },
        { text: "I enjoy meeting new people.", category: "extraversion" },
        { text: "I like adventure and excitement.", category: "extraversion" },
        { text: "I like helping others.", category: "agreeableness" },
        { text: "I am trustful of others.", category: "agreeableness" },
        { text: "I am considerate and kind.", category: "agreeableness" },
        { text: "I am willing to compromise.", category: "agreeableness" },
        { text: "I care about others' well-being.", category: "agreeableness" },
        { text: "I am sympathetic and empathetic.", category: "agreeableness" },
        { text: "I believe the best in people.", category: "agreeableness" },
        { text: "I enjoy cooperating with others.", category: "agreeableness" },
        { text: "I am forgiving.", category: "agreeableness" },
        { text: "I value social harmony.", category: "agreeableness" },
        { text: "I feel anxious sometimes.", category: "neuroticism" },
        { text: "I worry about things.", category: "neuroticism" },
        { text: "I get upset easily.", category: "neuroticism" },
        { text: "I have frequent mood swings.", category: "neuroticism" },
        { text: "I feel sad or depressed sometimes.", category: "neuroticism" },
        { text: "I am emotionally unstable.", category: "neuroticism" },
        { text: "I tend to overthink.", category: "neuroticism" },
        { text: "I am sensitive to criticism.", category: "neuroticism" },
        { text: "I feel insecure at times.", category: "neuroticism" },
        { text: "I have difficulty relaxing.", category: "neuroticism" }
    ],
    ar: [
        { text: "أستمتع بتجربة أفكار جديدة.", category: "openness" },
        { text: "أحب تعلم مواضيع غير مألوفة.", category: "openness" },
        { text: "لدي خيال واسع.", category: "openness" },
        { text: "أستمتع بالفن والإبداع.", category: "openness" },
        { text: "أبحث دائمًا عن طرق جديدة لحل المشكلات.", category: "openness" },
        { text: "أقدر الجمال في الطبيعة والفن.", category: "openness" },
        { text: "أستمتع بالمناقشات الفلسفية.", category: "openness" },
        { text: "أحب استكشاف ثقافات مختلفة.", category: "openness" },
        { text: "أنا منفتح على الأفكار غير العادية.", category: "openness" },
        { text: "أستمتع بالأحلام اليقظة.", category: "openness" },
        { text: "أخطط لمهاماتي مسبقًا.", category: "conscientiousness" },
        { text: "ألتزم بالمواعيد النهائية.", category: "conscientiousness" },
        { text: "أحب التنظيم.", category: "conscientiousness" },
        { text: "أنا شخص منظم.", category: "conscientiousness" },
        { text: "أهتم بالتفاصيل.", category: "conscientiousness" },
        { text: "أضع أهدافًا وأعمل على تحقيقها.", category: "conscientiousness" },
        { text: "أنا موثوق.", category: "conscientiousness" },
        { text: "أفضل الروتين المنظم.", category: "conscientiousness" },
        { text: "أنا منضبط ذاتيًا.", category: "conscientiousness" },
        { text: "أكره التسويف.", category: "conscientiousness" },
        { text: "أستمتع بالتحدث مع الناس.", category: "extraversion" },
        { text: "أشعر بالحيوية حول الآخرين.", category: "extraversion" },
        { text: "أحب التجمعات الاجتماعية.", category: "extraversion" },
        { text: "أنا منطلق وودود.", category: "extraversion" },
        { text: "أستمتع being in center of attention.", category: "extraversion" },
        { text: "أبدأ المحادثات بسهولة.", category: "extraversion" },
        { text: "أفضل العمل في فرق.", category: "extraversion" },
        { text: "أصنع الأصدقاء بسهولة.", category: "extraversion" },
        { text: "أستمتع بمقابلة أشخاص جدد.", category: "extraversion" },
        { text: "أحب المغامرة والإثارة.", category: "extraversion" },
        { text: "أحب مساعدة الآخرين.", category: "agreeableness" },
        { text: "أنا واثق بالآخرين.", category: "agreeableness" },
        { text: "أنا مهتم ولطيف.", category: "agreeableness" },
        { text: "أنا مستعد للتسوية.", category: "agreeableness" },
        { text: "أهتم برفاهية الآخرين.", category: "agreeableness" },
        { text: "أنا متعاطف.", category: "agreeableness" },
        { text: "أؤمن بأفضل ما في الناس.", category: "agreeableness" },
        { text: "أستمتع بالتعاون مع الآخرين.", category: "agreeableness" },
        { text: "أنا متسامح.", category: "agreeableness" },
        { text: "أقدر الانسجام الاجتماعي.", category: "agreeableness" },
        { text: "أشعر بالقلق أحيانًا.", category: "neuroticism" },
        { text: "أقلق بشأن الأشياء.", category: "neuroticism" },
        { text: "أغضب بسهولة.", category: "neuroticism" },
        { text: "أعاني من تقلبات مزاجية متكررة.", category: "neuroticism" },
        { text: "أشعر بالحزن أو الاكتئاب أحيانًا.", category: "neuroticism" },
        { text: "أنا غير مستقر عاطفيًا.", category: "neuroticism" },
        { text: "أميل إلى التفكير المفرط.", category: "neuroticism" },
        { text: "أنا حساس للنقد.", category: "neuroticism" },
        { text: "أشعر بعدم الأمان أحيانًا.", category: "neuroticism" },
        { text: "أصعب علي الاسترخاء.", category: "neuroticism" }
    ]
};

// ============================================================================
// Core Functions
// ============================================================================

function loadQuestions() {
    console.log('[TEST] Loading questions...');
    
    const lang = localStorage.getItem('lang') || 'en';
    questions = questionsData[lang];
    
    console.log('[TEST] Language:', lang);
    console.log('[TEST] Questions loaded:', questions.length);
    
    updateQuestion();
    setupEventListeners();
}

function setupEventListeners() {
    console.log('[TEST] Setting up event listeners...');
    
    const optionButtons = document.querySelectorAll('.option-btn');
    console.log('[TEST] Found option buttons:', optionButtons.length);
    
    optionButtons.forEach((btn, index) => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            const value = parseInt(this.getAttribute('data-value'));
            selectAnswer(value);
        });
        console.log('[TEST] Attached listener to button', index + 1);
    });
    
    // Next button
    const nextBtn = document.getElementById('nextBtn');
    if (nextBtn) {
        nextBtn.onclick = function() {
            goToNextQuestion();
        };
        console.log('[TEST] Next button configured');
    }
    
    // Previous button
    const prevBtn = document.getElementById('prevBtn');
    if (prevBtn) {
        prevBtn.onclick = function() {
            goToPrevQuestion();
        };
        console.log('[TEST] Previous button configured');
    }
}

function updateQuestion() {
    console.log('[TEST] Updating question:', currentQuestion);
    
    const questionText = document.getElementById('questionText');
    const questionNumber = document.getElementById('questionNumber');
    const progressFill = document.getElementById('progressFill');
    const prevBtn = document.getElementById('prevBtn');
    
    if (!questionText || !questionNumber || !progressFill) {
        console.error('[TEST] Required elements not found!');
        return;
    }
    
    questionText.textContent = questions[currentQuestion].text;
    questionNumber.textContent = `Question ${currentQuestion + 1} / ${questions.length}`;
    progressFill.style.width = `${((currentQuestion + 1) / questions.length) * 100}%`;
    
    if (prevBtn) {
        prevBtn.style.visibility = currentQuestion === 0 ? 'hidden' : 'visible';
    }
    
    updateOptionsDisplay();
}

function updateOptionsDisplay() {
    const options = document.querySelectorAll('.option-btn');
    
    options.forEach(btn => {
        btn.classList.remove('selected');
        
        const value = parseInt(btn.getAttribute('data-value'));
        if (answers[currentQuestion] === value) {
            btn.classList.add('selected');
        }
    });
}

function selectAnswer(value) {
    console.log('[TEST] Selected answer:', value);
    
    answers[currentQuestion] = value;
    updateOptionsDisplay();
    
    // Visual feedback
    const options = document.querySelectorAll('.option-btn');
    options.forEach(btn => {
        const btnValue = parseInt(btn.getAttribute('data-value'));
        if (btnValue === value) {
            btn.style.background = 'linear-gradient(135deg, #6366f1 0%, #ec4899 100%)';
            btn.style.color = 'white';
            btn.style.borderColor = 'transparent';
        } else {
            btn.style.background = 'rgba(255, 255, 255, 0.05)';
            btn.style.color = '#94a3b8';
            btn.style.borderColor = 'rgba(255, 255, 255, 0.1)';
        }
    });
}

function goToNextQuestion() {
    console.log('[TEST] Next question, current:', currentQuestion);
    
    if (answers[currentQuestion] === null) {
        alert('Please select an answer before continuing.');
        return;
    }
    
    if (currentQuestion < questions.length - 1) {
        currentQuestion++;
        updateQuestion();
    } else {
        submitTest();
    }
}

function goToPrevQuestion() {
    console.log('[TEST] Previous question, current:', currentQuestion);
    
    if (currentQuestion > 0) {
        currentQuestion--;
        updateQuestion();
    }
}

function submitTest() {
    console.log('[TEST] Submitting test...');
    console.log('[TEST] Answers:', answers);
    
    localStorage.setItem('answers', JSON.stringify(answers));
    
    console.log('[TEST] Redirecting to results...');
    window.location.href = 'results.html';
}

// ============================================================================
// Initialize on Page Load
// ============================================================================

document.addEventListener('DOMContentLoaded', function() {
    console.log('[TEST] Page loaded, initializing...');
    
    try {
        loadQuestions();
        console.log('[TEST] Initialization complete');
    } catch (error) {
        console.error('[TEST] Error during initialization:', error);
        alert('Error loading test. Please refresh the page.');
    }
});
