import numpy as np
from scipy.optimize import linear_sum_assignment

# 座標リストを定義
A = np.array([])
B = np.array([[15, 15], [25, 25], [35, 35]])

# ユークリッド距離を計算
def euclidean_distance_matrix(A, B):
    return np.linalg.norm(A[:, np.newaxis] - B, axis=2)

# 距離行列を計算
distance_matrix = euclidean_distance_matrix(A, B)

# 距離の上限を設定
distance_threshold = 10  # 例として上限を10に設定

# 上限を超える距離を非常に大きな値に設定
large_value = 1e6
distance_matrix[distance_matrix > distance_threshold] = large_value

# ハンガリアン法を使用して最小コストマッチングを見つける
row_ind, col_ind = linear_sum_assignment(distance_matrix)

# 結果をフィルタリングして上限を超えないペアのみをマッチングリストに追加
matching = [(r, c) for r, c in zip(row_ind, col_ind) if distance_matrix[r, c] < large_value]
print(matching)