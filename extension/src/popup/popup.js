chrome.storage.local.get(['selectedWord'], (result) => {
    if (result.selectedWord) {
        const word = result.selectedWord.trim();
        
        // Передаём слово в React-приложение
        chrome.storage.local.set({ 
            autoSearchWord: word 
        }, () => {
            // Очищаем original selectedWord
            chrome.storage.local.remove('selectedWord');
        });
    }
});

// Если нужно — можно добавить небольшую задержку для React
setTimeout(() => {
    chrome.storage.local.get(['autoSearchWord'], (res) => {
        if (res.autoSearchWord) {
            console.log('Auto search word received:', res.autoSearchWord);
        }
    });
}, 500);