from PIL import Image
import os

def resize_and_save_images(input_folder, output_folder, max_size=(10000, 10000)):
    # 出力フォルダが存在しない場合は作成
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # フォルダ内のTIFFファイルを取得
    tiff_files = sorted([file for file in os.listdir(input_folder) if file.endswith(('.tiff', '.tif'))])
    
    if not tiff_files:
        print("フォルダ内にTIFFファイルが見つかりませんでした。")
        return
    c = 0
    
    for file_name in tiff_files:
        input_path = os.path.join(input_folder, file_name)
        output_path = os.path.join(output_folder, file_name)
        
        with Image.open(input_path) as img:
            # 画像を縮小
            img.thumbnail(max_size, Image.ANTIALIAS)
            # 圧縮オプションを指定して保存
            img.save(output_path, compression="tiff_deflate")
            print(f"{file_name} を圧縮して保存しました: {output_path}")
        
        c += 1
        if c == 3001:
            break

# 入力フォルダの指定
input_folder = "/Users/apple/研究/data/小田切先生研究データ/Experiment/Scratch Assay"
# 出力フォルダの指定
output_folder = "/Users/apple/研究/data/小田切先生研究データ/Experiment/Scratch Assay_c"

# 画像を縮小して保存
resize_and_save_images(input_folder, output_folder)