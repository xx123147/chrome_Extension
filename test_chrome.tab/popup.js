document.querySelector("#getInfo").addEventListener("click",async ()=>{
    const [tab] = await chrome.tabs.query({active:true,currentWindow:true});
    console.log("Tab信息：",tab)
    alert( `标题：${tab.title}\nURL:${tab.url}`);
});

document.getElementById("takeScreenshot").addEventListener("click", async () => {
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  const screenshot = await chrome.tabs.captureVisibleTab(tab.windowId, { format: "png" });
  const imgWindow = window.open();
  imgWindow.document.write(`<img src="${screenshot}">`);
});
document.getElementById("detectLang").addEventListener("click", async () => {
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  alert(`Tab语言: ${tab.lang || "未知"}`);
});
document.getElementById("sendMessage").addEventListener("click", async () => {
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  chrome.scripting.executeScript({
    target: { tabId: tab.id },
    func: () => {
      alert("Hello from Extension!");
      return document.title;
    }
  });
});