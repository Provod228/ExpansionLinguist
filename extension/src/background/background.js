chrome.runtime.onInstalled.addListener(() => {
    console.log('Extension installed');

    chrome.contextMenus.create({
        id: 'searchWord',
        title: 'Search "%s"',
        contexts: ['selection']
    });
});

chrome.contextMenus.onClicked.addListener((info, tab) => {
    if (info.menuItemId === 'searchWord') {
        chrome.storage.local.set({ selectedWord: info.selectionText });
        chrome.action.openPopup();
    }
});