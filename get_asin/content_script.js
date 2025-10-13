// // content_script.js
// (() => {
//   console.log('[ASIN opener] content script loaded');

//   function clickElement(el) {
//     if (!el) return false;
//     try {
//       el.scrollIntoView({ behavior: "smooth", block: "center" });
//       el.dispatchEvent(new MouseEvent("mouseover", { bubbles: true }));
//       el.dispatchEvent(new MouseEvent("mousedown", { bubbles: true }));
//       el.dispatchEvent(new MouseEvent("mouseup", { bubbles: true }));
//       el.dispatchEvent(new MouseEvent("click", { bubbles: true }));
//       console.log("[ASIN opener] clicked:", el);
//       return true;
//     } catch (err) {
//       console.error("Click failed:", err);
//       return false;
//     }
//   }

//   function highlight(el) {
//     if (!el) return;
//     const oldOutline = el.style.outline;
//     el.style.outline = "3px solid #ff8c00";
//     setTimeout(() => (el.style.outline = oldOutline), 2000);
//   }

//   function openFirstResult() {
//     // 查找所有结果项的容器
//     const items = document.querySelectorAll("div.b9A9vAhPI9A4Qwi53T89");
//     if (!items.length) {
//       console.warn("[ASIN opener] no list items found");
//       return { ok: false, reason: "no-items" };
//     }

//     const first = items[0];
//     highlight(first);

//     const ok = clickElement(first);
//     if (ok) {
//       return { ok: true, reason: "clicked-first-item" };
//     }
//     return { ok: false, reason: "click-failed" };
//   }

//   chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
//     if (msg.action === "open_first") {
//       const result = openFirstResult();
//       sendResponse(result);
//     }
//   });

//   // 方便在控制台手动调试
//   window.__asinOpener_openFirst = openFirstResult;
// })();

(() => {
  console.log("[ASIN Scraper] content script loaded");

  const wait = (ms) => new Promise((res) => setTimeout(res, ms));

  // ===== 点击和高亮工具函数 =====
  function clickElement(el) {
    if (!el) return false;
    try {
      el.scrollIntoView({ behavior: "smooth", block: "center" });
      el.dispatchEvent(new MouseEvent("mouseover", { bubbles: true }));
      el.dispatchEvent(new MouseEvent("mousedown", { bubbles: true }));
      el.dispatchEvent(new MouseEvent("mouseup", { bubbles: true }));
      el.dispatchEvent(new MouseEvent("click", { bubbles: true }));
      return true;
    } catch (err) {
      console.error("Click failed:", err);
      return false;
    }
  }

  function highlight(el) {
    if (!el) return;
    const oldOutline = el.style.outline;
    el.style.outline = "3px solid #00cc66";
    setTimeout(() => (el.style.outline = oldOutline), 1000);
  }

  // ===== ASIN 提取函数 =====
  function extractASINFromPage() {
    const span1 = document.querySelector("#search-results-panel > div.uR5H99PpPykrzLz130Dc > div.yHp1x76T8dejVA7HzZnW > div > div.WfeKoekShvVAvyStBN7x > div.GjaIyfwFzGkX5L3wv0zI > span:nth-child(1)");
    const span2 = document.querySelector("#search-results-panel > div.uR5H99PpPykrzLz130Dc > div.yHp1x76T8dejVA7HzZnW > div > div.WfeKoekShvVAvyStBN7x > div.GjaIyfwFzGkX5L3wv0zI > kat-link[label]")
    if (!span1 && !span2) return null;

    const asin = span1.innerText.trim();
    const mesg = span2.getAttribute("label").trim();
    // const match = text.match(/ASIN[:：]?\s*([A-Z0-9]{8,12})/i);
    // if (match) return match[1].toUpperCase();
    return [asin,mesg]
    }

  async function waitForASIN(timeout = 5000) {
    const start = Date.now();
    let asin = null;
    let mesg = null;
    while (Date.now() - start < timeout) {
      try{
        [asin,mesg] = extractASINFromPage();
        if (asin&&mesg) return [asin,mesg];
        await wait(300);
      }
      catch (error){
        console.error("提取信息时出错：",error)
      }

    }
      console.warn("超时未提取到任何信息")
      return [asin,mesg]
  }

  // ===== 主抓取逻辑 =====
  async function scrapeAllASINs() {
    let items = document.querySelectorAll("div.b9A9vAhPI9A4Qwi53T89");
    if (!items.length) {
      alert("未找到任何商品条目，请确认页面加载完成。");
      return;
    }

    const results = [];

    for (let i = 0; i < items.length; i++) {
      // 重新获取列表，防止 DOM 更新导致元素失效
      items = document.querySelectorAll("div.b9A9vAhPI9A4Qwi53T89");
      const item = items[i];
      if (!item) continue;

      console.log(`👉 点击第 ${i + 1}/${items.length} 项...`);
      highlight(item);
      clickElement(item);

      // 等待详情页加载
      await wait(1500);

      // 获取 ASIN
      const [asin,mesg] = await waitForASIN(6000);
      if (asin&&mesg) {
        console.log(`✅ 第 ${i + 1} 项 ASIN 和 MESG:`, asin,mesg);
        data = {ASIN:asin,MESG:mesg}
        results.push({ index: i + 1, data });
      } else {
        console.warn(`⚠️ 第 ${i + 1} 项未检测到 ASIN 和 MESG`);
        if (asin || mesg) {
          results.push({
            index: i + 1,
            data: {
              ASIN: asin || '未获取',
              MESG: mesg || '未获取'
            },
            incomplete: true
            });
    }
      }

      // 点击返回按钮回列表页
      const backBtn = document.querySelector("div[slot='header'] kat-icon[name='keyboard_arrow_left']");
      if (backBtn) {
        clickElement(backBtn);
        await wait(1500); // 等待列表页加载
      } else {
        console.warn("⚠️ 返回按钮未找到，可能页面结构变化");
        break;
      }
    }

    console.log("✅ 抓取完成，共获取", results.length, "条 数据");
    console.table(results);

    // // 导出 CSV
    // const csv = "index,ASIN\n" + results.map(r => `${r.index},${r.asin}`).join("\n");
    // const blob = new Blob([csv], { type: "text/csv" });
    // const url = URL.createObjectURL(blob);
    // const a = document.createElement("a");
    // a.href = url;
    // a.download = "asins.csv";
    // a.click();
    // URL.revokeObjectURL(url);

    // alert("✅ 已完成抓取并下载 asins.csv");
    // 导出 CSV
    const csv = "index,ASIN,MESG\n" + 
        results.map(r => `${r.index},${r.data.ASIN},${r.data.MESG}`).join("\n");

    const blob = new Blob([csv], { type: "text/csv" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "asins_mesg.csv";
    a.click();
    URL.revokeObjectURL(url);

    alert("✅ 已完成抓取并下载 asins_mesg.csv");
  }

  // ===== 接收扩展消息 =====
  chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
    if (msg.action === "open_first") {
      scrapeAllASINs();
      sendResponse({ ok: true });
    }
  });

  // 控制台手动调用接口
  window.__asinScraper_run = scrapeAllASINs;
})();
