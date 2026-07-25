
// AgentForge content script - extracts page text
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === "extractText") {
    const text = extractPageText();
    sendResponse({ text: text });
  }
  return true;
});

function extractPageText() {
  const article = document.querySelector("article");
  if (article) return cleanText(article.innerText);
  const main = document.querySelector("main");
  if (main) return cleanText(main.innerText);
  return cleanText(document.body.innerText);
}

function cleanText(text) {
  return text
    .replace(/\\s+/g, " ")
    .replace(/\\n\\s*\\n/g, "\\n")
    .trim()
    .slice(0, 10000);
}
