import pandas as pd

# Table1とTable2のデータを準備
data1 = {
    "Id": [1, 2, 3, 4],
    "t": [0, 0, 1, 1],
    "値": [5, 4, 2, 2]
}

data2 = {
    "Id": [1, 2, 3, 4],
    "t": [0, 0, 1, 1],
    "値": [4, 3, 3, 3]
}

# DataFrameに変換
df1 = pd.DataFrame(data1)
df2 = pd.DataFrame(data2)

# 最大誤差の計算
max_error = (df1["値"] - df2["値"]).abs().max()

# 時間ごとの平均値の計算
average1 = df1.groupby("t")["値"].mean()
average2 = df2.groupby("t")["値"].mean()

print(average2)

# 差分の計算
diff = (average1 - average2).abs()

# 割合の計算
ratio = diff / max_error

# 結果をCSVに出力
result = ratio.reset_index()
result.columns = ["t", "マッチング割合"]
result.to_csv("matching_ratio.csv", index=False)

# print(result)
