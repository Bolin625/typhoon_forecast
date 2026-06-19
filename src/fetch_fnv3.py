import os
import requests

# 建立專案結構
DATA_DIR = "./data"
os.makedirs(DATA_DIR, exist_ok=True)

def test_connection():
    print("🛰️ [FNV3 颱風預報系統] 啟動中...")
    print("📂 檢查數據儲存路徑... [OK]")
    
    # 這裡未來會換成真實的 FNV3 開放數據源 URL
    print("🔍 正在嘗試連線至氣象數據伺服器...")
    
    # 提示：此處可加入你預計使用的 FNV3 資料下載點
    print("✅ 環境就緒！隨時可以開始解析 FNV3 格點/路徑數據。")

if __name__ == "__main__":
    test_connection()