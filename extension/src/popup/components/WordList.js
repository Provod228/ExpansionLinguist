import React, { useState, useEffect } from 'react';
import './WordList.css';

const WordList = ({ apiUrl, token }) => {
    const [words, setWords] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');

    useEffect(() => {
        fetchWords();
    }, []);

    const fetchWords = async () => {
        setLoading(true);
        try {
            const response = await fetch(`${apiUrl}/words/note-list`, {
                headers: {
                    'Authorization': `Bearer ${token}`,
                },
            });

            if (!response.ok) {
                throw new Error('Failed to fetch words');
            }

            const data = await response.json();
            setWords(data);
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    const deleteWord = async (wordId) => {
        if (!confirm('Remove this word from your notes?')) return;

        try {
            const response = await fetch(`${apiUrl}/words/delete/${wordId}`, {
                method: 'DELETE',
                headers: {
                    'Authorization': `Bearer ${token}`,
                },
            });

            if (!response.ok) {
                throw new Error('Failed to delete word');
            }

            setWords(words.filter(w => w.id !== wordId));
        } catch (err) {
            setError(err.message);
        }
    };

    if (loading) {
        return <div className="loading">Loading your words...</div>;
    }

    if (error) {
        return <div className="error-message">{error}</div>;
    }

    if (words.length === 0) {
        return (
            <div className="empty-state">
                <p>📖 No words saved yet</p>
                <p className="hint">Search for words and add them to your collection!</p>
            </div>
        );
    }

    return (
        <div className="word-list">
            <div className="word-count">
                📚 {words.length} word{words.length !== 1 ? 's' : ''} saved
            </div>
            <div className="words-grid">
                {words.map((word) => (
                    <div key={word.id} className="word-card">
                        <div className="word-card-header">
                            <h3>{word.word}</h3>
                            <button
                                onClick={() => deleteWord(word.id)}
                                className="delete-btn"
                                title="Remove from notes"
                            >
                                🗑️
                            </button>
                        </div>
                        <p className="word-definition">{word.summary || 'No definition'}</p>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default WordList;