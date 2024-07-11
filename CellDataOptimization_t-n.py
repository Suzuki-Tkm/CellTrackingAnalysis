import pandas as pd
import math
import numpy as np
from scipy.optimize import linear_sum_assignment
import csv
import datetime

class Cell:
  def __init__(self,id , time):
    self.id = id
    self.time = time
    self.memory = 0

class Cells:
  def __init__(self,cell,id):
    self.list = [cell]
    self.id = id

  def add_cell(self , cell):
    self.list.append(cell)

# print(pd.__version__)

#     # ユークリッド距離を計算
# def euclidean_distance_matrix(A, B):
#     return np.linalg.norm(A[:, np.newaxis] - B, axis=2)

def euclidean_distance_matrix(A, B):
    # PythonのリストをNumPy配列に変換
    A = np.array(A)
    B = np.array(B)
    
    # ユークリッド距離行列を計算
    return np.linalg.norm(A[:, np.newaxis] - B, axis=2)

input = pd.read_csv('/Users/apple/研究/data/小田切先生研究データ/60-fast/回答データと実験データ - 実験データ.csv')

#細胞数
cells = 72

# 距離の上限を設定
distance_threshold = 1  # 例として上限を10に設定

# cellの大きさを指定
cell_size = 0

# 細胞が未発見時の記憶する上限回数
memory_limit = 10

now = datetime.datetime.now()
formatted_time = now.strftime("%H:%M:%S")

df = input[['TRACK_ID','POSITION_X','POSITION_Y','POSITION_T','AREA']] #データの抽出
df = df.drop(df.index[[0,1,2]]) #利用しない行の削除
df = df.apply(pd.to_numeric, errors='coerce') #データの数値化
df = df.sort_values(by=['POSITION_T','TRACK_ID']) #ソート

#細胞データを作成（分裂しないと仮定し、細胞数を72に固定.keyをid、valueを実験データid）
use_cells_Fixed_value = list(df[df['POSITION_T']==0]['TRACK_ID'])
# cells_Fixed_value = {i+1: use_cells_Fixed_value[i] for i in range(0, cells)}
# cells_Fixed_value = {use_cells_Fixed_value[i]: [use_cells_Fixed_value[i]] for i in range(0, cells)}
cells_Fixed_value = {use_cells_Fixed_value[i]: Cells(Cell(use_cells_Fixed_value[i] , 0) , i) for i in range(0, cells)}
ret_cells_Fixed_value = []

# 確認用
# cnt = 0 
# for i in df['POSITION_T']:
#   if i == 0:
#     cnt += 1
# print(cnt)

# print(df['POSITION_T'].max())

