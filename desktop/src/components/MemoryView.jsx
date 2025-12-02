import React, { useState, useEffect } from 'react';
import { Brain, Search, Database, Network } from 'lucide-react';

const MemoryView = () => {
    const [stats, setStats] = useState(null);
    const [searchQuery, setSearchQuery] = useState('');
    const [searchResults, setSearchResults] = useState([]);

    useEffect(() => {
        fetch('http://localhost:8765/memory/stats')
            .then(res => res.json())
            .then(data => setStats(data))
            .catch(err => console.error(err));
    }, []);

    const handleSearch = (e) => {
        e.preventDefault();
        if (!searchQuery.trim()) return;

        fetch(`http://localhost:8765/memory/search?query=${encodeURIComponent(searchQuery)}`)
            .then(res => res.json())
            .then(data => setSearchResults(data))
            .catch(err => console.error(err));
    };

    return (
        <div className="space-y-6">
            <header className="flex items-center justify-between">
                <div>
                    <h1 className="text-3xl font-bold text-hva-cream flex items-center gap-3">
                        <Brain className="text-hva-accent" size={32} />
                        الذاكرة الحية
                    </h1>
                    <p className="text-hva-muted mt-1">استعراض وإدارة قاعدة المعرفة</p>
                </div>
            </header>

            {/* Stats Cards */}
            <div className="grid grid-cols-3 gap-6">
                <div className="bg-hva-card p-5 rounded-2xl border border-hva-border-subtle">
                    <div className="flex items-center gap-3 mb-2 text-purple-400">
                        <Network size={20} />
                        <h3 className="font-bold">Graph Nodes</h3>
                    </div>
                    <p className="text-2xl font-bold text-hva-cream">{stats?.graph_nodes || '-'}</p>
                </div>
                <div className="bg-hva-card p-5 rounded-2xl border border-hva-border-subtle">
                    <div className="flex items-center gap-3 mb-2 text-blue-400">
                        <Database size={20} />
                        <h3 className="font-bold">Vector Embeddings</h3>
                    </div>
                    <p className="text-2xl font-bold text-hva-cream">{stats?.vectors || '-'}</p>
                </div>
                <div className="bg-hva-card p-5 rounded-2xl border border-hva-border-subtle">
                    <div className="flex items-center gap-3 mb-2 text-green-400">
                        <Database size={20} />
                        <h3 className="font-bold">SQL Records</h3>
                    </div>
                    <p className="text-2xl font-bold text-hva-cream">{stats?.sql_records || '-'}</p>
                </div>
            </div>

            {/* Search */}
            <div className="bg-hva-card rounded-2xl border border-hva-border-subtle p-6">
                <form onSubmit={handleSearch} className="relative">
                    <Search className="absolute right-4 top-1/2 -translate-y-1/2 text-hva-muted" size={20} />
                    <input
                        type="text"
                        placeholder="ابحث في الذاكرة..."
                        className="w-full bg-hva-primary border border-hva-border-subtle rounded-xl py-3 pr-12 pl-4 text-hva-cream focus:outline-none focus:border-hva-accent transition-colors"
                        value={searchQuery}
                        onChange={(e) => setSearchQuery(e.target.value)}
                    />
                </form>

                <div className="mt-6 space-y-4">
                    {searchResults.length > 0 ? (
                        searchResults.map((item, index) => (
                            <div key={index} className="p-4 bg-hva-primary/50 rounded-xl border border-hva-border-subtle">
                                <p className="text-hva-cream">{item.content || JSON.stringify(item)}</p>
                            </div>
                        ))
                    ) : (
                        <div className="text-center text-hva-dim py-8">
                            لا توجد نتائج بحث
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
};

export default MemoryView;
