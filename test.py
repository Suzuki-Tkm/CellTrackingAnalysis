import pandas as pd

# サンプルデータの作成
df1 = pd.DataFrame({
    'ID': [1, 2, 3, 4],
    'Name': ['Alice', 'Bob', 'Charlie', 'David'],
    'Age': [25, 30, 35, 40]
})

df2 = pd.DataFrame({
    'ID': [1, 2, 3, 4],
    'Name': ['Alice', 'Bob', 'Charlie', 'Edward'],
    'Age': [25, 30, 35, 45]
})

# カラムのマッチング度合いを計算する関数
def calculate_matching(df1, df2, key_column):
    merged_df = pd.merge(df1, df2, on=key_column, how='inner', suffixes=('_df1', '_df2'))
    total_rows = len(merged_df)
    
    matching = {}
    for column in df1.columns:
        if column != key_column:
            match_count = (merged_df[f'{column}_df1'] == merged_df[f'{column}_df2']).sum()
            matching[column] = match_count / total_rows if total_rows > 0 else 0.0
    
    return matching

# IDカラムをキーにして一致率を計算
key_column = 'ID'
matching_result = calculate_matching(df1, df2, key_column)

print(matching_result)
