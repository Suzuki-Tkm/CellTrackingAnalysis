import pandas as pd

# サンプルデータフレームを作成する
data = {'name': ['Alice', 'Bob', 'Charlie'],
        'age': [25, 30, 35]}
df = pd.DataFrame(data)

# 新しいIDをforループで与える
for index, row in df.iterrows():
    # 新しいIDを1から始める場合
    new_id = index + 1
    df.at[index, 'new_id'] = new_id

print(df)
