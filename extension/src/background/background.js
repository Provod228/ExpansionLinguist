chrome.runtime.onInstalled.addListener(() => {
    console.log("Word Assistant installed");
    chrome.contextMenus.create({
        id: "searchWord",
        title: 'Search "%s" with Word Assistant',
        contexts: ["selection"]
    });
});

chrome.contextMenus.onClicked.addListener((info, tab) => {
    if (info.menuItemId === "searchWord" && info.selectionText) {
        const word = info.selectionText.trim();
        

        chrome.storage.local.set({ autoSearchWord: word }, () => {
            chrome.action.openPopup();
        });
    }
});


chrome.action.onClicked.addListener(() => {
    chrome.action.openPopup();
});