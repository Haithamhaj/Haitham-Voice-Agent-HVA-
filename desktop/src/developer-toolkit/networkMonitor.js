import { useState, useEffect } from 'react';

const listeners = new Set();

const emitChange = () => {
    listeners.forEach(listener => listener());
};

class NetworkMonitorService {
    constructor() {
        this.requests = [];
        this.maxRequests = 100;
    }

    logRequest(url, method, body) {
        const id = Date.now() + Math.random();
        const requestEntry = {
            id,
            url,
            method,
            startTime: Date.now(),
            status: 'pending',
            requestBody: body,
            responseBody: null,
            duration: null
        };
        this.requests.unshift(requestEntry);
        if (this.requests.length > this.maxRequests) {
            this.requests.pop();
        }
        emitChange();
        return id;
    }

    logResponse(id, status, body) {
        const entry = this.requests.find(r => r.id === id);
        if (entry) {
            entry.status = status;
            entry.responseBody = body;
            entry.duration = Date.now() - entry.startTime;
            emitChange();
        }
    }

    logError(id, error) {
        const entry = this.requests.find(r => r.id === id);
        if (entry) {
            entry.status = 'error';
            entry.responseBody = { error: error.message };
            entry.duration = Date.now() - entry.startTime;
            emitChange();
        }
    }

    getRequests() {
        return this.requests;
    }

    clear() {
        this.requests = [];
        emitChange();
    }

    subscribe(listener) {
        listeners.add(listener);
        return () => listeners.delete(listener);
    }
}

export const networkMonitor = new NetworkMonitorService();

export const useNetworkMonitor = () => {
    const [requests, setRequests] = useState(networkMonitor.getRequests());

    useEffect(() => {
        return networkMonitor.subscribe(() => {
            setRequests([...networkMonitor.getRequests()]);
        });
    }, []);

    return requests;
};
