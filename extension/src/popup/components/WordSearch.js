import React, { useState } from 'react';
import './WordSearch.css';

const WordSearch = ({ apiUrl, token }) => {
    const [word, setWord] = useState('');
    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState(null);
    const [error, setError] = useState('');
    const [addLoading, setAddLoading] = useState(false);
    const [addSuccess, setAddSuccess] = useState(false);

    const searchWord = async (e) => {
        e.preventDefault();
        if (!word.trim()) return;

        setLoading(true);
        setError('');
        setResult(null);
        setAddSuccess(false);

        try {
            const response = await fetch(`${apiUrl}/words/search?word=${encodeURIComponent(word)}`, {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${token}`,
                },
            });

            if (!response.ok) {
                const data = await response.json();
                throw new Error(data.detail || 'Search failed');
            }

            const data = await response.json();
            setResult(data);
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    const addToNotes = async () => {
        if (!result) return;
        setAddLoading(true);
        setError('');
        try {
            const response = await fetch(`${apiUrl}/words/add`, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ word: result.word }),
            });

            if (!response.ok) {
                const data = await response.json();
                throw new Error(data.detail || 'Failed to add word');
            }

            setAddSuccess(true);
            setTimeout(() => setAddSuccess(false), 2000);
        } catch (err) {
            setError(err.message);
        } finally {
            setAddLoading(false);
        }
    };

    return (
        <div className="word-search">
            <form onSubmit={searchWord} className="search-form">
                <input
                    type="text"
                    value={word}
                    onChange={(e) => setWord(e.target.value)}
                    placeholder="Enter a word to search..."
                    className="search-input"
                />
                <button type="submit" disabled={loading} className="search-button">
                    {loading ? '🔍' : 'Search'}
                </button>
            </form>

            {error && <div className="error-message">{error}</div>}
            {addSuccess && <div className="success-message">✅ Word added to your notes!</div>}

            {result && (
                <div className="result-container">
                    <div className="word-header">
                        <h3>{result.word}</h3>
                        <button onClick={addToNotes} disabled={addLoading} className="add-btn">
                            {addLoading ? 'Adding...' : '📌 Add to my words'}
                        </button>
                    </div>
                    <div className="word-summary">
                        <h4>Definition:</h4>
                        <p>{result.summary || 'No definition available'}</p>
                    </div>
                </div>
            )}

            <div className="tips">
                <p>💡 Tip: Select any text on a webpage, right-click, and choose "Search with Word Assistant"</p>
            </div>
        </div>
    );
};

export default WordSearch;