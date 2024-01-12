import cv2
import time
from ultralytics import YOLO
import os
import glob
from callapi import CallAPI
mCallAPI = CallAPI()
def initialize_yolo_model(model_path="bestv1.pt"):
    return YOLO(model_path)

def maintain_image_limit(folder, limit=1000):
    images = glob.glob(f"{folder}/*.jpg")
    if len(images) > limit:
        oldest_image = sorted(images, key=os.path.getmtime)[0]
        os.remove(oldest_image)

def reconnect_rtsp(url, max_attempts=10, interval=5):
    cap = None
    attempts = 0

    while attempts < max_attempts:
        cap = cv2.VideoCapture(url)
        if cap.isOpened():
            print("RTSP stream connected.")
            return cap
        else:
            print(f"Connection failed, attempt {attempts+1}/{max_attempts}. Retrying in {interval} seconds...")
            time.sleep(interval)
            attempts += 1
    mCallAPI.callrailstats(os.getenv('SOURCE',"未曾設定"), os.getenv('CAPTION',"未曾設定"), "cambreak", "")
    print("Failed to connect to RTSP stream after maximum attempts.")
    return None

def save_detected_images(frame, results, folder='data'):
    timestamp = str(time.time())
    cv2.imwrite(f'{folder}/{timestamp}.jpg', frame)
    cv2.imwrite(f'{folder}/{timestamp}_plot.jpg', results[0].plot())
    return f'{folder}/{timestamp}.jpg'

def main():
    if not os.path.exists('data'):
        os.makedirs('data')

    rtsp_url = os.getenv('RTSP_URL', "rtsp://user:user123456@125.228.247.68:7001/797e5e39-dcf7-7613-2279-8a16f39e7ff8?ch01.264?dev=1")
    d_count = int(os.getenv('DETECTION_COUNT', 7))

    model = initialize_yolo_model()
    cap = reconnect_rtsp(rtsp_url)

    while True:
        if cap is not None and cap.isOpened():
            ret, frame = cap.read()
            if ret:
                results = model(frame)
                if len(results[0].boxes.cls) < d_count:
                    print(f"發報: {len(results[0].boxes.cls)}   d_count: {d_count}")
                    # 發報 API
                    imgpath = save_detected_images(frame, results)
                    mCallAPI.callrailstats(os.getenv('SOURCE',"未曾設定"), os.getenv('CAPTION',"未曾設定"), "railbreak", imgpath)
                    maintain_image_limit('data', 1000)
                else:
                    mCallAPI.callrailstats(os.getenv('SOURCE',"未曾設定"), os.getenv('CAPTION',"未曾設定"), "normal", '')
                for _ in range(5):
                    cap.read()
                time.sleep(0.1)
                
            else:
                mCallAPI.callrailstats(os.getenv('SOURCE',"未曾設定"), os.getenv('CAPTION',"未曾設定"), "cambreak", "")
                print("Stream disconnected. Attempting to reconnect...")
                cap.release()
                cap = reconnect_rtsp(rtsp_url)
        else:
            cap = reconnect_rtsp(rtsp_url)
        if cap is None:
            break

    if cap is not None:
        cap.release()

if __name__ == "__main__":
    main()
