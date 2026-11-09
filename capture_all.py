import os
import glob
import random
import requests
from datetime import datetime 

# 將多個監視器設定在一個清單中
CAMERAS = [
    {"id": "tnn-805038", "dir": "19watergate"},
    {"id": "tnn-805042", "dir": "longshan"}
]
MAX_IMAGES = 200

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Referer": "https://c02.twipcam.com/"
}

def process_camera(cam):
    base_url = f"https://c02.twipcam.com/cam/proxy.php?id={cam['id']}"
    save_dir = cam['dir']
    os.makedirs(save_dir, exist_ok=True)
    
    now_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = os.path.join(save_dir, f"cam_{now_str}.jpg")
    req_url = f"{base_url}&t={random.random()}"

    try:
        response = requests.get(req_url, headers=HEADERS, timeout=15)
        if response.status_code == 200 and len(response.content) > 0:
            with open(output_path, "wb") as f:
                f.write(response.content)
            print(f"成功下載: {output_path}")
        else:
            print(f"下載失敗 ({save_dir})，HTTP 狀態碼: {response.status_code}")
    except Exception as e:
        print(f"網路連線異常 ({save_dir}): {e}")

    # 清理各資料夾舊圖
    files = glob.glob(os.path.join(save_dir, "*.jpg"))
    if len(files) > MAX_IMAGES:
        files.sort(key=os.path.getmtime)
        files_to_delete = files[:-MAX_IMAGES]
        for f in files_to_delete:
            try:
                os.remove(f)
                print(f"已刪除過期舊圖: {f}")
            except OSError as e:
                print(f"刪除失敗 {f}: {e}")

if __name__ == "__main__":
    # 迴圈執行清單中的所有監視器
    for cam in CAMERAS:
        print(f"開始處理: {cam['dir']}...")
        process_camera(cam)
