import React from 'react';
import { Minus, Square, X } from 'lucide-react';

const TitleBar = () => {
    const handleMinimize = () => {
        window.electronAPI?.minimize();
    };

    const handleMaximize = () => {
        window.electronAPI?.maximize();
    };

    const handleClose = () => {
        window.electronAPI?.close();
    };

    return (
        <div className="h-10 bg-hva-primary flex items-center justify-between px-4 select-none" style={{ WebkitAppRegion: 'drag' }}>
            <div className="flex items-center gap-2">
                <div className="w-3 h-3 rounded-full bg-red-500 hover:bg-red-600 cursor-pointer" onClick={handleClose}></div>
                <div className="w-3 h-3 rounded-full bg-yellow-500 hover:bg-yellow-600 cursor-pointer" onClick={handleMinimize}></div>
                <div className="w-3 h-3 rounded-full bg-green-500 hover:bg-green-600 cursor-pointer" onClick={handleMaximize}></div>
            </div>
            <div className="text-hva-muted text-sm font-medium">Haitham Voice Agent</div>
            <div className="w-16"></div> {/* Spacer for balance */}
        </div>
    );
};

export default TitleBar;
