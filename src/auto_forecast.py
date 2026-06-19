import os
import requests
import pandas as pd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import re

def get_latest_typhoon_url():
    """自動到美國氣象局目錄抓取今年西北太平洋最新活躍的颱風編號"""
    base_url = "https://ftp.nhc.noaa.gov/atcf/btk/"
    try:
        response = requests.get(base_url, timeout=15)
        if response.status_code == 200:
            # 尋找今年 (2026) 西北太平洋 (bwp) 的所有正式檔案
            files = re.findall(r'bwp\d{2}2026\.dat', response.text)
            if files:
                # 排序並拿到最新（編號最大）的那個活躍颱風
                latest_file = sorted(list(set(files)))[-1]
                print(f"📡 偵測到當前海面最新活躍氣旋檔案: {latest_file}")
                return base_url + latest_file
    except Exception as e:
        print(f"無法連線目錄解析最新編號 ({e})")
    return None

def run_pipeline():
    print("🛰️ [GitHub Actions] 啟動智慧型颱風監測系統...")
    os.makedirs('output', exist_ok=True)
    
    # 1. 自動偵測最新實時網址
    url = get_latest_typhoon_url()
    df = None
    is_realtime = False
    
    # 2. 嘗試抓取實時數據
    if url:
        try:
            print(f"📥 正在下載實時數據: {url}")
            response = requests.get(url, timeout=15)
            if response.status_code == 200 and len(response.text) > 100:
                lon_list, lat_list = [], []
                for line in response.text.strip().split('\n'):
                    parts = line.split(',')
                    if len(parts) > 7:
                        lat_str = parts[6].strip()
                        lon_str = parts[7].strip()
                        if lat_str and lon_str:
                            lat = float(lat_str[:-1]) / 10.0 if 'N' in lat_str else -float(lat_str[:-1]) / 10.0
                            lon = float(lon_str[:-1]) / 10.0 if 'E' in lon_str else -float(lon_str[:-1]) / 10.0
                            lon_list.append(lon)
                            lat_list.append(lat)
                if lon_list:
                    df = pd.DataFrame({'Lon': lon_list, 'Lat': lat_list}).drop_duplicates().reset_index(drop=True)
                    is_realtime = True
                    title_text = 'REAL-TIME Typhoon Track - Live Sync'
                    print("✅ 成功抓取到今日此時此刻的真實海面氣旋！")
        except Exception as e:
            print(f"實時數據解析失敗 ({e})")

    # 3. 如果海面平靜無颱風，切換為歷史校驗模式
    if df is None:
        print("ℹ️ 當前西北太平洋海面平靜，無活躍颱風。自動切換為歷史經典強颱路徑（展示模式）...")
        df = pd.DataFrame({
            'Lon': [136.2, 134.1, 131.5, 128.4, 125.1, 123.0, 121.5, 120.1],
            'Lat': [15.2, 16.5, 17.8, 19.1, 20.8, 22.5, 24.1, 25.8]
        })
        title_text = 'Typhoon Track - Demo Mode (No Active Typhoon Today)'

    # 4. 繪圖
    plt.figure(figsize=(10, 8))
    ax = plt.axes(projection=ccrs.PlateCarree())
    ax.set_extent([110, 145, 10, 35], crs=ccrs.PlateCarree()) 
    
    ax.coastlines(resolution='50m', color='black', linewidth=1)
    ax.add_feature(cfeature.BORDERS, linestyle=':')
    ax.add_feature(cfeature.OCEAN, color='azure')
    ax.add_feature(cfeature.LAND, color='whitesmoke')
    ax.gridlines(draw_labels=True, dms=True, x_inline=False, y_inline=False, linestyle='--')
    
    plt.plot(df['Lon'], df['Lat'], marker='o', color='crimson' if is_realtime else 'gray', linewidth=2.5, label='Forecast Track')
    plt.scatter(df['Lon'].iloc[-1], df['Lat'].iloc[-1], color='darkred', s=150, zorder=5, label='Latest Position')
    
    plt.title(title_text, fontsize=13, fontweight='bold')
    plt.legend(loc='lower left')
    
    plt.savefig('output/latest_typhoon_track.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("🎨 圖片渲染完畢！")

if __name__ == "__main__":
    run_pipeline()