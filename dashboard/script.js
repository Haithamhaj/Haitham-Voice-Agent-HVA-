// Service Details Data
const serviceData = {
    memory: {
        title: 'نظام الذاكرة المتقدم',
        titleEn: 'Advanced Memory System',
        description: 'نظام ذكي لحفظ واسترجاع الملاحظات والأفكار والقرارات مع بحث دلالي متقدم وتصنيف تلقائي',
        descriptionEn: 'Intelligent system for saving and retrieving notes, ideas, and decisions with advanced semantic search and automatic classification',
        features: [
            '✅ تخزين محلي آمن (SQLite)',
            '✅ بحث دلالي ذكي (Vector Search)',
            '✅ تصنيف تلقائي (أفكار، قرارات، مهام، ملاحظات)',
            '✅ استخراج تلقائي للمهام والقرارات',
            '✅ مزامنة اختيارية مع Google Sheets'
        ],
        featuresEn: [
            '✅ Secure local storage (SQLite)',
            '✅ Smart semantic search (Vector Search)',
            '✅ Automatic classification (ideas, decisions, tasks, notes)',
            '✅ Automatic extraction of tasks and decisions',
            '✅ Optional sync with Google Sheets'
        ],
        commands: [
            'احفظ ملاحظة: اجتماع المشروع غداً الساعة 3',
            'سجل فكرة: استخدام الذكاء الاصطناعي في التعليم',
            'ايش آخر الملاحظات؟',
            'ابحث في الملاحظات عن اجتماعات',
            'احفظ قرار: استخدام React للمشروع الجديد'
        ],
        commandsEn: [
            'Save note: Project meeting tomorrow at 3 PM',
            'Record idea: AI in education',
            'What are my recent notes?',
            'Search notes about meetings',
            'Save decision: Use React for new project'
        ]
    },
    gmail: {
        title: 'تكامل Gmail',
        titleEn: 'Gmail Integration',
        description: 'إدارة كاملة للبريد الإلكتروني بالصوت مع تلخيص ذكي واستخراج المهام',
        descriptionEn: 'Complete email management by voice with smart summarization and task extraction',
        features: [
            '✅ قراءة الرسائل والمحادثات',
            '✅ إنشاء مسودات (لا يرسل تلقائياً)',
            '✅ تلخيص ذكي للرسائل',
            '✅ استخراج المهام من الإيميلات',
            '✅ تصنيف تلقائي',
            '✅ مصادقة آمنة (OAuth)'
        ],
        featuresEn: [
            '✅ Read messages and threads',
            '✅ Create drafts (no auto-send)',
            '✅ Smart email summarization',
            '✅ Extract tasks from emails',
            '✅ Automatic categorization',
            '✅ Secure authentication (OAuth)'
        ],
        commands: [
            'اقرأ آخر إيميل',
            'لخص آخر 5 إيميلات',
            'اكتب مسودة إيميل لأحمد عن الاجتماع',
            'ابحث في الإيميلات عن فواتير',
            'استخرج المهام من آخر إيميل'
        ],
        commandsEn: [
            'Read latest email',
            'Summarize last 5 emails',
            'Draft email to John about the meeting',
            'Search emails for invoices',
            'Extract tasks from latest email'
        ]
    },
    files: {
        title: 'إدارة الملفات',
        titleEn: 'File Management',
        description: 'التحكم الكامل في ملفاتك ومجلداتك بالأوامر الصوتية',
        descriptionEn: 'Complete control of your files and folders with voice commands',
        features: [
            '✅ عرض محتويات المجلدات',
            '✅ البحث المتقدم عن الملفات',
            '✅ فتح المجلدات في Finder',
            '✅ إنشاء مجلدات جديدة',
            '✅ نقل ونسخ الملفات',
            '✅ إعادة تسمية الملفات',
            '✅ ترتيب الملفات'
        ],
        featuresEn: [
            '✅ List folder contents',
            '✅ Advanced file search',
            '✅ Open folders in Finder',
            '✅ Create new folders',
            '✅ Move and copy files',
            '✅ Rename files',
            '✅ Sort files'
        ],
        commands: [
            'اعرض الملفات في مجلد Downloads',
            'ابحث عن ملفات PDF في المستندات',
            'افتح مجلد المشاريع',
            'أنشئ مجلد جديد اسمه AI-Project',
            'انقل الملف إلى مجلد Documents',
            'رتب الملفات حسب التاريخ'
        ],
        commandsEn: [
            'List files in Downloads',
            'Search for PDF files in Documents',
            'Open Projects folder',
            'Create folder named AI-Project',
            'Move file to Documents',
            'Sort files by date'
        ]
    },
    docs: {
        title: 'معالجة المستندات',
        titleEn: 'Document Processing',
        description: 'قراءة وتحليل وترجمة المستندات بقوة Gemini AI',
        descriptionEn: 'Read, analyze, and translate documents with Gemini AI power',
        features: [
            '✅ قراءة ملفات PDF',
            '✅ تلخيص ذكي للمستندات',
            '✅ ترجمة متعددة اللغات',
            '✅ مقارنة المستندات',
            '✅ استخراج المهام والنقاط المهمة'
        ],
        featuresEn: [
            '✅ Read PDF files',
            '✅ Smart document summarization',
            '✅ Multi-language translation',
            '✅ Document comparison',
            '✅ Extract tasks and key points'
        ],
        commands: [
            'لخص هذا الملف PDF',
            'ترجم هذا المستند للإنجليزية',
            'قارن بين هذين الملفين',
            'استخرج المهام من هذا المستند',
            'اقرأ محتوى الملف'
        ],
        commandsEn: [
            'Summarize this PDF file',
            'Translate this document to English',
            'Compare these two files',
            'Extract tasks from this document',
            'Read file content'
        ]
    },
    tasks: {
        title: 'إدارة المهام',
        titleEn: 'Task Management',
        description: 'تنظيم وتتبع مهامك اليومية بسهولة وفعالية',
        descriptionEn: 'Organize and track your daily tasks easily and effectively',
        features: [
            '✅ إضافة مهام سريعة بالصوت',
            '✅ تتبع حالة المهام',
            '✅ تحديد الأولويات',
            '✅ تذكير بالمهام',
            '✅ تصنيف حسب المشاريع'
        ],
        featuresEn: [
            '✅ Quick voice task addition',
            '✅ Task status tracking',
            '✅ Priority setting',
            '✅ Task reminders',
            '✅ Project-based categorization'
        ],
        commands: [
            'أضف مهمة: مراجعة الكود',
            'اعرض مهامي',
            'أكمل مهمة رقم 3',
            'احذف المهمة الأولى',
            'ايش المهام المهمة اليوم؟'
        ],
        commandsEn: [
            'Add task: Review code',
            'Show my tasks',
            'Complete task number 3',
            'Delete first task',
            'What are today\'s important tasks?'
        ]
    },
    browser: {
        title: 'أدوات المتصفح',
        titleEn: 'Browser Tools',
        description: 'فتح المواقع والبحث في الإنترنت بسهولة',
        descriptionEn: 'Open websites and search the internet easily',
        features: [
            '✅ فتح المواقع مباشرة',
            '✅ البحث في Google',
            '✅ التنقل السريع',
            '✅ فتح روابط متعددة'
        ],
        featuresEn: [
            '✅ Open websites directly',
            '✅ Google search',
            '✅ Quick navigation',
            '✅ Open multiple links'
        ],
        commands: [
            'افتح موقع google.com',
            'ابحث في Google عن Python tutorials',
            'افتح YouTube',
            'ابحث عن أخبار الذكاء الاصطناعي'
        ],
        commandsEn: [
            'Open google.com',
            'Search Google for AI news',
            'Open YouTube',
            'Search for machine learning tutorials'
        ]
    },
    system: {
        title: 'أدوات النظام',
        titleEn: 'System Tools',
        description: 'التحكم في تطبيقات macOS بالأوامر الصوتية',
        descriptionEn: 'Control macOS applications with voice commands',
        features: [
            '✅ فتح التطبيقات',
            '✅ عرض معلومات النظام',
            '✅ التحكم بالصوت',
            '✅ آمن ومحمي'
        ],
        featuresEn: [
            '✅ Open applications',
            '✅ Show system info',
            '✅ Volume control',
            '✅ Safe and secure'
        ],
        commands: [
            'افتح تطبيق Safari',
            'افتح Chrome',
            'اعرض معلومات النظام',
            'افتح Finder'
        ],
        commandsEn: [
            'Open Safari app',
            'Open Chrome',
            'Show system info',
            'Open Finder'
        ]
    },
    terminal: {
        title: 'الطرفية الآمنة',
        titleEn: 'Safe Terminal',
        description: 'تنفيذ أوامر Terminal الآمنة فقط بدون مخاطر',
        descriptionEn: 'Execute only safe Terminal commands without risks',
        features: [
            '✅ أوامر آمنة فقط',
            '✅ بدون sudo',
            '✅ محمي من الأوامر المدمرة',
            '✅ قائمة بيضاء للأوامر'
        ],
        featuresEn: [
            '✅ Safe commands only',
            '✅ No sudo',
            '✅ Protected from destructive commands',
            '✅ Command whitelist'
        ],
        commands: [
            'ls - عرض الملفات',
            'pwd - عرض المسار الحالي',
            'echo - طباعة نص',
            'whoami - عرض اسم المستخدم',
            'df - عرض مساحة القرص',
            'date - عرض التاريخ'
        ],
        commandsEn: [
            'ls - list files',
            'pwd - print working directory',
            'echo - print text',
            'whoami - show username',
            'df - disk space',
            'date - show date'
        ]
    },
    voice: {
        title: 'نظام الصوت',
        titleEn: 'Voice System',
        description: 'تحويل متقدم بين الكلام والنص بدقة عالية ودعم كامل للعربية',
        descriptionEn: 'Advanced speech-to-text conversion with high accuracy and full Arabic support',
        features: [
            '✅ دقة 90-95% للأوامر القصيرة (Google Cloud STT)',
            '✅ دقة 75-85% للجلسات الطويلة (Whisper large-v3)',
            '✅ دعم كامل للعربية (ar-SA) والإنجليزية (en-US)',
            '✅ كشف تلقائي للغة',
            '✅ توفير ~60% من التكلفة',
            '✅ أصوات عربية طبيعية (Majed)'
        ],
        featuresEn: [
            '✅ 90-95% accuracy for short commands (Google Cloud STT)',
            '✅ 75-85% accuracy for long sessions (Whisper large-v3)',
            '✅ Full Arabic (ar-SA) and English (en-US) support',
            '✅ Automatic language detection',
            '✅ ~60% cost savings',
            '✅ Natural Arabic voices (Majed)'
        ],
        commands: [
            'استراتيجية هجينة ذكية:',
            '• Google Cloud STT للأوامر القصيرة',
            '• Whisper large-v3 للجلسات الطويلة',
            '• كشف تلقائي للغة المستخدمة',
            '• استجابة صوتية باللغة المناسبة'
        ],
        commandsEn: [
            'Smart hybrid strategy:',
            '• Google Cloud STT for short commands',
            '• Whisper large-v3 for long sessions',
            '• Automatic language detection',
            '• Voice response in appropriate language'
        ]
    }
};

