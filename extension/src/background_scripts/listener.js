

function updateLinks(message) {
    browser.storage.local.set({ foundLinks: message.foundLinks, pageText: message.pageText })
}

browser.runtime.onMessage.addListener(updateLinks);