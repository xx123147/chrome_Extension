import json


# cookies = json.load(r'cookies.json')
# print(cookies)

# with open(r'cookies.json', 'r', encoding='utf-8') as f:
#     print(f)
#     cookies = json.load()
#     print(type(cookies))
#     print(cookies[0])

import pandas as pd
f = pd.read_excel(r"C:\Users\Administrator\Desktop\上新\ASIN\10.14.xlsx",header=None)
# print(f.head())
asins = f[0].iloc[180:];
print(asins.head())