// Current language
let currentLang = 'ar';

// Show service details in modal
function showServiceDetails(serviceId) {
    const service = serviceData[serviceId];
    const modal = document.getElementById('serviceModal');
    const modalBody = document.getElementById('modalBody');

    const isArabic = currentLang === 'ar';
    const title = isArabic ? service.title : service.titleEn;
    const description = isArabic ? service.description : service.descriptionEn;
    const features = isArabic ? service.features : service.featuresEn;
    const commands = isArabic ? service.commands : service.commandsEn;

    let html = `
        <h2 class="text-gradient mb-3" style="font-size: 32px; font-weight: 700;">${title}</h2>
        <p class="mb-4" style="font-size: 18px; color: var(--text-secondary);">${description}</p>
        
        <h3 class="mb-2" style="font-size: 24px; font-weight: 600;">${isArabic ? 'المميزات:' : 'Features:'}</h3>
        <div class="mb-4">
            ${features.map(f => `<p style="margin: 8px 0; font-size: 16px; color: var(--text-secondary);">${f}</p>`).join('')}
        </div>
        
        <h3 class="mb-2" style="font-size: 24px; font-weight: 600;">${isArabic ? 'أمثلة الأوامر:' : 'Command Examples:'}</h3>
        <div>
            ${commands.map(cmd => `<div class="command-example" onclick="copyCommand(this)">${cmd}</div>`).join('')}
        </div>
        
        <p class="mt-3" style="font-size: 14px; color: var(--text-tertiary); text-align: center;">
            ${isArabic ? '💡 انقر على أي أمر لنسخه' : '💡 Click any command to copy it'}
        </p>
    `;

    modalBody.innerHTML = html;
    modal.classList.add('active');
}

