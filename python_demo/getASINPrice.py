# import pandas as pd
# import requests
# from lxml import etree
#
# path=r"C:\Users\Administrator\Desktop\asins_mesg (2).csv"
# df = pd.read_csv(path)
# asins = df['ASIN']
# # print(len(asins))
# base_url  = r"https://www.amazon.co.uk/gp/product/"
# url = base_url + asins[0]
# # url = r"https://www.amazon.co.uk/gp/product/B0FLWGN5X7"
# headers = {
#     "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36",
#     "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
#     "Accept-Language":"en-GB,en;q=0.9",
#     "Accept-Encoding": "gzip, deflate, br",
#     "Referer": "https://www.amazon.co.uk/",
# }
# response = requests.get(url,headers=headers)
# # print(response.text)
# tree = etree.HTML(response.text)
# # print(tree)
# seller_list = tree.xpath('//*[@id="sellerProfileTriggerId"]')
# # price_list = tree.xpath('//*[@id="corePriceDisplay_desktop_feature_div"]/div[1]/span[1]')
# price_list = tree.xpath('//*[@id="corePrice_feature_div"]/div/div/span[1]/span[1]')
# seller_name = seller_list[0].text if len(seller_list) > 0 else None
# price = price_list[0].text if len(price_list) > 0 else None
# # print(seller_name)
# # print(price)
# # print(df.hed())
import pandas as pd
import requests
from lxml import etree
import time

# 1. 读取 CSV
path = r"C:\Users\Administrator\Desktop\asins_mesg (2).csv"
df = pd.read_csv(path)
asins = df['ASIN']


# 2. 定义抓取函数
def fetch_amazon_info(asin):
    base_url = "https://www.amazon.co.uk/gp/product/"
    url = base_url + str(asin)

    headers = {
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36",
        "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Language":"en-GB,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Referer": "https://www.amazon.co.uk/",
    }
    cookies = {
        "session-id": "259-4362666-6775734",
        "ubid-acbuk": "2593145516-5774178-",
        "session-token": "HkaqYFNPWD3/ltTacgSnV4mMPEY55ATnmP4zm2LtzSKaq1EOZm2Dqo/EYES3+7c60i9xr3QKsDwbWmegP90Mcxahi3DKuFJmR+wKVXBby8gvqDX8X3Kg2VFmdH+6DVxf7y1592r/c2VJnWbsINyS2XEwM/fzkIw1ScFM2lxNNs/1Gt3Zfi//68C63fIkc+GPkaBBhsDwNWdigEkz7pLhGUSNfliV370m7JU6GBsutl7CQKhbCQV3dF7VqgOjSQ08cjwrk5s1ScEYVjXQO+QArqCc2S5vzBG6T+oV27q6CnhZfGdU8m35VHBGQoOFr6/H010G2Gp4Pb1I9363pc0t3/SCZjOoK+ftHJkrIecazXM=",
        "i18n-prefs": "GBP",
        "lc-acbuk": "en_GB",

        # 可以加上其他你觉得必要的 Cookie
    }



    try:
        response = requests.get(url, headers=headers, timeout=10,cookies=cookies)
        tree = etree.HTML(response.text)

        seller_elem = tree.xpath('//*[@id="sellerProfileTriggerId"]')
        title = seller_elem[0].text.strip() if seller_elem else None

        price_elem = tree.xpath('//*[@id="corePrice_feature_div"]/div/div/span[1]/span[1]')
        price = price_elem[0].text.strip() if price_elem else None

        return title, price
    except Exception as e:
        print(f"抓取 {asin} 出错:", e)
        return None, None


# 3. 遍历 ASIN 并填充新的列
sellers = []
prices = []
links = []

for asin in asins:
    title, price = fetch_amazon_info(asin)
    sellers.append(title)
    prices.append(price)
    links.append(f"https://www.amazon.co.uk/gp/product/{asin}")
    time.sleep(1)  # 避免被封 IP

# 4. 添加到原 DataFrame
df['seller'] = sellers
df['Price'] = prices
df['Link'] = links

# 5. 保存回原 Excel（覆盖原文件）
df.to_csv(path, index=False)

print("抓取完成，原 Excel 已更新。")
