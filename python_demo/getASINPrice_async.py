import asyncio
import json

import aiohttp
import pandas as pd
from lxml import etree

# 读取asin
asin_path = r"C:\Users\Administrator\Desktop\test.xlsx"
df = pd.read_excel(asin_path,header=None)
asinsList = df[0]   # series类型
# cookies
cookies_path = r"cookies.json"
with open(cookies_path, 'r', encoding='utf-8') as f:
    cookiesList = json.load(f)
cookies = {c["name"]:c["value"] for c in cookiesList}

#headers
headers = {
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36",
        "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Language":"en-GB,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Referer": "https://www.amazon.co.uk/",
}

#抓取函数
async def get_asin_price_async(session,asin):
    url = f"https://www.amazon.co.uk/gp/product/{asin}"
    try:
        async with session.get(url) as response:
            html = await response.text()
            root = etree.HTML(html)
            seller_elem=root.xpath('//*[@id="sellerProfileTriggerId"]')
            seller = seller_elem[0].text.strip() if seller_elem else None
            price_elem = root.xpath('//*[@id="corePrice_feature_div"]/div/div/span[1]/span[1]')
            price = price_elem[0].text.strip() if price_elem else None
            return asin,seller, price
    except Exception as e:
        print(f"抓取 {asin}数据 出错:", e)
        return None, None

#主异步流程
async def main():
    results = []
    connector = aiohttp.TCPConnector(limit=20, ssl=False)
    async with aiohttp.ClientSession(connector=connector,headers=headers, cookies=cookies) as session:
        tasks = [get_asin_price_async(session,asin) for asin in asinsList]
        for f in asyncio.as_completed(tasks):  # 边抓边处理
            asin, seller, price = await f
            print(f"完成: {asin} | {seller} | {price}")
            results.append((asin, seller, price))
    return results

        # for asin in asinsList:
        #     seller,price = await get_asin_price_async(session,asin)
        #     sellers.append(seller)
        #     prices.append(price)


# 运行
if __name__=="__main__":
    results=asyncio.run(main())
    out_df = pd.DataFrame(results, columns=["ASIN", "Title", "Price"])
    out_df.to_excel(asin_path, index=False)
    print(f"\n✅ 抓取完成，共 {len(results)} 个商品。结果已保存到：{asin_path}")


# import asyncio
# import aiohttp
# import pandas as pd
# import json
# from lxml import html
#
# # === 配置部分 ===
# COOKIES_FILE = r"C:\Users\Administrator\Desktop\amazon_cookies.json"
# ASIN_FILE = r"C:\Users\Administrator\Desktop\asins_mesg (2).csv"
# OUTPUT_FILE = r"C:\Users\Administrator\Desktop\asins_mesg_out.xlsx"
#
# # === 加载 cookies ===
# with open(COOKIES_FILE, "r", encoding="utf-8") as f:
#     cookies_list = json.load(f)
# cookies = {c["name"]: c["value"] for c in cookies_list}
#
# # === 加载 ASIN ===
# df = pd.read_csv(ASIN_FILE)
# asins = df["ASIN"].dropna().tolist()
#
# # === 请求头 ===
# HEADERS = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
#                   "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
#     "Accept-Language": "en-GB,en;q=0.9",
# }
#
# # === 抓取函数 ===
# async def fetch(session, asin):
#     url = f"https://www.amazon.co.uk/dp/{asin}"
#     try:
#         async with session.get(url, timeout=15) as resp:
#             if resp.status != 200:
#                 return asin, None, None
#             text = await resp.text()
#             tree = html.fromstring(text)
#
#             # 解析标题和价格
#             title = tree.xpath('normalize-space(//span[@id="productTitle"]/text())')
#             price = tree.xpath('normalize-space(//span[@class="a-price-whole"]/text())')
#
#             return asin, title or None, price or None
#     except Exception as e:
#         return asin, None, None
#
# # === 主异步流程 ===
# async def main():
#     results = []
#     connector = aiohttp.TCPConnector(limit=20, ssl=False)  # 并发上限20
#     async with aiohttp.ClientSession(headers=HEADERS, cookies=cookies, connector=connector) as session:
#         tasks = [fetch(session, asin) for asin in asins]
#         for f in asyncio.as_completed(tasks):  # 边抓边处理
#             asin, title, price = await f
#             print(f"完成: {asin} | {title} | {price}")
#             results.append((asin, title, price))
#     return results
#
# # === 运行 ===
# if __name__ == "__main__":
#     results = asyncio.run(main())
#
#     out_df = pd.DataFrame(results, columns=["ASIN", "Title", "Price"])
#     out_df.to_excel(OUTPUT_FILE, index=False)
#     print(f"\n✅ 抓取完成，共 {len(results)} 个商品。结果已保存到：{OUTPUT_FILE}")
#