// Close modal
function closeModal() {
    const modal = document.getElementById('serviceModal');
    modal.classList.remove('active');
}

// Copy command to clipboard
function copyCommand(element) {
    const text = element.textContent;
    navigator.clipboard.writeText(text).then(() => {
        // Visual feedback
        const originalBg = element.style.background;
        element.style.background = 'rgba(79, 172, 254, 0.3)';

        // Show toast notification
        showToast(currentLang === 'ar' ? 'تم النسخ! ✓' : 'Copied! ✓');

        setTimeout(() => {
            element.style.background = originalBg;
        }, 300);
    });
}

// Show toast notification
function showToast(message) {
    const toast = document.createElement('div');
    toast.textContent = message;
    toast.style.cssText = `
        position: fixed;
        bottom: 30px;
        ${currentLang === 'ar' ? 'right' : 'left'}: 50%;
        transform: translateX(${currentLang === 'ar' ? '50%' : '-50%'});
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        color: white;
        padding: 16px 32px;
        border-radius: 50px;
        font-weight: 600;
        font-size: 16px;
        box-shadow: 0 8px 32px rgba(79, 172, 254, 0.4);
        z-index: 10000;
        animation: slideUp 0.3s ease-out;
    `;

    document.body.appendChild(toast);

    setTimeout(() => {
        toast.style.animation = 'fadeOut 0.3s ease-out';
        setTimeout(() => toast.remove(), 300);
    }, 2000);
}

