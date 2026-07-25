
// AgentForge background service worker
chrome.runtime.onInstalled.addListener(() => {
  console.log("AgentForge extension installed");
});

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === "callApi") {
    callAgentForgeAPI(request.endpoint, request.data)
      .then(result => sendResponse(result))
      .catch(error => sendResponse({ error: error.message }));
    return true;
  }
});

async function callAgentForgeAPI(endpoint, data) {
  const response = await fetch(`http://localhost:8000/${endpoint}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  return await response.json();
}
