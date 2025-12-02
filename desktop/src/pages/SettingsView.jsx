import React from 'react';
import { Settings, Volume2, Monitor, Shield, Globe } from 'lucide-react';

const SettingsView = () => {
    return (
        <div className="space-y-6">
            <header>
                <h1 className="text-3xl font-bold text-hva-cream flex items-center gap-3">
                    <Settings className="text-hva-dim" size={32} />
                    الإعدادات
                </h1>
                <p className="text-hva-muted mt-1">تخصيص النظام</p>
            </header>

            <div className="space-y-4">
                {/* Section */}
                <div className="bg-hva-card rounded-2xl border border-hva-border-subtle p-6">
                    <h2 className="text-xl font-bold text-hva-cream mb-4 flex items-center gap-2">
                        <Monitor size={20} className="text-hva-accent" />
                        المظهر
                    </h2>
                    <div className="flex items-center justify-between py-2">
                        <span className="text-hva-muted">الوضع الليلي</span>
                        <div className="w-12 h-6 bg-hva-accent rounded-full relative cursor-pointer">
                            <div className="absolute right-1 top-1 w-4 h-4 bg-white rounded-full"></div>
                        </div>
                    </div>
                </div>

                {/* Section */}
                <div className="bg-hva-card rounded-2xl border border-hva-border-subtle p-6">
                    <h2 className="text-xl font-bold text-hva-cream mb-4 flex items-center gap-2">
                        <Volume2 size={20} className="text-hva-accent" />
                        الصوت
                    </h2>
                    <div className="space-y-4">
                        <div className="flex items-center justify-between">
                            <span className="text-hva-muted">مستوى صوت المساعد</span>
                            <input type="range" className="w-48 accent-hva-accent" />
                        </div>
                        <div className="flex items-center justify-between">
                            <span className="text-hva-muted">تفعيل الاستماع التلقائي</span>
                            <div className="w-12 h-6 bg-hva-card-hover rounded-full relative cursor-pointer border border-hva-dim">
                                <div className="absolute left-1 top-1 w-4 h-4 bg-hva-dim rounded-full"></div>
                            </div>
                        </div>
                    </div>
                </div>

                {/* Section */}
                <div className="bg-hva-card rounded-2xl border border-hva-border-subtle p-6">
                    <h2 className="text-xl font-bold text-hva-cream mb-4 flex items-center gap-2">
                        <Globe size={20} className="text-hva-accent" />
                        اللغة والمنطقة
                    </h2>
                    <div className="flex items-center justify-between">
                        <span className="text-hva-muted">لغة الواجهة</span>
                        <select className="bg-hva-primary border border-hva-border-subtle rounded-lg px-3 py-1 text-hva-cream">
                            <option>العربية</option>
                            <option>English</option>
                        </select>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default SettingsView;
