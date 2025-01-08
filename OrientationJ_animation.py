import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# データをCSVファイルから読み込む
data = pd.read_csv("/Users/apple/Downloads/16000cells_1day_疎_OJ-Distribution-1.csv")

# グラフの設定
fig, ax = plt.subplots()

# Y軸の範囲をスライスの最小・最大値に基づいて設定
y_min = data.iloc[:, 1:].min().min()  # 各スライスの最小値を取得
y_max = data.iloc[:, 1:].max().max()  # 各スライスの最大値を取得
ax.set_xlim(min(data['Orientation']), max(data['Orientation']))  # X軸範囲（Orientation）
ax.set_ylim(y_min, y_max)  # Y軸範囲（スライスの最小・最大値）

line, = ax.plot([], [], lw=2)

# アニメーションの更新関数
def update(frame):
    # スライスごとのデータ
    slice_data = data.iloc[:, [0, frame + 1]]
    
    # グラフを更新
    line.set_data(slice_data['Orientation'], slice_data.iloc[:, 1])
    ax.set_title(f'Slice {frame + 1}')
    return line,

# アニメーションの設定
ani = FuncAnimation(fig, update, frames=len(data.columns) - 1, blit=True, interval=500)

# MP4ファイルとして保存
ani.save('/Users/apple/Downloads/animation.mp4', writer='ffmpeg', fps=30)
# ani.save('/Users/apple/Downloads/animation.gif', writer='imagemagick', fps=2)
# アニメーションを表示
# plt.show()