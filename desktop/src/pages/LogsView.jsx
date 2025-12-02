import React, { useState, useEffect } from 'react';
import ToolkitView from '../developer-toolkit/ToolkitView';
import { api } from '../services/api';
import { useWebSocket } from '../hooks/useWebSocket';
import { logger } from '../developer-toolkit/logger';

const LogsView = () => {
    const { isListening, wsConnected } = useWebSocket();
    const [memoryStats, setMemoryStats] = useState(null);
    const [backendLogs, setBackendLogs] = useState([]);

    const fetchBackendLogs = async () => {
        try {
            const logs = await api.fetchSystemLogs();
            setBackendLogs(logs);
        } catch (error) {
            console.error("Failed to fetch backend logs", error);
            logger.error("Failed to fetch backend logs", error.message);
        }
    };

    const fetchStateData = async () => {
        try {
            const stats = await api.fetchMemoryStats();
            setMemoryStats(stats);
        } catch (e) {
            console.error(e);
        }
    };

    useEffect(() => {
        // Initial fetch
        fetchStateData();
        fetchBackendLogs();
    }, []);

    return (
        <ToolkitView
            api={api}
            wsStatus={{ connected: wsConnected, listening: isListening }}
            memoryStats={memoryStats}
            onRefreshState={fetchStateData}
            onRefreshBackend={fetchBackendLogs}
            backendLogs={backendLogs}
        />
    );
};

export default LogsView;
