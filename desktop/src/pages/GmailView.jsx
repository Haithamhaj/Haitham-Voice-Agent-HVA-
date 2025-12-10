import React, { useState, useEffect } from 'react';
import { Mail, RefreshCw, ExternalLink, Star, Sparkles, CheckCircle, X } from 'lucide-react';
import { api } from '../services/api';

const EmailModal = ({ isOpen, onClose, title, content }) => {
    if (!isOpen) return null;
    return (
        <div className="fixed inset-0 bg-black/60 backdrop-blur-sm z-50 flex items-center justify-center p-4 animate-in fade-in duration-200">
            <div className="bg-hva-card border border-hva-border rounded-xl w-full max-w-2xl shadow-2xl animate-in zoom-in-95 duration-200 flex flex-col max-h-[85vh]">
                <header className="flex items-center justify-between p-4 border-b border-hva-border-subtle shrink-0">
                    <h3 className="font-bold text-hva-cream text-lg truncate pr-4">{title}</h3>
                    <button onClick={onClose} className="p-1 hover:bg-hva-bg rounded-lg text-hva-muted hover:text-white transition-colors">
                        <X size={20} />
                    </button>
                </header>
                <div className="p-6 text-hva-cream overflow-y-auto whitespace-pre-wrap leading-relaxed custom-scrollbar">
                    {content}
                </div>
            </div>
        </div>
    );
};

const GmailView = () => {
    const [emails, setEmails] = useState([]);
    const [loading, setLoading] = useState(true);
    const [modal, setModal] = useState({ isOpen: false, title: "", content: "" });

    const fetchEmails = () => {
        setLoading(true);
        api.fetchEmails()
            .then(data => {
                // Handle different response structures based on API implementation
                const list = Array.isArray(data) ? data : (data.messages || []);
                setEmails(list);
            })
            .catch(err => console.error(err))
            .finally(() => setLoading(false));
    };

    useEffect(() => {
        fetchEmails();
    }, []);

    return (
        <div className="space-y-6">
            <header className="flex items-center justify-between">
                <div>
                    <h1 className="text-3xl font-bold text-hva-cream flex items-center gap-3">
                        <Mail className="text-red-500" size={32} />
                        البريد الإلكتروني
                    </h1>
                    <p className="text-hva-muted mt-1">الرسائل غير المقروءة</p>
                </div>
                <button
                    onClick={fetchEmails}
                    className="p-2 bg-hva-card hover:bg-hva-card-hover rounded-lg text-hva-cream transition-colors"
                >
                    <RefreshCw size={20} className={loading ? "animate-spin" : ""} />
                </button>
            </header>

            <div className="bg-hva-card rounded-2xl border border-hva-border-subtle overflow-hidden">
                {loading ? (
                    <div className="p-8 text-center text-hva-muted">جاري التحميل...</div>
                ) : emails.length > 0 ? (
                    <div className="divide-y divide-hva-border-subtle">
                        {emails.map((email, index) => (
                            <div key={index} className="p-4 hover:bg-hva-card-hover transition-colors cursor-pointer group">
                                <div className="flex items-center justify-between mb-1">
                                    <h3 className="font-bold text-hva-cream group-hover:text-hva-accent transition-colors">
                                        {email.subject || "بدون عنوان"}
                                    </h3>
                                    <div className="flex items-center gap-2">
                                        <span className="text-xs text-hva-dim">{email.date ? new Date(email.date).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) : "الآن"}</span>
                                        <button
                                            onClick={(e) => {
                                                e.stopPropagation();
                                                const btn = e.currentTarget;
                                                btn.classList.add('animate-pulse');
                                                api.summarizeEmail(email.id)
                                                    .then(res => {
                                                        setModal({
                                                            isOpen: true,
                                                            title: "ملخص الذكاء الاصطناعي ✨",
                                                            content: res.summary
                                                        });
                                                    })
                                                    .catch(err => {
                                                        alert("تعذر التلخيص: " + err.message);
                                                    })
                                                    .finally(() => btn.classList.remove('animate-pulse'));
                                            }}
                                            className="p-1 hover:bg-hva-bg rounded opacity-0 group-hover:opacity-100 transition-all text-hva-accent"
                                            title="تلخيص بالذكاء الاصطناعي"
                                        >
                                            <Sparkles size={16} />
                                        </button>
                                        <button
                                            onClick={(e) => {
                                                e.stopPropagation();
                                                const btn = e.currentTarget;
                                                btn.classList.add('animate-pulse');
                                                api.convertEmailToTask(email.id)
                                                    .then(res => {
                                                        const msg = res.title ? `تمت الإضافة: ${res.title}` : "تم تحويل المهمة بنجاح";
                                                        // Alert for task is okay (quick action), but we ensure it works
                                                        alert("✅ " + msg + "\n(قم بتحديث صفحة المهام لرؤيتها)");
                                                    })
                                                    .catch(err => {
                                                        alert("❌ فشل التحويل: " + err.message);
                                                    })
                                                    .finally(() => btn.classList.remove('animate-pulse'));
                                            }}
                                            className="p-1 hover:bg-hva-bg rounded opacity-0 group-hover:opacity-100 transition-all text-green-400"
                                            title="تحويل إلى مهمة"
                                        >
                                            <CheckCircle size={16} />
                                        </button>
                                    </div>
                                </div>
                                <div className="flex items-center justify-between">
                                    <p className="text-sm text-hva-muted truncate max-w-[80%]">
                                        {email.snippet || email.sender || "لا يوجد معاينة"}
                                    </p>
                                    <Star size={16} className="text-hva-dim hover:text-yellow-400 cursor-pointer" />
                                </div>
                            </div>
                        ))}
                    </div>
                ) : (
                    <div className="p-12 text-center flex flex-col items-center text-hva-muted">
                        <Mail size={48} className="mb-4 opacity-20" />
                        <p>لا توجد رسائل جديدة</p>
                    </div>
                )}
            </div>

            <EmailModal
                isOpen={modal.isOpen}
                onClose={() => setModal({ ...modal, isOpen: false })}
                title={modal.title}
                content={modal.content}
            />
        </div>
    );
};

export default GmailView;
