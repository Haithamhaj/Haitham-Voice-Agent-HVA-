import React from 'react';
import { Mic, X } from 'lucide-react';

const VoiceOverlay = ({ onClose }) => {
    return (
        <div className="fixed inset-0 bg-black/60 backdrop-blur-sm z-50 flex items-center justify-center flex-col animate-in fade-in duration-200">
            <div className="relative">
                <div className="absolute inset-0 bg-red-500/30 rounded-full animate-ping"></div>
                <div className="absolute inset-0 bg-red-500/20 rounded-full animate-pulse delay-75"></div>
                <div className="w-32 h-32 bg-gradient-to-br from-hva-card to-hva-primary rounded-full flex items-center justify-center border-4 border-red-500 shadow-[0_0_50px_rgba(239,68,68,0.5)] relative z-10">
                    <Mic size={48} className="text-red-500" />
                </div>
            </div>

            <h2 className="mt-8 text-3xl font-bold text-white tracking-wide">أستمع إليك...</h2>
            <p className="mt-2 text-hva-muted text-lg">تحدث الآن</p>

            <button
                onClick={onClose}
                className="mt-12 px-6 py-2 rounded-full bg-white/10 hover:bg-white/20 text-white transition-colors flex items-center gap-2"
            >
                <X size={18} />
                <span>إلغاء</span>
            </button>
        </div>
    );
};

export default VoiceOverlay;
