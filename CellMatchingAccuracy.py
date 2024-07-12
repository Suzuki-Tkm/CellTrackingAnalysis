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