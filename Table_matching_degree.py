import pandas as pd

def calc_matching_rate(table1, table2, threshold=0.1):
  """
  2つのテーブルのマッチング率を計算し、timeごとに詳細な分析結果を出力します。

  Args:
    table1: リスト形式のテーブル1。各要素は[Id, time, size, Len, x, y]の形式。
    table2: リスト形式のテーブル2。各要素は[Id, time, size, Len, x, y]の形式。
    threshold: 許容される値の差（デフォルトは0.1）。

  Returns:
    全体の一致率、timeごとの一致率、詳細な分析結果を返す。
  """

  # テーブルをDataFrameに変換
  df1 = pd.DataFrame(table1, columns=["Id", "time", "size", "Len", "x", "y"])
  df2 = pd.DataFrame(table2, columns=["Id", "time", "size", "Len", "x", "y"])

  # size、Len、x、yのマッチング度合いを計算
  match_size_len_xy = calc_match_rate_by_columns(df1, df2, ["size", "Len", "x", "y"], threshold=threshold)

  # timeごとの一致率を計算
  match_rate_by_time = {}
  for time in set(df1["time"]):
    # 特定のtimeを持つレコードを取得
    df1_time = df1[df1["time"] == time]
    df2_time = df2[df2["time"] == time]

    # size、Len、x、yのマッチング度合いを計算
    match_rate_time = calc_match_rate_by_columns(df1_time, df2_time, ["size", "Len", "x", "y"], threshold=threshold)

    # timeごとの一致率を保存
    match_rate_by_time[time] = match_rate_time

  # 全体の一致率を計算
  overall_match_rate = sum(match_size_len_xy.values()) / (len(df1) * 4)

  # 分析結果を返す
  return overall_match_rate, match_rate_by_time, match_size_len_xy


def calc_match_rate_by_columns(df1, df2, columns, threshold=0.1):
  """
  指定された列の値が一致または近似一致するレコードの割合を計算します。

  Args:
    df1: DataFrame形式のテーブル1。
    df2: DataFrame形式のテーブル2。
    columns: 比較対象とする列名。
    threshold: 許容される値の差（デフォルトは0.1）。

  Returns:
    各列のマッチング率を辞書形式で返す。
  """

  match_rate = {}
  for col in columns:
    # 一致するレコードの数をカウント
    match_count = sum(
        (df1[col] - df2[col]).abs() <= threshold for i in range(len(df1))
    )

    # マッチング率を計算
    match_rate[col] = match_count / len(df1)

  return match_rate


# テーブルデータ
table1 = [
  [1, 0, 3, 10, 1, 1],
  [2, 0, 2, 2, 2, 3],
  [3, 0, 3, 12, 2, 2],
  [1, 1, 4, 2, 2, 3],
  [2, 1, 3, 12, 2, 2],
  [3, 1, 3, 2, 2, 3],
  [1, 2, 2, 12, 2, 2],
  [2, 2, 4, 2, 2, 3],
  [3, 2, 4, 12, 2, 2],
]

table2 = [
  [1, 0, 4, 10, 1, 1],
  [2, 0, 2, 2, 2, 3],
  [3, 0, 5, 12, 2, 2],
  [1, 1, 6, 2, 2, 3],
  [2, 1, 3, 12, 4, 2],
  [3, 1, 2, 2, 2, 3],
  [1, 2, 2, 11, 2, 2],
  [2, 2, 4, 1, 2, 3],
  [3, 2, 4, 12, 2, 2],
]

# マッチング率を計算
overall_match_rate, match_rate_by_time, match_size_len_xy = calc_matching_rate(table1, table2)

# 結果を出力
print("全体の一致率:", overall_match_rate)
print("timeごとの一致率:")
for time, match_rate in match_rate_by_time.items():
  print(f"  time {time}:", match_rate)
print("size、Len、x、yのマッチング度合い:")
for col, match_rate in match_size_len_xy.items():
  print(f"  {col}:", match_rate)