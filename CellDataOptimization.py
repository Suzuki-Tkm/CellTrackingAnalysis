import pandas as pd
import math

# print(pd.__version__)

input = pd.read_csv('/Users/apple/研究/data/小田切先生研究データ/60-fast/回答データと実験データ - 実験データ.csv')

#細胞数
cells = 72
AllowableDistance = 1000

df = input[['TRACK_ID','POSITION_X','POSITION_Y','POSITION_T','AREA']] #データの抽出
df = df.drop(df.index[[0,1,2]]) #利用しない行の削除
df = df.apply(pd.to_numeric, errors='coerce') #データの数値化
df = df.sort_values(by=['POSITION_T','TRACK_ID']) #ソート

#細胞データを作成（分裂しないと仮定し、細胞数を72に固定.keyをid、valueを実験データid）
use_cells_Fixed_value = list(df[df['POSITION_T']==0]['TRACK_ID'])
cells_Fixed_value = {i+1: use_cells_Fixed_value[i] for i in range(0, cells)}

# 確認用
# cnt = 0 
# for i in df['POSITION_T']:
#   if i == 0:
#     cnt += 1
# print(cnt)

# print(df['POSITION_T'].max())

for t in range(4):
  print("-------- time ",t," --------")
  df_temp = df[df['POSITION_T'] == t]
  cells_temp = df_temp.shape[0]
  print("細胞数",cells_temp)
  decID = list(cells_Fixed_value.values()) #使われているかの判定用
  incID = []
  # print(cells_Fixed_value.values())
  for i in range(cells_temp):
    cell = df_temp[i:i+1]
    id = cell['TRACK_ID'].iloc[-1]
    # print(df_temp)
    if id in list(cells_Fixed_value.values()):
      # print("正常")
      decID.remove(id)
    else:
      # print("異常個体id",id)
      incID.append(id)

  # 細胞の増減のデータ
  # print("---------増---------")
  # for i in incID:
  #   print(df_temp[df_temp['TRACK_ID'] == i])

  if t!=0:
    # print("---------減---------")
    for i in decID:
      before_df = df[df['POSITION_T'] == t-1]
      ret = before_df[before_df['TRACK_ID'] == i]
      # print(ret)
      x = ret['POSITION_X'].iloc[-1]
      y = ret['POSITION_Y'].iloc[-1]
      area = ret['AREA'].iloc[-1]

      ans_dis = 100000000
      ans_id = 0

      for k in incID:
        ret1 = df_temp[df_temp['TRACK_ID'] == k] 
        x1 = ret1['POSITION_X'].iloc[-1]
        y1 = ret1['POSITION_Y'].iloc[-1]
        area1 = ret1['AREA'].iloc[-1]
        distance = math.sqrt((x - x1) ** 2 + (y - y1) ** 2)
        if ans_dis > distance:
          ans_dis = distance
          ans_id = k
        
      print(i,ans_id,"マッチング確認")
      print("距離",ans_dis)
      if ans_dis < AllowableDistance:
        cells_Fixed_value

  # データの結合

  # for i in decID:
  #   before_df = df[df['POSITION_T'] == t-1]
  #   x = before_df[before_df['TRACK_ID'] == i]
  #   print(x)

