import pandas as pd

# pandas Series 类似列表
series = pd.Series([1, 2, 3, 4, 5])

# pandas DataFrame 类似字典（列名→Series）
df = pd.DataFrame({
    'A': [1, 2, 3],  # 列表 → Series
    'B': ['x', 'y', 'z']
})

# 可以使用字典方法操作
print(df.columns)  # 转换为列表