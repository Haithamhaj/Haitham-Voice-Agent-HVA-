import { useState, useEffect } from 'react';

// Simple event emitter for log updates
const listeners = new Set();
const errorListeners = new Set();

const emitChange = () => {
    listeners.forEach(listener => listener());
};

const emitError = (error) => {
    errorListeners.forEach(listener => listener(error));
};

class LoggerService {
    constructor() {
        this.logs = [];
        this.maxLogs = 1000;
    }

    addLog(level, message, details = null) {
        const logEntry = {
            id: Date.now() + Math.random(),
            timestamp: new Date().toISOString(),
            level,
            message,
            details
        };

        this.logs.unshift(logEntry);
        if (this.logs.length > this.maxLogs) {
            this.logs.pop();
        }

        console.log(`[${level}] ${message}`, details || '');
        emitChange();

        if (level === 'ERROR') {
            emitError(logEntry);
        }
    }

    info(message, details) {
        this.addLog('INFO', message, details);
    }

    warn(message, details) {
        this.addLog('WARN', message, details);
    }

    error(message, details) {
        this.addLog('ERROR', message, details);
    }

    getLogs() {
        return this.logs;
    }

    clear() {
        this.logs = [];
        emitChange();
    }

    subscribe(listener) {
        listeners.add(listener);
        return () => listeners.delete(listener);
    }

    subscribeErrors(listener) {
        errorListeners.add(listener);
        return () => errorListeners.delete(listener);
    }
}

export const logger = new LoggerService();

// Hook to use logs in components
export const useLogs = () => {
    const [logs, setLogs] = useState(logger.getLogs());

    useEffect(() => {
        return logger.subscribe(() => {
            setLogs([...logger.getLogs()]);
        });
    }, []);

    return logs;
};
