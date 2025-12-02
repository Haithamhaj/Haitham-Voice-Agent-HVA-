import React, { useEffect } from 'react';
import { HashRouter, Routes, Route } from 'react-router-dom';
import TitleBar from './components/layout/TitleBar';
import Sidebar from './components/layout/Sidebar';
import Dashboard from './pages/Dashboard';
import GmailView from './pages/GmailView';
import CalendarView from './pages/CalendarView';
import TasksView from './pages/TasksView';
import SettingsView from './pages/SettingsView';
import ChatView from './pages/ChatView';
import MemoryView from './pages/MemoryView';
import VoiceOverlay from './components/voice/VoiceOverlay';
import { useWebSocket } from './hooks/useWebSocket';
import { api } from './services/api';

function App() {
  const { isListening, wsConnected, setIsListening } = useWebSocket();

  // Listen for keyboard shortcut from Electron
  useEffect(() => {
    window.electronAPI?.onTriggerVoice(() => {
      toggleListening();
    });
  }, [isListening]); // Add dependency to ensure latest state is used

  const toggleListening = async () => {
    try {
      if (isListening) {
        await api.stopVoice();
      } else {
        await api.startVoice();
      }
    } catch (e) {
      console.error("Failed to toggle voice", e);
    }
  };

  return (
    <HashRouter>
      <div className="flex flex-col h-screen bg-hva-primary text-hva-cream overflow-hidden" dir="rtl">
        <TitleBar />

        <div className="flex flex-1 overflow-hidden">
          <Sidebar isListening={isListening} wsConnected={wsConnected} toggleListening={toggleListening} />

          <main className="flex-1 overflow-auto p-8 bg-hva-primary/30">
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/chat" element={<ChatView />} />
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
