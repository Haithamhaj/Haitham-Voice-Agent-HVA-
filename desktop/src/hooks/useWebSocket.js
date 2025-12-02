import { useState, useEffect, useRef } from 'react';

export const useWebSocket = () => {
    const [isListening, setIsListening] = useState(false);
    const [wsConnected, setWsConnected] = useState(false);
    const wsRef = useRef(null);

    useEffect(() => {
        const connectWs = () => {
            if (wsRef.current?.readyState === WebSocket.OPEN) return;

            console.log('Attempting to connect to WebSocket...');
            const ws = new WebSocket('ws://127.0.0.1:8765/ws');
            wsRef.current = ws;

            ws.onopen = () => {
                setWsConnected(true);
                console.log('WebSocket Connected');
            };

            ws.onmessage = (event) => {
                try {
                    const data = JSON.parse(event.data);
                    if (data.type === 'status') {
                        setIsListening(data.listening);
                    }
                } catch (e) {
                    console.error("Failed to parse WS message", e);
                }
            };

            ws.onclose = (event) => {
                console.log('WebSocket Disconnected', event.code, event.reason);
                setWsConnected(false);
                wsRef.current = null;
                // Reconnect after 3 seconds
                setTimeout(connectWs, 3000);
            };

            ws.onerror = (error) => {
                console.error('WebSocket Error:', error);
                ws.close();
            };
        };

        connectWs();

        return () => {
            if (wsRef.current) {
                wsRef.current.onclose = null; // Prevent reconnect on cleanup
                wsRef.current.close();
                wsRef.current = null;
            }
        };
    }, []);

    return { isListening, wsConnected, setIsListening };
};