for t in range(df['POSITION_T'].max()):
  print("-------- time ",t," --------")
  print("解析中の細胞数：",len(list(cells_Fixed_value.keys())))
  if len(list(cells_Fixed_value.keys())) == 0:
    break
  df_temp = df[df['POSITION_T'] == t]
  cells_temp = df_temp.shape[0]
  print("現フレームの細胞数:",cells_temp)
  decID = list(cells_Fixed_value.keys()) #使われているかの判定用
  incID = []
  # print(cells_Fixed_value.values())
  for i in range(cells_temp):
    cell = df_temp[i:i+1]
    id = cell['TRACK_ID'].iloc[-1]
    # print(df_temp)
    if id in list(cells_Fixed_value.keys()):
      # print("正常")
      cells_Fixed_value[id].list[-1].time = t
      decID.remove(id)
    else:
      # print("異常個体id",id)
      incID.append(id)
  print("消えた細胞")
  print(decID)
  print("増えた細胞")
  print(incID)

  if t!=0:
    # print("---------減---------")
    decPoint = []
    incPoint = []

    for i in decID:
      temp_cell = cells_Fixed_value[i].list[-1]
      # print(temp_cell)
      # before_df = df[df['POSITION_T'] == t-1]
      before_df = df[df['POSITION_T'] == temp_cell.time]
      dec_ret = before_df[before_df['TRACK_ID'] == i]
      # print(dec_ret)
      x = dec_ret['POSITION_X'].iloc[-1]
      y = dec_ret['POSITION_Y'].iloc[-1]
      area = dec_ret['AREA'].iloc[-1]
      decPoint.append([x,y])
    print("消えた細胞座標")
    print(decPoint)
      
    for i in incID:
      inc_ret = df_temp[df_temp['TRACK_ID'] == i]
      x1 = inc_ret['POSITION_X'].iloc[-1]
      y1 = inc_ret['POSITION_Y'].iloc[-1]
      area = inc_ret['AREA'].iloc[-1]
      incPoint.append([x1,y1])
    print("増えた細胞座標")
    print(incPoint)
    
    if len(incPoint) == 0 or len(decPoint) == 0:
      matching = []
    else:
      # 距離行列を計算
      distance_matrix = euclidean_distance_matrix(decPoint, incPoint)

      # 上限を超える距離を非常に大きな値に設定
      large_value = 1e6
      distance_matrix[distance_matrix > distance_threshold] = large_value
      # ハンガリアン法を使用して最小コストマッチングを見つける
      row_ind, col_ind = linear_sum_assignment(distance_matrix)
      # 結果をフィルタリングして上限を超えないペアのみをマッチングリストに追加
      matching = [(r, c) for r, c in zip(row_ind, col_ind) if distance_matrix[r, c] < large_value]
    print("マッチング：",matching)
    diff_list = decID.copy()

    for i in matching:
      matching_dec = decID[i[0]]
      matching_inc = incID[i[1]]

      diff_list.remove(matching_dec)

      cells_Fixed_value[matching_dec].add_cell(Cell(matching_inc,t))

      # print(cells_Fixed_value[matching_dec])
      #キーの変更
      cells_Fixed_value[matching_inc] = cells_Fixed_value.pop(matching_dec)

    # for i in diff_list:
    #   for t_b in range(2, time_frame_before+1):
    #     time_frame_before_df = df[df['POSITION_T'] == t-t_b]


    #消えた細胞を削除
    for i in diff_list:
      temp_cell = cells_Fixed_value[i].list[-1]
      before_df = df[df['POSITION_T'] == temp_cell.time]
      before_df_cell = before_df[before_df['TRACK_ID'] == i]
      area = before_df_cell['AREA'].iloc[-1]
      temp_cell.memory = temp_cell.memory + 1
      if i not in cells_Fixed_value or area < cell_size or temp_cell.memory > memory_limit:
        ret_cells_Fixed_value.append(cells_Fixed_value.pop(i))

      #書き込みcsv
  with open('./data/'+formatted_time+'.csv', 'a') as f:
    writer = csv.writer(f)
        
    cells_temp = df_temp.shape[0]
    if t == 0:
      writer.writerow(['ID','TRACK_ID','POSITION_X','POSITION_Y','POSITION_T','AREA'])
    for i in cells_Fixed_value.values():
      df_cell = i.list[-1]
      df_temp = df[df['POSITION_T'] == df_cell.time]
      df_temp = df_temp[df_temp['TRACK_ID'] == df_cell.id]
      # print(df_temp.values.tolist())
      # print(i.list[-1].id)
      l_temp = []
      l_temp.append(i.id)
      l_temp = l_temp + df_temp.values.tolist()[0]
      writer.writerow(l_temp)

with open('./data/DeletedCells'+formatted_time+'.csv', 'a') as m:
  writer = csv.writer(m)
  writer.writerow(['ID','TRACK_ID','POSITION_X','POSITION_Y','POSITION_T','AREA'])
  # print(ret_cells_Fixed_value)
  for i in ret_cells_Fixed_value:
    df_cells = i.list
    # print(df_cells)
    for cell in df_cells:
      df_temp = df[df['POSITION_T'] == cell.time]
      df_temp = df_temp[df_temp['TRACK_ID'] == cell.id]
      writer.writerow([i.id] + df_temp.values.tolist()[0])

    writer.writerow(["-","-","-","-","-"])