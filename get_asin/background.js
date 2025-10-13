// background.js
//chrome Extension的事件机制，当我在某一个tab中点击icon,chrome会自动触发点击事件，并且告诉我是在哪个tab中点击的
chrome.action.onClicked.addListener((tab) => {
  if (!tab || !tab.id) return;
  chrome.tabs.sendMessage(tab.id, { action: 'open_first' }, (response) => {
    if (chrome.runtime.lastError) {
      // content script 可能还没注入 —— 注入后再发一次消息
      chrome.scripting.executeScript({
        target: { tabId: tab.id },
        files: ['content_script.js']
      }).then(() => {
        chrome.tabs.sendMessage(tab.id, { action: 'open_first' });
      }).catch(err => {
        console.error('注入 content_script 失败:', err);
      });
    } else {
      console.log('content script 返回:', response);
    }
  });
});
