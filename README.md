## 細胞トラッキング分析 -小田切研究室-

#### ・手順
1. 動画ファイルからtiffへ
→編集ソフト adobe premiere pro
2. tiffのマージ
→Tiff_combination.py
3. RGBから輝度への変換(Image/color/RGB to liminance)
4. 色の転換（Edit/Invert）
5. トラッキング分析（Plugins/tracking/TrackMate）

#### ・トラッキングアルゴリズム
StarDist - Object Detection with Star-convex Shapes
https://github.com/stardist/stardist
https://qiita.com/JohannPachelbel/items/5ddb096d0ca33076879e
https://imagej.net/imagej-wiki-static/StarDist

#### ・使用データ
| | 実験データ | 回答データ |
| ---- | ---- | ---- |
|フレームの数| 0-579 | 0-580 |
|セルの数| 5179 | 72 |
|データ数| 47650 | 41832 |

#### ・実験データの適応（CellDataOptimization.py）
1. フレームごとの細胞の増減を前のフレームから摘出
2. 減った細胞（t-1）と増えた細胞(t)を比較し、最短距離のものを摘出（ハンガリアン法：最小コストマッチング）
3. t-1のみを考慮しているため、記録（追跡）される細胞は減少するため検討する必要があり

#### ・実験データの適応の方針
1. 細胞サイズが小さいものを削除(細胞の大きさを昇順に並べたが、δに変化があまり見えなく、区切る点が難しい)
2. 分裂の際の対応
<img width="181" alt="スクリーンショット 2024-06-14 15 20 14" src="https://github.com/Suzuki-Tkm/CellTrackingAnalysis/assets/140580925/70178f6b-282a-4ee7-954b-f08f14735fb7">

#### 各Pythonファイルの説明
##### CellDFS.py
1,0からなる二次元の配列で１を島とした時、DFSでその島の大きさと周の長さを出力する
→トラッキングのアルゴリズムに悩み断念

##### Image_video.py
動画をフレームでjpg化

##### Python_to_ImageJ.py
imageJをpythonから実行

##### Table_matching_degree.py
二つのテーブルのマッチング率を計算
→実験データと回答データの分析

#### Tiff_combination.py
tiffファイルのマージ
