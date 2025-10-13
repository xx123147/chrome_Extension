// popup.js
const titleEl = document.getElementById("title");
const urlEl = document.getElementById("url");
const refreshBtn = document.getElementById("refreshBtn");
const copyBtn = document.getElementById("copyBtn");
const msgEl = document.getElementById("msg");

async function getActiveTabInfo() {
  try {
    // 获取当前活动标签页
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    if (!tab) {
      titleEl.textContent = "无法获取当前标签";
      urlEl.textContent = "";
      urlEl.removeAttribute("href");
      return;
    }

    // 在页面上下文执行代码以获取 document.title 和 location.href
    const results = await chrome.scripting.executeScript({
      target: { tabId: tab.id },
      func: () => {
        return {
          title: document.title || "",
          url: location.href || ""
        };
      }
    });

    const result = results && results[0] && results[0].result;
    if (result) {
      titleEl.textContent = result.title || "(无标题)";
      urlEl.textContent = result.url || "(无 URL)";
      urlEl.href = result.url || "#";
    } else {
      titleEl.textContent = tab.title || "(无标题)";
      urlEl.textContent = tab.url || "(无 URL)";
      urlEl.href = tab.url || "#";
    }

    msgEl.textContent = "";
  } catch (err) {
    console.error("getActiveTabInfo error:", err);
    titleEl.textContent = "(错误)";
    urlEl.textContent = "(无法读取 URL)";
    urlEl.href = "#";
    msgEl.textContent = "读取页面信息失败，请确保页面允许脚本执行。";
    msgEl.style.color = "#c33";
  }
}

refreshBtn.addEventListener("click", () => {
  getActiveTabInfo();
  msgEl.textContent = "已刷新";
  msgEl.style.color = "#2a7";
  setTimeout(() => { msgEl.textContent = ""; }, 1200);
});

copyBtn.addEventListener("click", async () => {
  const url = urlEl.getAttribute("href") || "";
  if (!url || url === "#" || url === "null") {
    msgEl.textContent = "无可复制的 URL";
    msgEl.style.color = "#c33";
    return;
  }

  try {
    // 使用 clipboard API（需要用户交互）
    await navigator.clipboard.writeText(url);
    msgEl.textContent = "已复制到剪贴板 ✔";
    msgEl.style.color = "#2a7";
  } catch (e) {
    // 回退方案：在 popup 中临时创建 textarea 复制
    try {
      const textarea = document.createElement("textarea");
      textarea.value = url;
      document.body.appendChild(textarea);
      textarea.select();
      document.execCommand("copy");
      textarea.remove();
      msgEl.textContent = "已复制到剪贴板（回退） ✔";
      msgEl.style.color = "#2a7";
    } catch (err) {
      console.error("复制失败：", err);
      msgEl.textContent = "复制失败，请手动复制 URL";
      msgEl.style.color = "#c33";
    }
  }

  setTimeout(() => { msgEl.textContent = ""; }, 1600);
});

// 首次加载时获取信息
getActiveTabInfo();
