import React, { useState, useEffect } from 'react';
import './App.css';
import Settings from './components/Settings';
import WordSearch from './components/WordSearch';
import WordList from './components/WordList';

const App = () => {
    const [activeTab, setActiveTab] = useState('search');
    const [token, setToken] = useState(null);
    const [user, setUser] = useState(null);
    const [apiUrl, setApiUrl] = useState('http://localhost:8000');

    useEffect(() => {
        chrome.storage.sync.get(['apiUrl', 'token', 'user'], (result) => {
            if (result.apiUrl) setApiUrl(result.apiUrl);
            if (result.token) setToken(result.token);
            if (result.user) setUser(result.user);
        });
    }, []);

    const handleLogout = () => {
        chrome.storage.sync.remove(['token', 'user'], () => {
            setToken(null);
            setUser(null);
        });
    };

    if (!token) {
        return <Settings onLogin={(token, user) => {
            setToken(token);
            setUser(user);
        }} apiUrl={apiUrl} />;
    }

    return (
        <div className="app">
            <div className="header">
                <h2>📚 Word Learning Assistant</h2>
                {user && <div className="user-info">
                    <span>👤 {user.username}</span>
                    <button onClick={handleLogout} className="logout-btn">🚪</button>
                </div>}
            </div>

            <div className="tabs">
                <button className={`tab ${activeTab === 'search' ? 'active' : ''}`}
                    onClick={() => setActiveTab('search')}>🔍 Search</button>
                <button className={`tab ${activeTab === 'words' ? 'active' : ''}`}
                    onClick={() => setActiveTab('words')}>📖 My Words</button>
                <button className={`tab ${activeTab === 'settings' ? 'active' : ''}`}
                    onClick={() => setActiveTab('settings')}>⚙️ Settings</button>
            </div>

            <div className="content">
                {activeTab === 'search' && <WordSearch apiUrl={apiUrl} token={token} />}
                {activeTab === 'words' && <WordList apiUrl={apiUrl} token={token} />}
                {activeTab === 'settings' && <Settings apiUrl={apiUrl} token={token} onApiUrlChange={setApiUrl} />}
            </div>
        </div>
    );
};

export default App;