import pandas as pd
import math
import numpy as np
from scipy.optimize import linear_sum_assignment

class Cell:
  def __init__(self,id , time):
    self.id = id
    self.time = time

class Cells:
  def __init__(self,cell):
    self.list = [cell]

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
distance_threshold = 6  # 例として上限を10に設定

# cellの大きさを指定
cell_size = 1000

# 再マッチングの距離の許容範囲
distance_threshold_next = 6
# 許容するフレーム数
time_next = 3


df = input[['TRACK_ID','POSITION_X','POSITION_Y','POSITION_T','AREA']] #データの抽出
df = df.drop(df.index[[0,1,2]]) #利用しない行の削除
df = df.apply(pd.to_numeric, errors='coerce') #データの数値化
df = df.sort_values(by=['POSITION_T','TRACK_ID']) #ソート

#細胞データを作成（分裂しないと仮定し、細胞数を72に固定.keyをid、valueを実験データid）
use_cells_Fixed_value = list(df[df['POSITION_T']==0]['TRACK_ID'])
# cells_Fixed_value = {i+1: use_cells_Fixed_value[i] for i in range(0, cells)}
# cells_Fixed_value = {use_cells_Fixed_value[i]: [use_cells_Fixed_value[i]] for i in range(0, cells)}
cells_Fixed_value = {use_cells_Fixed_value[i]: Cells(Cell(use_cells_Fixed_value[i] , 0)) for i in range(0, cells)}
ret_cells_Fixed_value = {}

unused_cells = {}

# 確認用
# cnt = 0 
# for i in df['POSITION_T']:
#   if i == 0:
#     cnt += 1
# print(cnt)

# print(df['POSITION_T'].max())

for t in range(500):
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
    diff_list_dec = decID.copy()
    diff_list_inc = incID.copy()

    for i in matching:
      matching_dec = decID[i[0]]
      matching_inc = incID[i[1]]

      diff_list_dec.remove(matching_dec)
      diff_list_inc.remove(matching_inc)

      cells_Fixed_value[matching_dec].add_cell(Cell(matching_inc,t))

      # print(cells_Fixed_value[matching_dec])
      #キーの変更
      cells_Fixed_value[matching_inc] = cells_Fixed_value.pop(matching_dec)

    # for i in diff_list:
    #   for t_b in range(2, time_frame_before+1):
    #     time_frame_before_df = df[df['POSITION_T'] == t-t_b]
    
    #記録用のセル(新規追加されたがマッチングされなかった)
    print(diff_list_inc)
    for i in diff_list_inc:
      # if unused_cells not in i:
      #   unused_cells[i] = Cells(Cell(i,t))
      # else:
      #   unused_cells[i].add_cell(Cell(i,t))

    #消えた細胞を削除
    # for i in diff_list_dec:
    #   temp_cell = cells_Fixed_value[i].list[-1]
    #   before_df = df[df['POSITION_T'] == temp_cell.time]
    #   before_df_cell = before_df[before_df['TRACK_ID'] == i]
    #   area = before_df_cell['AREA'].iloc[-1]
    #   if i not in cells_Fixed_value or area < cell_size:
    #     #t=2以上前のデータから解析するパターン
    #     for k in unused_cells:
    #       c = k.list[-1]
    #       before_df_tmep = df[df['POSITION_T'] == c.time]
    #       before_df_c = before_df_tmep[before_df_tmep['TRACK_ID'] == c.id]
    #       t_temp = before_df_c['POSITION_T'].iloc[-1]
    #       if t - t_temp < time_next:
    #         cell_distance = math.sqrt((before_df_c['POSITION_X'].iloc[-1] - before_df_cell['POSITION_X'].iloc[-1])**2 + (before_df_c['POSITION_Y'].iloc[-1] - before_df_cell['POSITION_Y'].iloc[-1])**2)
    #         if cell_distance < distance_threshold_next:
    #           cells_Fixed_value[i].add_cell(c)
    #           cells_Fixed_value[i] = cells_Fixed_value.pop(k)
    #           continue
        ret_cells_Fixed_value = cells_Fixed_value.pop(i)

    #この場合どの細胞を追跡対象にするのか
    for i in cells_Fixed_value.values():
      for k in i.list:
        print(k.id,end=' , ')
      print()