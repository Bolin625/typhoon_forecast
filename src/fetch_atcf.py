import os
import requests
import pandas as pd

def fetch_ai_typhoon_track():
    print("🛰️ [AI 颱風預報系統] 正在由公開氣象源獲取 AI 預報路徑 (ATCF 格式)...")
    
    # 這是 ECMWF / 全球氣象機構提供給 AI 模型（如 FuXi/FNV3）專用的輕量路徑資料庫範例
    # 我們先用一個公開穩定的測試路徑檔來打通工作流
    url = "https://raw.githubusercontent.com/ytg95/AI-Weather-Models/main/sample_tracks.csv"
    
    os.makedirs("./data", exist_ok=True)
    output_path = "./data/ai_track_latest.csv"
    
    try:
        response = requests.get(url, timeout=15)
        if response.status_code == 200:
            with open(output_path, "wb") as f:
                f.write(response.content)
            print(f"✅ 成功！AI 颱風預報路徑已儲存至: {output_path}")
            
            # 順便用 pandas 讀出來看看結構
            df = pd.read_csv(output_path)
            print("\n📊 最新預報數據前三行：")
            print(df.head(3))
        else:
            print(f"❌ 伺服器回應錯誤碼: {response.status_code}")
    except Exception as e:
        print(f"💥 連線失敗，請檢查網路或防火牆設定。錯誤原因: {e}")

if __name__ == "__main__":
    fetch_ai_typhoon_track()