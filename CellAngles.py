import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv('/Users/apple/研究/CellTrackingAnalysis/data/60-fast-ang/ang.csv')

def calculate_angle_change(df):
    df['angle_change'] = df.groupby('ID')['ELLIPSE_THETA'].diff()
    return df

df = calculate_angle_change(df)

print("角度変化を計算したデータフレーム:")
print(df)

plt.figure(figsize=(10, 6))


cell_ids = df['ID'].unique()[:1]
for cell_id in cell_ids:
    cell_data = df[df['ID'] == cell_id]
    plt.plot(cell_data['POSITION_T'], cell_data['angle_change'], marker='o', label=f'Cell {cell_id}')

plt.xlabel('Time')
plt.ylabel('Angle Change (degrees)')
plt.title('Angle Change of Cells Over Time (First 5 Cells)')
plt.legend()
plt.grid(True)
plt.show()