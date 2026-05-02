
import React, { useState, useEffect } from 'react';
import './Settings.css';

const Settings = ({ onLogin, apiUrl, onApiUrlChange, token }) => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [email, setEmail] = useState('');
    const [nickname, setNickname] = useState('');
    const [isLogin, setIsLogin] = useState(true);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    const [localApiUrl, setLocalApiUrl] = useState(apiUrl || 'http://localhost:8000');
    const [success, setSuccess] = useState('');

    useEffect(() => {
        // Load saved API URL
        chrome.storage.sync.get(['apiUrl'], (result) => {
            if (result.apiUrl) {
                setLocalApiUrl(result.apiUrl);
            }
        });
    }, []);

    const saveApiUrl = () => {
        chrome.storage.sync.set({ apiUrl: localApiUrl }, () => {
            setSuccess('API URL saved!');
            setTimeout(() => setSuccess(''), 2000);
            if (onApiUrlChange) onApiUrlChange(localApiUrl);
        });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError('');

        const endpoint = isLogin ? '/users/login' : '/users/register';
        const body = isLogin
            ? { username, password }
            : { username, email, password, nickname: nickname || username };

        try {
            const response = await fetch(`${localApiUrl}${endpoint}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(body),
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.detail || 'Authentication failed');
            }

            if (isLogin) {
                // Login successful
                chrome.storage.sync.set({
                    token: data.access_token,
                    apiUrl: localApiUrl
                }, () => {
                    // Fetch user info
                    fetch(`${localApiUrl}/users/me`, {
                        headers: {
                            'Authorization': `Bearer ${data.access_token}`
                        }
                    })
                    .then(res => res.json())
                    .then(userData => {
                        chrome.storage.sync.set({ user: userData });
                        if (onLogin) onLogin(data.access_token, userData);
                    });
                });
            } else {
                // Registration successful, switch to login
                setSuccess('Registration successful! Please login.');
                setIsLogin(true);
                setPassword('');
            }
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    // If we have token and onLogin is not provided, we're in settings mode
    if (token && !onLogin) {
        return (
            <div className="settings">
                <h3>API Settings</h3>
                <div className="setting-group">
                    <label>API URL:</label>
                    <input
                        type="text"
                        value={localApiUrl}
                        onChange={(e) => setLocalApiUrl(e.target.value)}
                        placeholder="http://localhost:8000"
                    />
                    <button onClick={saveApiUrl} className="save-btn">Save</button>
                    {success && <div className="success">{success}</div>}
                </div>
                <div className="info">
                    <p>💡 Tip: Make sure your backend server is running</p>
                </div>
            </div>
        );
    }

    // Login/Register form
    return (
        <div className="auth-container">
            <div className="auth-header">
                <h3>{isLogin ? '🔐 Login' : '📝 Register'}</h3>
            </div>

            <form onSubmit={handleSubmit} className="auth-form">
                <div className="form-group">
                    <label>API URL:</label>
                    <input
                        type="text"
                        value={localApiUrl}
                        onChange={(e) => setLocalApiUrl(e.target.value)}
                        placeholder="http://localhost:8000"
                        required
                    />
                </div>

                <div className="form-group">
                    <label>Username:</label>
                    <input
                        type="text"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                        required
                    />
                </div>

                {!isLogin && (
                    <>
                        <div className="form-group">
                            <label>Email:</label>
                            <input
                                type="email"
                                value={email}
                                onChange={(e) => setEmail(e.target.value)}
                                required
                            />
                        </div>
                        <div className="form-group">
                            <label>Nickname (optional):</label>
                            <input
                                type="text"
                                value={nickname}
                                onChange={(e) => setNickname(e.target.value)}
                            />
                        </div>
                    </>
                )}

                <div className="form-group">
                    <label>Password:</label>
                    <input
                        type="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        required
                        minLength={6}
                    />
                </div>

                {error && <div className="error">{error}</div>}
                {success && <div className="success">{success}</div>}

                <button type="submit" disabled={loading} className="submit-btn">
                    {loading ? 'Loading...' : (isLogin ? 'Login' : 'Register')}
                </button>

                <button
                    type="button"
                    onClick={() => {
                        setIsLogin(!isLogin);
                        setError('');
                        setSuccess('');
                    }}
                    className="switch-btn"
                >
                    {isLogin ? "Don't have an account? Register" : "Already have an account? Login"}
                </button>
            </form>
        </div>
    );
};

export default Settings;