// Toggle language
function toggleLanguage() {
    currentLang = currentLang === 'ar' ? 'en' : 'ar';
    const html = document.documentElement;
    const langText = document.getElementById('lang-text');

    if (currentLang === 'en') {
        html.setAttribute('lang', 'en');
        html.setAttribute('dir', 'ltr');
        langText.textContent = 'AR';
        updateContentToEnglish();
    } else {
        html.setAttribute('lang', 'ar');
        html.setAttribute('dir', 'rtl');
        langText.textContent = 'EN';
        updateContentToArabic();
    }
}

// Update content to English
function updateContentToEnglish() {
    document.querySelector('.logo-text h1').textContent = 'Haitham Voice Agent';
    document.querySelector('.logo-text p').textContent = 'Your Smart Voice Assistant';
    document.querySelector('.hero-title').textContent = 'Explore HVA Services';
    document.querySelector('.hero-subtitle').textContent = 'Nine intelligent services at your voice command';
    document.querySelector('.footer p').textContent = 'Made with ❤️ by Haitham | 🎤 Voice-Powered • 🤖 AI-Driven • 🔒 Privacy-First';

    // Update service cards
    const cards = document.querySelectorAll('.service-card');
    const services = ['memory', 'gmail', 'files', 'docs', 'tasks', 'browser', 'system', 'terminal', 'voice'];

    cards.forEach((card, index) => {
        const serviceId = services[index];
        const service = serviceData[serviceId];
        card.querySelector('.service-title').textContent = service.titleEn;
        card.querySelector('.service-description').textContent = service.descriptionEn;
        card.querySelector('.btn-primary span:first-child').textContent = 'Explore Service';
    });
}

// Update content to Arabic
function updateContentToArabic() {
    document.querySelector('.logo-text h1').textContent = 'Haitham Voice Agent';
    document.querySelector('.logo-text p').textContent = 'وكيلك الصوتي الذكي';
    document.querySelector('.hero-title').textContent = 'استكشف خدمات HVA';
    document.querySelector('.hero-subtitle').textContent = 'تسع خدمات ذكية تحت أمرك الصوتي';
    document.querySelector('.footer p').textContent = 'Made with ❤️ by Haitham | 🎤 Voice-Powered • 🤖 AI-Driven • 🔒 Privacy-First';

    // Update service cards
    const cards = document.querySelectorAll('.service-card');
    const services = ['memory', 'gmail', 'files', 'docs', 'tasks', 'browser', 'system', 'terminal', 'voice'];

    cards.forEach((card, index) => {
        const serviceId = services[index];
        const service = serviceData[serviceId];
        card.querySelector('.service-title').textContent = service.title;
        card.querySelector('.service-description').textContent = service.description;
        card.querySelector('.btn-primary span:first-child').textContent = 'استكشف الخدمة';
    });
}

// Close modal on escape key
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        closeModal();
    }
});

// Add stagger animation to service cards
document.addEventListener('DOMContentLoaded', () => {
    const cards = document.querySelectorAll('.service-card');
    cards.forEach((card, index) => {
        card.style.animation = `fadeInUp 0.6s ease-out ${index * 0.1}s both`;
    });
});
