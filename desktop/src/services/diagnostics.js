export const diagnoseError = (log) => {
    const message = log.message.toLowerCase();
    const details = log.details ? JSON.stringify(log.details).toLowerCase() : '';
    const fullText = message + ' ' + details;

    // Extract Location (File:Line:Function)
    let location = null;

    // 1. Try to find JS stack trace pattern: at Function (File:Line:Col)
    const jsStackMatch = details.match(/at\s+(.+?)\s+\((.+?):(\d+):(\d+)\)/);
    if (jsStackMatch) {
        location = {
            function: jsStackMatch[1],
            file: jsStackMatch[2].split('/').pop(), // Get filename only
            line: jsStackMatch[3]
        };
    }

    // 2. Try to find Python stack trace pattern: File "...", line X, in Function
    if (!location) {
        const pyStackMatch = details.match(/File\s+"(.+?)",\s+line\s+(\d+),\s+in\s+(.+)/);
        if (pyStackMatch) {
            location = {
                file: pyStackMatch[1].split('/').pop(),
                line: pyStackMatch[2],
                function: pyStackMatch[3]
            };
        }
    }

    // WebSocket Connection Refused / Closed
    if (fullText.includes('1006') || fullText.includes('connection refused') || fullText.includes('failed to connect')) {
        return {
            title: 'فشل الاتصال بالخادم',
            explanation: 'التطبيق غير قادر على الاتصال بالخادم الخلفي (Backend).',
            cause: 'قد يكون الخادم متوقفاً عن العمل، أو هناك برنامج حماية (Firewall) يمنع الاتصال، أو أن المنفذ 8765 مشغول.',
            impact: 'لن تعمل الأوامر الصوتية، المحادثة، أو تحديث البيانات.',
            steps: [
                'تأكد من تشغيل التطبيق كمسؤول (Admin) إذا لزم الأمر.',
                'تحقق من عدم وجود تطبيق آخر يستخدم المنفذ 8765.',
                'أعد تشغيل التطبيق بالكامل.',
                'إذا استمرت المشكلة، تحقق من ملفات السجل (Backend Logs) لمزيد من التفاصيل.'
            ],
            location
        };
    }

    // Fetch Error (API Unreachable)
    if (fullText.includes('fetch') || fullText.includes('network request failed')) {
        return {
            title: 'خطأ في الشبكة',
            explanation: 'فشل التطبيق في جلب البيانات من الخادم.',
            cause: 'الخادم لا يستجيب للطلبات، أو هناك انقطاع في الاتصال المحلي.',
            impact: 'لن تظهر البيانات المحدثة (البريد، التقويم، المهام).',
            steps: [
                'تأكد من أن الخادم يعمل (انظر حالة النظام).',
                'تحقق من اتصال الإنترنت (للخدمات الخارجية).',
                'حاول تحديث الصفحة.'
            ],
            location
        };
    }

    // 500 Internal Server Error
    if (fullText.includes('500') || fullText.includes('internal server error')) {
        return {
            title: 'خطأ داخلي في الخادم',
            explanation: 'حدثت مشكلة غير متوقعة داخل الخادم أثناء معالجة الطلب.',
            cause: 'قد يكون هناك خطأ برمجي في الكود الخلفي، أو بيانات غير صالحة تم إرسالها.',
            impact: 'العملية الحالية لم تكتمل.',
            steps: [
                'حاول تكرار العملية مرة أخرى.',
                'راجع سجلات الخادم (Backend Logs) لمعرفة الخطأ البرمجي الدقيق.',
                'أبلغ المطور عن المشكلة مع إرفاق السجلات.'
            ],
            location
        };
    }

    // Microphone Error
    if (fullText.includes('microphone') || fullText.includes('audio') || fullText.includes('notallowederror')) {
        return {
            title: 'مشكلة في الميكروفون',
            explanation: 'التطبيق لا يستطيع الوصول إلى الميكروفون.',
            cause: 'لم يتم منح الصلاحية، أو الميكروفون غير متصل، أو مستخدم من قبل تطبيق آخر.',
            impact: 'لن تعمل الأوامر الصوتية.',
            steps: [
                'تأكد من منح صلاحية الميكروفون للتطبيق في إعدادات النظام.',
                'تأكد من أن الميكروفون متصل ويعمل.',
                'أغلق التطبيقات الأخرى التي قد تستخدم الميكروفون.'
            ],
            location
        };
    }

    // Default / Unknown
    return {
        title: 'خطأ غير محدد',
        explanation: 'حدث خطأ لم يتم التعرف على سببه بدقة من خلال التحليل التلقائي.',
        cause: 'غير معروف.',
        impact: 'قد يؤثر على وظائف معينة حسب سياق الخطأ.',
        steps: [
            'اقرأ رسالة الخطأ الأصلية بعناية.',
            'حاول إعادة تشغيل التطبيق.',
            'تواصل مع الدعم الفني.'
        ],
        location
    };
};
