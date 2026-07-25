
document.addEventListener("DOMContentLoaded", () => {
  const resultEl = document.getElementById("result");
  const contentEl = document.getElementById("result-content");
  const statusEl = document.getElementById("status");
  const labelEl = document.getElementById("result-label");
  const closeBtn = document.getElementById("btn-close");

  function showResult(label, text) {
    labelEl.textContent = label;
    contentEl.textContent = text;
    resultEl.classList.remove("hidden");
    statusEl.textContent = "Done";
  }

  function setLoading(label) {
    labelEl.textContent = label;
    contentEl.textContent = "Processing...";
    resultEl.classList.remove("hidden");
    statusEl.textContent = "Working...";
  }

  closeBtn.addEventListener("click", () => {
    resultEl.classList.add("hidden");
  });

  document.getElementById("btn-summarize").addEventListener("click", async () => {
    setLoading("Summary");
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    chrome.tabs.sendMessage(tab.id, { action: "extractText" }, (response) => {
      if (response && response.text) {
        const lines = response.text.split("\\n").filter(l => l.trim()).slice(0, 30).join("\\n");
        showResult("Summary", `[Page Text Extracted]\\n\\n${lines}\\n\\n---\\nSend to API for summarization.`);
      } else {
        showResult("Summary", "Could not extract page text.");
      }
    });
  });

  document.getElementById("btn-translate").addEventListener("click", async () => {
    setLoading("Translation");
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    chrome.tabs.sendMessage(tab.id, { action: "extractText" }, (response) => {
      if (response && response.text) {
        const lines = response.text.split("\\n").filter(l => l.trim()).slice(0, 10).join("\\n");
        showResult("Translation (EN->ZH)", `[To translate]\\n\\n${lines}\\n\\n---\\nConnect to AgentForge API for real translation.`);
      } else {
        showResult("Translation", "Could not extract page text.");
      }
    });
  });

  document.getElementById("btn-extract").addEventListener("click", async () => {
    setLoading("Extracted Text");
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    chrome.tabs.sendMessage(tab.id, { action: "extractText" }, (response) => {
      if (response && response.text) {
        showResult("Page Text", response.text.slice(0, 2000));
      } else {
        showResult("Page Text", "Could not extract text. Try reloading the page.");
      }
    });
  });
});
