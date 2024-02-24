
const API_URL = 'http://127.0.0.1'
const ACCESS_CODE = 'access_code1'

async function success() {
    const paragraph = document.getElementById('found-links');
    browser.storage.local.get('foundLinks').then(
        message => {
            const foundLinks = message.foundLinks
            if (!foundLinks) return;

            foundLinks.forEach(link => {
                const a = document.createElement('button');
                a.href = link.href;
                a.textContent = link.text;
                paragraph.appendChild(a);
                paragraph.appendChild(document.createElement('br'));
            });
        }
    )



    const currentUrl = encodeURI(await getCurrentTabURL());
    browser.storage.local.get('pageText').then(
        message => {
            const pageText = message.pageText;
            if (!pageText) return;

            const thisPageButton = document.getElementById('this-page-button');
            thisPageButton.addEventListener('click', createThisPageButtonHandler(currentUrl, ACCESS_CODE, pageText));
        }
    )

}

async function getCurrentTabURL() {
    const tabs = await browser.tabs.query({ active: true, currentWindow: true });
    const activeTab = tabs[0];
    const parsedUrl = new URL(activeTab.url);
    parsedUrl.search = '';
    return parsedUrl.toString();
}

function createThisPageButtonHandler(url, accessCode, pageText) {
    console.log('thisPageButtonHandler');
    return () =>
        fetch(`${API_URL}/summarise?${new URLSearchParams({ url, accessCode })}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'text/plain'
            },
            body: pageText
        })
            .then(response => response.json())
            .then(data => {
                console.log('Success:', data);
            })
            .catch(error => {
                console.error('Error:', error);
            });
}

function reportExecuteScriptError(error) {
    document.querySelector("#popup-content").classList.add("hidden");
    document.querySelector("#error-content").classList.remove("hidden");
    console.error(`Failed to execute beastify content script: ${error.message}`);
}

browser.tabs
    .executeScript({ file: "/src/content_scripts/find-links.js" })
    .then(success)
    .catch(reportExecuteScriptError);