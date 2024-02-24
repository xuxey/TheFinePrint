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
    const keywords = ['privacy', 'service', 'cookie', 'policy'];
    let matches = [];

    anchorLinks.forEach((link) => {
        for (let i = 0; i < keywords.length; i++) {
            if (link.textContent.toLowerCase().includes(keywords[i].toLowerCase())) {
                matches.push(link);
                break;
            }
        }
    });

    console.log(matches);
    document.getElementById('found-links').innerHTML = matches;
})();
