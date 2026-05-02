import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';  // ← ЭТО ВАЖНО! Импортируем App

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<App />);