from PIL import Image
import os

def combine_to_multi_page_tiff(folder_path, output_file):
    tiff_files = sorted([file for file in os.listdir(folder_path) if file.endswith('.tiff') or file.endswith('.tif')])
    if not tiff_files:
        print("No TIFF files found in the folder.")
        return

    images = []
    
    for file_name in tiff_files:
        image = Image.open(os.path.join(folder_path, file_name))
        images.append(image)
    
    images[0].save(output_file, save_all=True, append_images=images[1:])
    print(f"Combined {len(tiff_files)} TIFF files into {output_file}")

# tiffフォルダの指定
folder_path = "/Users/apple/Downloads/Experiment 2/血管内皮細胞/血管内皮細胞x10マトリゲル"
# tiffのファイルの指定
output_file = "/Users/apple/Downloads/Experiment 2/血管内皮細胞/血管内皮細胞x10マトリゲル.tiff"
combine_to_multi_page_tiff(folder_path, output_file)
