const API_BASE_URL = 'http://127.0.0.1:8765';

export const api = {
    // Voice
    startVoice: () => fetch(`${API_BASE_URL}/voice/start`, { method: 'POST' }),
    stopVoice: () => fetch(`${API_BASE_URL}/voice/stop`, { method: 'POST' }),

    // Dashboard Stats
    fetchTasks: () => fetch(`${API_BASE_URL}/tasks/`).then(res => res.json()),
    fetchEmails: () => fetch(`${API_BASE_URL}/gmail/unread`).then(res => res.json()),
    fetchEvents: () => fetch(`${API_BASE_URL}/calendar/today`).then(res => res.json()),

    // Memory
    fetchMemoryStats: () => fetch(`${API_BASE_URL}/memory/stats`).then(res => res.json()),
    searchMemory: (query) => fetch(`${API_BASE_URL}/memory/search?query=${encodeURIComponent(query)}`).then(res => res.json()),
};
