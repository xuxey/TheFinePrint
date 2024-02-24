
function success() {
    console.log('succ')
}

function reportExecuteScriptError(error) {
    document.querySelector("#popup-content").classList.add("hidden");
    document.querySelector("#error-content").classList.remove("hidden");
    console.error(`Failed to execute beastify content script: ${error.message}`);
}

console.log('got here')

browser.tabs
    .executeScript({ file: "/src/content_scripts/find-links.js" })
    .then(success)
    .catch(reportExecuteScriptError);