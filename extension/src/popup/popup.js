const PORT = 6969
// const API_URL = `http://127.0.0.1:${PORT}`
const API_URL = "http://172.22.152.6:6969"
const ACCESS_CODE = 'access_code1'
const POLLING_INTERVAL_MS = 3000

async function success() {
    const paragraph = document.getElementById('found-links');
    browser.storage.local.get('foundLinks').then(
        message => {
            const foundLinks = message.foundLinks
            if (!foundLinks) return;

            foundLinks.forEach(link => {
                const href = link.link;
                const button = document.createElement('button');
                button.classList.add('found-link', 'montserrat-400');
                button.textContent = link.text;
                button.addEventListener('click', createLinkButtonHandler(href, ACCESS_CODE));
                paragraph.appendChild(button);
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

            const backToMenuButton = document.getElementById('back-to-menu');
            backToMenuButton.addEventListener('click', () => {
                document.getElementById('summary-section').classList.add('hidden');
                document.getElementById('links-section').classList.remove('hidden');
            });
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

function createLinkButtonHandler(url, accessCode) {
    return () => {
        fetch(`${API_URL}/summary?${new URLSearchParams({ url, access_code: accessCode })}`)
            // .then(response => response.json())
            .then(data => {
                console.log('Success:', data);
            })
            .catch(error => {
                console.error('Error:', error);
            });
    }
}

function createThisPageButtonHandler(url, accessCode, pageText) {
    return () => {
        function pollRequest() {
            // Make a GET request
            fetch(`${API_URL}/summary?${new URLSearchParams({ url, access_code: accessCode })}`)
                .then(response => {
                    if (response.status === 200) {
                        response.text().then(
                            text => document.getElementById('gpt-output').innerText = text
                        )
                    } else if (response.status == 201) {
                        console.log(`Request failed, retrying in ${POLLING_INTERVAL_MS}ms:`, response.status);
                        setTimeout(pollRequest, POLLING_INTERVAL_MS);
                    } else {
                        console.error('Got Status:', response.status);
                        document.getElementById('gpt-output').innerText = `Failed with status: ${response.status} ${response.statusText}`
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                });
        }

        fetch(`${API_URL}/summarise?${new URLSearchParams({ url, access_code: accessCode })}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'text/plain'
            },
            body: pageText
        })
            .then(data => {
                console.log('Success:', data);
                document.getElementById('links-section').classList.add(['hidden'])
                document.getElementById('summary-section').classList.remove(['hidden'])
                document.getElementById('gpt-output').innerText = 'loading...'
                setTimeout(pollRequest, POLLING_INTERVAL_MS);
            })
            .catch(error => {
                console.error('Error:', error);
            });
    }
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
