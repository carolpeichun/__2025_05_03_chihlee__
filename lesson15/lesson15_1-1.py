import yfinance as yf
from datetime import datetime
import os

def download_data():
    """
    每日更新並下載指定股票的資料，並以日期為檔名儲存。

    1. 股票代碼: 2330.TW, 2303.TW, 2454.TW, 2317.TW
    2. 檔案會儲存在 'data' 資料夾內。
    3. 檔案名稱格式為 '代碼_YYYY-MM-DD.csv' (例如: 2330_2023-10-27.csv)。
    4. 如果當日的檔案已存在，則跳過下載。
    5. 每次成功下載新檔案後，會刪除該股票對應的所有舊檔案 (包含無日期和舊日期的檔案)，確保只保留最新的一份。
    """
    # 設定股票列表和資料夾名稱
    STOCKS = ['2330.TW', '2303.TW', '2454.TW', '2317.TW']
    DATA_DIR = 'dataUpdated1'
    START_DATE = '2000-01-01'

    # 確保資料夾存在
    os.makedirs(DATA_DIR, exist_ok=True)

    # 獲取今天的日期字串
    today_str = datetime.now().strftime('%Y-%m-%d')

    for ticker in STOCKS:
        # 從 ticker '2330.TW' 中取得股票代碼 '2330'
        stock_code = ticker.split('.')[0]
        
        # 組合今天的檔案路徑
        today_filename = f"{stock_code}_{today_str}.csv"
        today_filepath = os.path.join(DATA_DIR, today_filename)

        # 1. 檢查今日檔案是否已存在，若存在則跳過
        if os.path.exists(today_filepath):
            print(f"'{today_filepath}' 今日檔案已存在，跳過下載。")
            continue

        # 2. 下載資料
        print(f"正在下載 {ticker} 的最新資料...")
        try:
            # 下載從起始日到今日的完整資料
            data = yf.download(ticker, start=START_DATE, end=today_str, auto_adjust=True)
            if data.empty:
                print(f"警告：找不到 {ticker} 的資料，跳過儲存。")
                continue
            
            # 3. 儲存為今日的檔案
            data.to_csv(today_filepath)
            print(f"成功儲存資料至 '{today_filepath}'")

            # 4. 刪除此股票的舊檔案 (包括有日期和無日期的)
            for filename in os.listdir(DATA_DIR):
                # 檢查檔案是否為此股票的舊CSV檔
                # 條件1: 檔名以 '2330_' 開頭 (舊日期檔) 或 檔名等於 '2330.csv' (無日期檔)
                # 條件2: 檔名以 '.csv' 結尾
                # 條件3: 檔名不是今天的新檔案
                if (filename.startswith(f"{stock_code}_") or filename == f"{stock_code}.csv") and filename.endswith(".csv") and filename != today_filename:
                    old_filepath = os.path.join(DATA_DIR, filename)
                    os.remove(old_filepath)
                    print(f"已刪除舊檔案: {old_filepath}")
        except Exception as e:
            print(f"下載 {ticker} 時發生錯誤: {e}")

def main():
    download_data()

if __name__ == '__main__':
    main()