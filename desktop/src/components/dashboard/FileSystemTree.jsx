import React, { useState, useEffect } from 'react';
import { Folder, File, ChevronRight, ChevronDown, HardDrive } from 'lucide-react';
import { api } from '../../services/api';

const TreeNode = ({ node, level = 0, onLoadChildren }) => {
    const [isOpen, setIsOpen] = useState(false);
    const [isLoading, setIsLoading] = useState(false);
    const hasChildren = node.type === 'directory'; // Directories might have children

    const handleClick = async () => {
        if (hasChildren) {
            // Toggle Directory
            if (!isOpen && (!node.children || node.children.length === 0)) {
                setIsLoading(true);
                await onLoadChildren(node);
                setIsLoading(false);
            }
            setIsOpen(!isOpen);
        } else {
            // Open File
            try {
                await api.openFile(node.path);
            } catch (error) {
                console.error("Failed to open file:", error);
            }
        }
    };

    const getIcon = () => {
        if (node.type === 'directory') return <Folder size={16} className="text-blue-400" />;
        return <File size={16} className="text-hva-muted" />;
    };

    return (
        <div className="select-none">
            <div
                className={`flex items-center gap-2 py-1 px-2 hover:bg-white/5 rounded cursor-pointer transition-colors ${level === 0 ? 'font-bold text-hva-cream' : 'text-hva-muted text-sm'}`}
                style={{ paddingRight: `${level * 12}px` }} // RTL indentation
                onClick={handleClick}
            >
                {hasChildren && (
                    <span className="text-hva-muted">
                        {isLoading ? (
                            <div className="w-3.5 h-3.5 border-2 border-hva-muted border-t-transparent rounded-full animate-spin" />
                        ) : (
                            isOpen ? <ChevronDown size={14} /> : <ChevronRight size={14} className="rtl:rotate-180" />
                        )}
                    </span>
                )}
                {!hasChildren && <span className="w-[14px]" />} {/* Spacer */}

                {getIcon()}
                <span className="truncate">{node.name}</span>
            </div>

            {isOpen && node.children && (
                <div className="mr-2 border-r border-white/10 pr-2">
                    {node.children.map((child, index) => (
                        <TreeNode key={index} node={child} level={level + 1} onLoadChildren={onLoadChildren} />
                    ))}
                </div>
            )}
        </div>
    );
};

const FileSystemTree = () => {
    const [treeData, setTreeData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    const fetchTree = async (path = "~", depth = 1) => {
        try {
            const result = await api.getFileTree(path, depth);
            if (result.success) {
                return result.tree;
            } else {
                console.error(result.message);
                return null;
            }
        } catch (err) {
            console.error("Failed to load file system.", err);
            return null;
        }
    };

    const loadRoot = async () => {
        setLoading(true);
        const root = await fetchTree("~", 1);
        if (root) {
            setTreeData(root);
            setError(null);
        } else {
            setError("Failed to load root.");
        }
        setLoading(false);
    };

    useEffect(() => {
        loadRoot();
        // Auto-refresh every 10 seconds to keep in sync with "Smart Sync"
        const interval = setInterval(loadRoot, 10000);
        return () => clearInterval(interval);
    }, []);

    const handleLoadChildren = async (parentNode) => {
        if (parentNode.children && parentNode.children.length > 0) return;

        const childrenTree = await fetchTree(parentNode.path, 1);
        if (childrenTree && childrenTree.children) {
            // Update tree state deeply
            const updateNode = (nodes) => {
                if (nodes.path === parentNode.path) {
                    return { ...nodes, children: childrenTree.children };
                }
                if (nodes.children) {
                    return { ...nodes, children: nodes.children.map(updateNode) };
                }
                return nodes;
            };
            setTreeData(prev => updateNode(prev));
        }
    };

    if (loading && !treeData) return <div className="animate-pulse h-40 bg-white/5 rounded-xl"></div>;
    if (error) return <div className="text-red-400 text-sm p-4">Error: {error}</div>;

    return (
        <div className="bg-hva-card rounded-2xl border border-hva-border-subtle p-4 h-[500px] flex flex-col">
            <div className="flex items-center justify-between mb-4">
                <h2 className="text-lg font-bold text-hva-cream flex items-center gap-2">
                    <HardDrive size={20} className="text-hva-accent" />
                    شجرة المعرفة (الملفات)
                </h2>
                <button
                    onClick={loadRoot}
                    className="text-xs text-hva-muted hover:text-hva-cream bg-white/5 hover:bg-white/10 px-2 py-1 rounded transition-colors"
                >
                    تحديث
                </button>
            </div>

            <div className="flex-1 overflow-y-auto custom-scrollbar pr-1" dir="rtl">
                {treeData ? (
                    <TreeNode node={treeData} onLoadChildren={handleLoadChildren} />
                ) : (
                    <p className="text-hva-muted text-center mt-10">No files found.</p>
                )}
            </div>
        </div>
    );
};

export default FileSystemTree;
