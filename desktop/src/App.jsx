import { useState, useEffect } from 'react';
import { HashRouter, Routes, Route } from 'react-router-dom';
import TitleBar from './components/TitleBar';
import Sidebar from './components/Sidebar';
import Dashboard from './components/Dashboard';
import MemoryView from './components/MemoryView';
import GmailView from './components/GmailView';
import CalendarView from './components/CalendarView';
import TasksView from './components/TasksView';
import SettingsView from './components/SettingsView';
import VoiceOverlay from './components/VoiceOverlay';

function App() {
  const [isListening, setIsListening] = useState(false);
  const [wsConnected, setWsConnected] = useState(false);

  // WebSocket Connection
  useEffect(() => {
    const connectWs = () => {
      const ws = new WebSocket('ws://127.0.0.1:8765/ws');

      ws.onopen = () => {
        setWsConnected(true);
        console.log('WebSocket Connected');
      };

      ws.onmessage = (event) => {
        const data = JSON.parse(event.data);
        if (data.type === 'status') {
          setIsListening(data.listening);
        }
      };

      ws.onclose = () => {
        setWsConnected(false);
        // Reconnect after 3 seconds
        setTimeout(connectWs, 3000);
      };

      return ws;
    };

    const ws = connectWs();
    return () => ws.close();
  }, []);

  // Listen for keyboard shortcut from Electron
  useEffect(() => {
    window.electronAPI?.onTriggerVoice(() => {
      toggleListening();
    });
  }, [isListening]); // Add dependency to ensure latest state is used

  const toggleListening = async () => {
    try {
      if (isListening) {
        await fetch('http://127.0.0.1:8765/voice/stop', { method: 'POST' });
      } else {
        await fetch('http://127.0.0.1:8765/voice/start', { method: 'POST' });
      }
    } catch (e) {
      console.error("Failed to toggle voice", e);
    }
  };

  return (
    <HashRouter>
      <div className="h-screen bg-hva-deep text-hva-cream overflow-hidden rounded-2xl flex flex-col" dir="rtl">
        <TitleBar />

        <div className="flex flex-1 overflow-hidden">
          <Sidebar isListening={isListening} wsConnected={wsConnected} />

          <main className="flex-1 overflow-auto p-8 bg-hva-primary/30">
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/memory" element={<MemoryView />} />
              <Route path="/gmail" element={<GmailView />} />
              <Route path="/calendar" element={<CalendarView />} />
              <Route path="/tasks" element={<TasksView />} />
              <Route path="/settings" element={<SettingsView />} />
            </Routes>
          </main>
        </div>

        {isListening && <VoiceOverlay onClose={toggleListening} />}
      </div>
    </HashRouter>
  );
}

export default App;
