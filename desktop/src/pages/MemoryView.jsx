import React, { useState, useEffect } from 'react';
import { Brain, Search, Database, Network, Activity } from 'lucide-react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, ScatterChart, Scatter, ZAxis } from 'recharts';
import { api } from '../services/api';

const MemoryView = () => {
    const [stats, setStats] = useState(null);
    const [searchQuery, setSearchQuery] = useState('');
    const [searchResults, setSearchResults] = useState([]);

    useEffect(() => {
        api.fetchMemoryStats()
            .then(data => setStats(data))
            .catch(err => console.error(err));
    }, []);

    const handleSearch = (e) => {
        e.preventDefault();
        if (!searchQuery.trim()) return;

        api.searchMemory(searchQuery)
            .then(data => setSearchResults(data))
            .catch(err => console.error(err));
    };

    // Mock Data for Visualizations (until backend provides detailed breakdown)
    const sqlData = [
        { name: 'Notes', count: 12 },
        { name: 'Files', count: stats?.sql_records || 0 },
        { name: 'Projects', count: 5 },
        { name: 'Tasks', count: 8 },
    ];

    const vectorData = Array.from({ length: 20 }, () => ({
        x: Math.random() * 100,
        y: Math.random() * 100,
        z: Math.random() * 500
    }));

    return (
        <div className="space-y-6 pb-10">
            <header className="flex items-center justify-between border-b border-white/10 pb-6">
                <div>
                    <h1 className="text-4xl font-bold text-hva-cream flex items-center gap-4">
                        <Brain className="text-hva-accent" size={40} />
                        الذاكرة الحية (The Living Memory)
                    </h1>
                    <p className="text-hva-muted mt-2 text-lg max-w-2xl">
                        نظام ذاكرة ثلاثي الأبعاد يجمع بين البيانات المنظمة، الفهم الدلالي، والعلاقات المترابطة لمنح النظام وعياً سياقياً عميقاً.
                    </p>
                </div>
            </header>

            {/* Layer 1: SQL (Structured) */}
            <section className="bg-hva-card rounded-3xl border border-hva-border-subtle overflow-hidden">
                <div className="p-8 border-b border-white/5 bg-gradient-to-l from-green-500/5 to-transparent">
                    <div className="flex items-start justify-between">
                        <div className="flex items-center gap-4">
                            <div className="p-3 bg-green-500/10 rounded-xl text-green-400">
                                <Database size={32} />
                            </div>
                            <div>
                                <h2 className="text-2xl font-bold text-hva-cream">1. الذاكرة المنظمة (Structured Memory)</h2>
                                <p className="text-hva-muted mt-1">المسؤولة عن حفظ الحقائق، الملفات، والسجلات بدقة متناهية.</p>
                            </div>
                        </div>
                        <div className="text-right">
                            <span className="block text-sm text-hva-muted">عدد السجلات</span>
                            <span className="text-4xl font-bold text-green-400">{stats?.sql_records || 0}</span>
                        </div>
                    </div>
                    <div className="mt-6 text-sm text-hva-dim leading-relaxed max-w-3xl">
                        <p>
                            هذه الطبقة تعمل مثل "الأرشيف الرقمي". تخزن المعلومات بتنسيق جداول (SQL) مما يسمح باسترجاع سريع ودقيق للبيانات المعروفة مسبقاً مثل أسماء الملفات، تواريخ التعديل، وسجلات المحادثة. الرسم البياني أدناه يوضح توزيع هذه البيانات حسب النوع.
                        </p>
                    </div>
                </div>
                <div className="p-8 bg-black/20">
                    <div className="h-80 w-full">
                        <ResponsiveContainer width="100%" height="100%">
                            <BarChart data={sqlData} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
                                <CartesianGrid strokeDasharray="3 3" stroke="#333" vertical={false} />
                                <XAxis dataKey="name" stroke="#666" tick={{ fill: '#888' }} />
                                <YAxis stroke="#666" tick={{ fill: '#888' }} />
                                <Tooltip
                                    contentStyle={{ backgroundColor: '#1a1a1a', border: '1px solid #333', borderRadius: '8px' }}
                                    itemStyle={{ color: '#4ade80' }}
                                    cursor={{ fill: 'rgba(255,255,255,0.05)' }}
                                />
                                <Bar dataKey="count" name="العدد" fill="#4ade80" radius={[6, 6, 0, 0]} barSize={60} />
                            </BarChart>
                        </ResponsiveContainer>
                    </div>
                </div>
            </section>

            {/* Layer 2: Vector (Semantic) */}
            <section className="bg-hva-card rounded-3xl border border-hva-border-subtle overflow-hidden">
                <div className="p-8 border-b border-white/5 bg-gradient-to-l from-blue-500/5 to-transparent">
                    <div className="flex items-start justify-between">
                        <div className="flex items-center gap-4">
                            <div className="p-3 bg-blue-500/10 rounded-xl text-blue-400">
                                <Activity size={32} />
                            </div>
                            <div>
                                <h2 className="text-2xl font-bold text-hva-cream">2. الذاكرة الدلالية (Semantic Memory)</h2>
                                <p className="text-hva-muted mt-1">المسؤولة عن "الفهم" وإيجاد المعاني المتشابهة حتى لو اختلفت الكلمات.</p>
                            </div>
                        </div>
                        <div className="text-right">
                            <span className="block text-sm text-hva-muted">عدد التضمينات</span>
                            <span className="text-4xl font-bold text-blue-400">{stats?.vector_embeddings || 0}</span>
                        </div>
                    </div>
                    <div className="mt-6 text-sm text-hva-dim leading-relaxed max-w-3xl">
                        <p>
                            هنا يتم تحويل النصوص إلى "متجهات" (أرقام) في فضاء متعدد الأبعاد. هذا يسمح للنظام بأن يفهم أن "سيارة" قريبة من "مركبة" في المعنى. الرسم البياني يصور إسقاطاً ثنائي الأبعاد لهذه الأفكار؛ النقاط المتقاربة تمثل مفاهيم مترابطة.
                        </p>
                    </div>
                </div>
                <div className="p-8 bg-black/20">
                    <div className="h-80 w-full relative rounded-xl overflow-hidden border border-white/5 bg-[#0f172a]">
                        <ResponsiveContainer width="100%" height="100%">
                            <ScatterChart margin={{ top: 20, right: 20, bottom: 20, left: 20 }}>
                                <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                                <XAxis type="number" dataKey="x" name="Dimension 1" hide />
                                <YAxis type="number" dataKey="y" name="Dimension 2" hide />
                                <Tooltip cursor={{ strokeDasharray: '3 3' }} contentStyle={{ backgroundColor: '#1a1a1a', border: '1px solid #333' }} />
                                <Scatter name="Embeddings" data={vectorData} fill="#60a5fa" shape="circle" />
                            </ScatterChart>
                        </ResponsiveContainer>
                        <div className="absolute bottom-4 right-4 text-xs text-blue-400/50 bg-black/50 px-2 py-1 rounded">
                            * تمثيل تخيلي للفضاء المتجهي
                        </div>
                    </div>
                </div>
            </section>

            {/* Layer 3: Graph (Relational) */}
            <section className="bg-hva-card rounded-3xl border border-hva-border-subtle overflow-hidden">
                <div className="p-8 border-b border-white/5 bg-gradient-to-l from-purple-500/5 to-transparent">
                    <div className="flex items-start justify-between">
                        <div className="flex items-center gap-4">
                            <div className="p-3 bg-purple-500/10 rounded-xl text-purple-400">
                                <Network size={32} />
                            </div>
                            <div>
                                <h2 className="text-2xl font-bold text-hva-cream">3. الذاكرة الترابطية (Associative Memory)</h2>
                                <p className="text-hva-muted mt-1">شبكة من العقد (Nodes) والروابط (Edges) تحاكي طريقة عمل الدماغ البشري.</p>
                            </div>
                        </div>
                        <div className="text-right">
                            <span className="block text-sm text-hva-muted">عدد العقد</span>
                            <span className="text-4xl font-bold text-purple-400">{stats?.graph_nodes || 0}</span>
                        </div>
                    </div>
                    <div className="mt-6 text-sm text-hva-dim leading-relaxed max-w-3xl">
                        <p>
                            تستخدم هذه الطبقة لربط الكيانات ببعضها (مثلاً: "هيثم" &rarr; "يعمل على" &rarr; "مشروع X"). هذا يسمح للنظام بالإجابة على أسئلة معقدة تتطلب القفز بين المعلومات. الرسم أدناه يوضح شبكة العلاقات النشطة حالياً.
                        </p>
                    </div>
                </div>
                <div className="p-8 bg-black/20 flex justify-center">
                    <div className="h-80 w-full max-w-2xl relative flex items-center justify-center">
                        {/* Advanced CSS Animation for Graph */}
                        <div className="relative w-64 h-64">
                            {/* Central Node */}
                            <div className="absolute top-1/2 left-1/2 w-8 h-8 bg-purple-500 rounded-full -translate-x-1/2 -translate-y-1/2 shadow-[0_0_30px_rgba(168,85,247,0.6)] z-10 animate-pulse"></div>

                            {/* Orbiting Nodes */}
                            {[...Array(6)].map((_, i) => (
                                <div key={i} className="absolute top-1/2 left-1/2 w-full h-full -translate-x-1/2 -translate-y-1/2 animate-spin-slow" style={{ animationDuration: `${10 + i * 5}s`, animationDirection: i % 2 === 0 ? 'normal' : 'reverse' }}>
                                    <div className="absolute top-0 left-1/2 w-4 h-4 bg-purple-400 rounded-full -translate-x-1/2 shadow-[0_0_15px_rgba(168,85,247,0.4)]"></div>
                                    <div className="absolute top-1/2 left-1/2 w-0.5 h-1/2 bg-gradient-to-b from-purple-500/20 to-transparent -translate-x-1/2 origin-top"></div>
                                </div>
                            ))}

                            {/* Connecting Lines (Static for visual structure) */}
                            <svg className="absolute top-0 left-0 w-full h-full opacity-30 pointer-events-none">
                                <circle cx="50%" cy="50%" r="30%" fill="none" stroke="#a855f7" strokeWidth="1" strokeDasharray="4 4" />
                                <circle cx="50%" cy="50%" r="45%" fill="none" stroke="#a855f7" strokeWidth="0.5" />
                            </svg>
                        </div>
                        <div className="absolute bottom-4 text-center text-xs text-purple-400/50">
                            محاكاة بصرية للشبكة العصبية
                        </div>
                    </div>
                </div>
            </section>

            {/* Search Section */}
            <section className="bg-hva-card rounded-3xl border border-hva-border-subtle p-8">
                <h2 className="text-xl font-bold text-hva-cream mb-6 flex items-center gap-2">
                    <Search size={24} className="text-hva-accent" />
                    اختبار الذاكرة (Search & Retrieval)
                </h2>
                <form onSubmit={handleSearch} className="relative max-w-2xl mx-auto">
                    <Search className="absolute right-5 top-1/2 -translate-y-1/2 text-hva-muted" size={24} />
                    <input
                        type="text"
                        placeholder="اسأل الذاكرة عن أي شيء..."
                        className="w-full bg-black/30 border border-hva-border-subtle rounded-2xl py-4 pr-14 pl-6 text-lg text-hva-cream focus:outline-none focus:border-hva-accent focus:ring-1 focus:ring-hva-accent transition-all shadow-inner"
                        value={searchQuery}
                        onChange={(e) => setSearchQuery(e.target.value)}
                    />
                </form>

                <div className="mt-8 space-y-4 max-w-3xl mx-auto">
                    {searchResults.length > 0 ? (
                        searchResults.map((item, index) => (
                            <div key={index} className="p-6 bg-white/5 rounded-2xl border border-white/10 hover:border-hva-accent/50 transition-colors">
                                <p className="text-hva-cream leading-relaxed">
                                    {item.content || item.text || item.summary || (typeof item === 'string' ? item : JSON.stringify(item))}
                                </p>
                                <div className="mt-3 flex gap-2">
                                    {(item.metadata?.type || item.type) && (
                                        <span className="text-xs px-2 py-1 rounded bg-white/10 text-hva-muted uppercase tracking-wider">
                                            {item.metadata?.type || item.type}
                                        </span>
                                    )}
                                    {item.score !== undefined && (
                                        <span className="text-xs px-2 py-1 rounded bg-green-500/10 text-green-400">
                                            Match: {Math.round(item.score * 100)}%
                                        </span>
                                    )}
                                </div>
                            </div>
                        ))
                    ) : searchQuery && (
                        <div className="text-center text-hva-dim py-8">
                            لا توجد نتائج بحث مطابقة.
                        </div>
                    )}
                </div>
            </section>
        </div>
    );
};

export default MemoryView;
