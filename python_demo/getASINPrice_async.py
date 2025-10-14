import asyncio
import json

import aiohttp
import pandas as pd
from lxml import etree

# 读取asin
asin_path = r"asin.csv"
df = pd.read_csv(asin_path)
asinsList = df['ASIN']   # series类型
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
        async with session.get(url, headers=headers, cookies=cookies) as response:
            html = await response.text()
            root = etree.HTML(html)
            seller_elem=root.xpath('//*[@id="sellerProfileTriggerId"]')
            seller = seller_elem[0].text.strip() if seller_elem else None
            price_elem = root.xpath('//*[@id="corePrice_feature_div"]/div/div/span[1]/span[1]')
            price = price_elem[0].text.strip() if price_elem else None
            return seller, price
    except Exception as e:
        print(f"抓取 {asin}数据 出错:", e)
        return None, None

#主异步流程
async def main():
    sellers = []
    prices = []
    connector = aiohttp.TCPConnector(limit=20, ssl=False)
    async with aiohttp.ClientSession(connector=connector) as session:
        for asin in asinsList:
            seller,price = await get_asin_price_async(session,asin)
            sellers.append(seller)
            prices.append(price)


# 运行
if __name__=="__main__":
    asyncio.run(main())



