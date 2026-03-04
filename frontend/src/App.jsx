import { useState } from 'react';
import ChatBot from './components/ChatBot';
import Dashboard from './components/Dashboard';
import './App.css';

function App() {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [refreshKey, setRefreshKey] = useState(0);

  const handleNewTrace = () => {
    setRefreshKey((k) => k + 1);
  };

  return (
    <div className="app">
      <header className="app-header">
        <div className="header-content">
          <div className="logo">
            <span className="logo-icon">◉</span>
            <h1>SupportLens</h1>
          </div>
          <p className="tagline">Customer Support Observability</p>
        </div>
        <nav className="tab-nav">
          <button
            className={`tab-btn ${activeTab === 'dashboard' ? 'active' : ''}`}
            onClick={() => setActiveTab('dashboard')}
          >
            📊 Dashboard
          </button>
          <button
            className={`tab-btn ${activeTab === 'chatbot' ? 'active' : ''}`}
            onClick={() => setActiveTab('chatbot')}
          >
            💬 Chatbot
          </button>
        </nav>
      </header>
      <main className="app-main">
        {activeTab === 'dashboard' ? (
          <Dashboard refreshKey={refreshKey} />
        ) : (
          <ChatBot onNewTrace={handleNewTrace} />
        )}
      </main>
    </div>
  );
}

export default App;
