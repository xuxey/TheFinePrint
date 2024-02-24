(() => {
    /**
     * Check and set a global guard variable.
     * If this content script is injected into the same page again,
     * it will do nothing next time.
     */
    if (window.hasRun) {
        return;
    }
    window.hasRun = true;

    const anchorLinks = document.querySelectorAll('a');
    const keywords = ['privacy', 'service', 'cookie', 'policy', 'terms'];
    let matches = [];

    anchorLinks.forEach((link) => {
        for (let i = 0; i < keywords.length; i++) {
            if (link.textContent.toLowerCase().includes(keywords[i].toLowerCase())) {
                matches.push(link);
                break;
            }
        }
    });

    const links = matches.map(match => {
        const parsedUrl = new URL(match.href);
        const link = parsedUrl.origin + parsedUrl.pathname
        const text = match.text;
        return { link, text }
    })

    browser.runtime.sendMessage({ foundLinks: links, pageText: document.body.innerText })
})();
