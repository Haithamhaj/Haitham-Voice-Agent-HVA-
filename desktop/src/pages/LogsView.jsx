import React, { useState, useEffect } from 'react';
import { Terminal, Server, RefreshCw, Trash2, AlertCircle, Info, AlertTriangle } from 'lucide-react';
import { logger, useLogs } from '../services/logger';
import { api } from '../services/api';

const LogsView = () => {
    const [activeTab, setActiveTab] = useState('frontend');
    const frontendLogs = useLogs();
    const [backendLogs, setBackendLogs] = useState([]);
    const [loading, setLoading] = useState(false);

    const fetchBackendLogs = async () => {
        setLoading(true);
        try {
            const logs = await api.fetchSystemLogs();
            setBackendLogs(logs);
        } catch (error) {
            console.error("Failed to fetch backend logs", error);
            logger.error("Failed to fetch backend logs", error.message);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        if (activeTab === 'backend') {
            fetchBackendLogs();
        }
    }, [activeTab]);

    const getLevelColor = (level) => {
        switch (level) {
            case 'ERROR': return 'text-red-500';
            case 'WARN': return 'text-yellow-500';
            case 'INFO': return 'text-blue-400';
            default: return 'text-hva-muted';
        }
    };

    const getLevelIcon = (level) => {
        switch (level) {
            case 'ERROR': return <AlertCircle size={16} />;
            case 'WARN': return <AlertTriangle size={16} />;
            case 'INFO': return <Info size={16} />;
            default: return <Info size={16} />;
        }
    };

    return (
        <div className="flex flex-col h-full space-y-4">
            <header className="flex justify-between items-center">
                <h1 className="text-3xl font-bold text-hva-cream flex items-center gap-3">
                    <Terminal className="text-hva-accent" size={32} />
                    سجلات النظام
                </h1>
                <div className="flex bg-hva-card rounded-lg p-1 border border-hva-border-subtle">
                    <button
                        onClick={() => setActiveTab('frontend')}
                        className={`px-4 py-2 rounded-md transition-colors flex items-center gap-2 ${activeTab === 'frontend' ? 'bg-hva-accent text-hva-primary font-bold' : 'text-hva-muted hover:text-hva-cream'}`}
                    >
                        <Terminal size={16} />
                        الواجهة
                    </button>
                    <button
                        onClick={() => setActiveTab('backend')}
                        className={`px-4 py-2 rounded-md transition-colors flex items-center gap-2 ${activeTab === 'backend' ? 'bg-hva-accent text-hva-primary font-bold' : 'text-hva-muted hover:text-hva-cream'}`}
                    >
                        <Server size={16} />
                        الخادم
                    </button>
                </div>
            </header>

            <div className="flex-1 bg-hva-card rounded-2xl border border-hva-border-subtle overflow-hidden flex flex-col">
                <div className="p-4 border-b border-hva-border-subtle flex justify-between items-center bg-hva-primary/30">
                    <div className="flex gap-2">
                        <span className="text-sm text-hva-muted">
                            {activeTab === 'frontend' ? `${frontendLogs.length} سجل` : 'آخر 100 سطر'}
                        </span>
                    </div>
                    <div className="flex gap-2">
                        <button
                            onClick={activeTab === 'frontend' ? () => logger.clear() : fetchBackendLogs}
                            className="p-2 hover:bg-hva-primary rounded-lg text-hva-muted hover:text-hva-cream transition-colors"
                            title={activeTab === 'frontend' ? "مسح السجلات" : "تحديث"}
                        >
                            {activeTab === 'frontend' ? <Trash2 size={18} /> : <RefreshCw size={18} className={loading ? "animate-spin" : ""} />}
                        </button>
                    </div>
                </div>

                <div className="flex-1 overflow-y-auto p-4 font-mono text-sm space-y-2">
                    {activeTab === 'frontend' ? (
                        frontendLogs.length === 0 ? (
                            <div className="text-center text-hva-muted py-10">لا توجد سجلات حالياً</div>
                        ) : (
                            frontendLogs.map(log => (
                                <div key={log.id} className="flex gap-3 hover:bg-hva-primary/20 p-2 rounded transition-colors">
                                    <span className="text-hva-muted shrink-0 w-24 text-xs">{log.timestamp.split('T')[1].split('.')[0]}</span>
                                    <span className={`shrink-0 w-16 font-bold flex items-center gap-1 ${getLevelColor(log.level)}`}>
                                        {getLevelIcon(log.level)}
                                        {log.level}
                                    </span>
                                    <span className="text-hva-cream break-all">{log.message}</span>
                                    {log.details && <span className="text-hva-muted text-xs italic">{JSON.stringify(log.details)}</span>}
                                </div>
                            ))
                        )
                    ) : (
                        <div className="whitespace-pre-wrap text-hva-cream/80 leading-relaxed">
                            {backendLogs.length > 0 ? backendLogs.join('\n') : "جاري التحميل..."}
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
};

export default LogsView;
