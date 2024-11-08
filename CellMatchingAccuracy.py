import pandas as pd
import numpy as np
import csv
from scipy.optimize import linear_sum_assignment

AnsData = pd.read_csv('/Users/apple/研究/data/小田切先生研究データ/120_slowCellData.csv')
MyData = pd.read_csv('/Users/apple/研究/CellTrackingAnalysis/data/120-slow-big/T0.csv')
output = "data/120-slow-big/T0_frame.csv"
Ans_matching = []
My_matching = []

cells = 288
t = 0.1

AnsDf = AnsData[AnsData['Time']==0]
MyDf = MyData[MyData['POSITION_T']==0.0]

#両データフレームの誤差
#基準をansデータに設定
AnsDf['distance_from_origin'] = np.sqrt(AnsDf['Gx']**2 + AnsDf['Gy']**2)
MyDf['distance_from_origin'] = np.sqrt(MyDf['POSITION_X']**2 + MyDf['POSITION_Y']**2)

# x座標でソートしてから、y座標でソート
AnsDf_sorted = AnsDf.sort_values(by=['Gx', 'Gy'])

# 1番目と2番目に小さい座標を取得
AnsDf_closest_y1 = AnsDf_sorted.iloc[0]
AnsDf_closest_y2 = AnsDf_sorted.iloc[1]

MyDf_sorted = MyDf.sort_values(by='distance_from_origin')
MyDf_sorted = MyDf_sorted[:2]
MyDf_sorted = MyDf_sorted.sort_values(by=['POSITION_X', 'POSITION_Y'])
MyDf_closest_y1 = MyDf_sorted.iloc[0]
MyDf_closest_y2 = MyDf_sorted.iloc[1]

# print(AnsDf_closest_y1)
# print(AnsDf_closest_y2)

# print(MyDf_closest_y1)
# print(MyDf_closest_y2)
# 差分を計算
AnsDf_diff_Y = AnsDf_closest_y2['Gy'] - AnsDf_closest_y1['Gy']
MyDf_diff_Y = MyDf_closest_y2['POSITION_Y'] - MyDf_closest_y1['POSITION_Y']

# print(AnsDf_diff_Y)
# print(MyDf_diff_Y)
scale_factor_y =  MyDf_diff_Y / AnsDf_diff_Y

print("---------------F(s)=",scale_factor_y,"---------------")

#mydfをn倍
MyDf['POSITION_X'] = MyDf['POSITION_X'] / scale_factor_y
MyDf['POSITION_Y'] = MyDf['POSITION_Y'] / scale_factor_y
MyDf['AREA'] = MyDf['AREA'] / (scale_factor_y * scale_factor_y)

print(MyDf)

# 最短経路
def euclidean_distance_matrix(A, B):
    A = np.array(A)
    B = np.array(B)
    return np.linalg.norm(A[:, np.newaxis] - B, axis=2)

coords_Ans = AnsDf[['Gx', 'Gy']].values
coords_My = MyDf[['POSITION_X', 'POSITION_Y']].values

distance_matrix = np.linalg.norm(coords_Ans[:, np.newaxis] - coords_My, axis=2)

row_ind, col_ind = linear_sum_assignment(distance_matrix)

for i, j in zip(row_ind, col_ind):
    Ans_matching.append(AnsDf['ID'].iloc[i])
    My_matching.append(MyDf['ID'].iloc[j])

Ans_my_matching = {index: value for index, value in zip(My_matching,Ans_matching)}

# print(Ans_matching)
# print(My_matching)

########################解析########################

#idの変更
MyData['ID'] = MyData['ID'].map(Ans_my_matching)
print(MyData)

#myDataをn倍
MyData['POSITION_X'] = MyData['POSITION_X'] / scale_factor_y
MyData['POSITION_Y'] = MyData['POSITION_Y'] / scale_factor_y
MyData['PERIMETER'] = MyData['PERIMETER'] / scale_factor_y
MyData['AREA'] = MyData['AREA'] / (scale_factor_y * scale_factor_y)

#ユニークなIDを付与
for index, row in MyData.iterrows():
    IDMagnification = cells * (int(row['POSITION_T']) + 1) + row['ID']
    MyData.at[index, 'unique_id'] = int(IDMagnification)

for index, row in AnsData.iterrows():
    IDMagnification = cells * (row['Time'] + 1) + row['ID']
    AnsData.at[index, 'unique_id'] = int(IDMagnification)

# print(AnsData)
# print(MyData)
#dfのリネーム
MyData = MyData.rename(columns={'POSITION_X': 'Gx', 'POSITION_Y': 'Gy', 'AREA': 'Size' ,'POSITION_T': 'Time', 'PERIMETER' : 'Len'})
print("----------------------")
print(MyData)
# df1とdf2のマッチング計算
def calculate_matching_with_percentage_tolerance(df1, df2, key_column, columns_to_compare, tolerance_dict):
    # 共通のIDを取得
    common_ids = set(df1[key_column].unique()).intersection(set(df2[key_column].unique()))
    
    matching = {}
    
    # 各カラムごとにマッチングを計算
    for column in columns_to_compare:
        if column in df1.columns and column in df2.columns:
            match_count = 0
            total_rows = 0
            tolerance = tolerance_dict.get(column, 0)
            
            # 各共通IDごとにフィルタリングして比較
            for id_value in common_ids:
                df1_filtered = df1[df1[key_column] == id_value]
                df2_filtered = df2[df2[key_column] == id_value]
                
                if not df1_filtered.empty and not df2_filtered.empty:
                    total_rows += 1
                    value1 = df1_filtered[column].values[0]
                    value2 = df2_filtered[column].values[0]
                    
                    # 割合誤差の範囲で比較
                    if (1.0 - tolerance) <= (value1 / value2) <= (1.0 + tolerance):
                        match_count += 1
            matching[column] = match_count / total_rows if total_rows > 0 else 0.0
    
    return matching

# df1とdf2のフレームごとのマッチング計算
def calculate_matching_ratio(data1, data2, output_file , c):
    df1 = data1
    df2 = data2

    max_error = (df1[c] - df2[c]).abs().max()

    average1 = df1.groupby("Time")[c].mean()
    average2 = df2.groupby("Time")[c].mean()

    diff = (average1 - average2).abs()

    ratio = 1 - (diff / max_error)

    result = ratio.reset_index()
    result.columns = ["Time", "マッチング割合"]
    result.to_csv(output_file, index=False)

def count_condition_met(df1, df2, tolerance=t, output_file='result.csv'):
    merged_df = pd.merge(df1, df2, on=['unique_id', 'Time'], suffixes=('_1', '_2'))

    merged_df['条件を満たす'] = merged_df.apply(
        lambda row: (1.0 - tolerance) <= (row['Size_1'] / row['Size_2']) <= (1.0 + tolerance), axis=1)

    count_by_t = merged_df.groupby('Time')['条件を満たす'].sum()

    result = count_by_t / 288

    result.to_csv(output_file, header=['カウント_288で割る'])

    return result

key_column = 'unique_id'
columns_to_compare = ['Size']
tolerance_dict = {'Size': t}

matching_result = calculate_matching_with_percentage_tolerance(MyData, AnsData, key_column, columns_to_compare, tolerance_dict)
print(matching_result)

result = count_condition_met(MyData, AnsData, tolerance=t , output_file=output)