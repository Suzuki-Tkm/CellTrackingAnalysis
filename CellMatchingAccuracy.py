import pandas as pd
import numpy as np
from scipy.optimize import linear_sum_assignment

AnsData = pd.read_csv('/Users/apple/研究/data/小田切先生研究データ/60-fast/回答データと実験データ - 回答データ.csv')
MyData = pd.read_csv('/Users/apple/研究/CellTrackingAnalysis/data/09:27:40.csv')

Ans_matching = []
My_matching = []

cells = 72

AnsDf = AnsData[AnsData['Time']==0]
MyDf = MyData[MyData['POSITION_T']==0.0]

#両データフレームの誤差
#基準をansデータに設定
AnsDf['distance_from_origin'] = np.sqrt(AnsDf['Gx']**2 + AnsDf['Gy']**2)
MyDf['distance_from_origin'] = np.sqrt(MyDf['POSITION_X']**2 + MyDf['POSITION_Y']**2)

AnsDf_closest_point = AnsDf.loc[AnsDf['distance_from_origin'].idxmax()]
MyDf_closest_point = MyDf.loc[MyDf['distance_from_origin'].idxmax()]
print(AnsDf_closest_point)
print(MyDf_closest_point)

scale_factor_x = MyDf_closest_point['POSITION_X'] / AnsDf_closest_point['Gx']
scale_factor_y = MyDf_closest_point['POSITION_Y'] / AnsDf_closest_point['Gy']

#mydfをn倍
MyDf['POSITION_X'] = MyDf['POSITION_X'] * scale_factor_x
MyDf['POSITION_Y'] = MyDf['POSITION_Y'] * scale_factor_y

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
MyData = MyData.rename(columns={'POSITION_X': 'Gx', 'POSITION_Y': 'Gy', 'AREA': 'Size' ,'POSITION_T': 'Time'})
print("----------------------")
print(MyData)

def calculate_matching_with_tolerance(df1, df2, key_column, columns_to_compare, tolerance_dict):
    common_ids = set(df1[key_column].unique()).intersection(set(df2[key_column].unique()))
    
    matching = {}
    
    for column in columns_to_compare:
        if column in df1.columns and column in df2.columns:
            match_count = 0
            total_rows = 0
            tolerance = tolerance_dict.get(column, 0)
            
            for id_value in common_ids:
                df1_filtered = df1[df1[key_column] == id_value]
                df2_filtered = df2[df2[key_column] == id_value]
                
                if not df1_filtered.empty and not df2_filtered.empty:
                    total_rows += 1
                    if abs(df1_filtered[column].values[0] - df2_filtered[column].values[0]) <= tolerance:
                        match_count += 1
            
            matching[column] = match_count / total_rows if total_rows > 0 else 0.0
    
    return matching

key_column = 'unique_id'
columns_to_compare = ['Size', 'Gx', 'Gy' , 'ID' , 'Time']
tolerance_dict = {'Size': 1500, 'Gx': 10, 'Gy': 10 , 'ID': 0 , 'Time' : 0}

matching_result = calculate_matching_with_tolerance(MyData, AnsData, key_column, columns_to_compare, tolerance_dict)
print(matching_result)