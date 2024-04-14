import cv2
import os
from datetime import datetime

def extract_frames(video_path, output_folder, frame_rate):
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)

    skip_frames = int(round(fps / frame_rate))
    
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    frame_count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        if frame_count % skip_frames == 0:
            output_file = os.path.join(output_folder, f"frame_{frame_count}.jpg")
            cv2.imwrite(output_file, frame)
        
        frame_count += 1
    
    cap.release()

if __name__ == "__main__":
    video_path = input("動画ファイルのパスを入力：")

    output_folder = "./output_frames"

    current_date = datetime.now().strftime("%Y-%m-%d")

    output_folder = output_folder + "/" + current_date

    frame_rate = 100

    extract_frames(video_path, output_folder, frame_rate)