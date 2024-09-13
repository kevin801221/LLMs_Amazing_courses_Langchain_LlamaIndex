import pandas as pd

# 創建示範數據
data = {
    "Name": ["Alice", "Bob", "Charlie", "David", "Eva"],
    "Age": [30, 35, 25, 40, 28],
    "Department": ["HR", "IT", "Marketing", "Finance", "IT"],
    "Salary": [60000, 75000, 50000, 80000, 70000]
}

# 創建 DataFrame
df = pd.DataFrame(data)

# 將 DataFrame 保存為 CSV 文件
df.to_csv("sample_data.csv", index=False)

print("sample_data.csv 已成功創建！")
