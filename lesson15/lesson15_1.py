import yfinance as yf
from datetime import datetime, timedelta
import os
import pandas as pd

def download_data():
    """
    每日下載指定股票的資料，並儲存為CSV檔。

    1. 股票代碼: 2330.TW, 2303.TW, 2454.TW, 2317.TW
    2. 檔案會儲存在 'data' 資料夾內。
    3. 檔案名稱格式為 '代碼_YYYY-MM-DD.csv' (例如: 2330_2023-10-27.csv)。
    4. 如果當日的檔案已存在，則不會重複下載。
    5. 每次成功下載新檔案後，會刪除該股票對應的舊日期檔案，確保只保留最新的一份。    
    6. 如果下載日無交易資料 (如假日)，則會省略不建立新檔案。
    7. 檔案名稱會以資料本身的最新日期來命名，確保檔名與內容一致。
    8. 在非交易日執行時，程式會偵測到資料已是最新而跳過，不會產生重複或無效的檔案。
    """
    # 設定股票列表和資料夾名稱
    STOCKS = ['2330.TW', '2303.TW', '2454.TW', '2317.TW']
    DATA_DIR = 'dataUpdated'
    START_DATE = '2000-01-01'

    # 確保資料夾存在
    os.makedirs(DATA_DIR, exist_ok=True)

    # 獲取今天的日期
    today = datetime.now()
    # 為了確保能抓到包含今天在內的最新資料，yf.download 的結束日期 (end) 參數需要設定為明天
    tomorrow = today + timedelta(days=1)
    end_date_str = tomorrow.strftime('%Y-%m-%d')

    for ticker in STOCKS:
        stock_code = ticker.split('.')[0]
                
        # 1. 下載資料
        print(f"正在下載 {ticker} 的資料...")
        try:
            # 使用 end_date_str (明天) 作為結束日期，才能確保下載到今天 (today_str) 的資料
            data = yf.download(ticker, start=START_DATE, end=end_date_str, auto_adjust=True)
            
            # 增加對索引的檢查，確保資料不僅存在，而且包含日期索引
            if data.empty or len(data.index) == 0:
                print(f"警告：找不到 {ticker} 的任何有效資料，跳過。")
                continue
            
            # 2. 以資料的「最新日期」來產生檔名
            latest_date_str = data.index[-1].strftime('%Y-%m-%d')
            new_filename = f"{stock_code}_{latest_date_str}.csv"
            new_filepath = os.path.join(DATA_DIR, new_filename)

            # 3. 檢查最新資料的檔案是否已存在，若已存在則代表資料已是最新，直接跳過
            if os.path.exists(new_filepath):
                print(f"資料已是最新 ({latest_date_str})，檔案 '{new_filename}' 已存在，無需更新。")
                continue
            
            # 4. 儲存新檔案
            data.to_csv(new_filepath)
            print(f"成功儲存新資料至 '{new_filepath}'")

            # 5. 刪除此股票的所有其他舊檔案
            for filename in os.listdir(DATA_DIR):
                if filename.startswith(f"{stock_code}_") and filename.endswith(".csv") and filename != new_filename:
                    old_filepath = os.path.join(DATA_DIR, filename)
                    os.remove(old_filepath)
                    print(f"已刪除舊檔案: {old_filepath}")
        except Exception as e:
            print(f"下載 {ticker} 時發生錯誤: {e}")

def create_close_price_df():
    """
    讀取 dataUpdated 資料夾中最新的個股 CSV 檔，並將收盤價整合成一個 DataFrame。

    Returns:
        pandas.DataFrame: 包含所有股票收盤價的 DataFrame，若無資料則回傳空的 DataFrame。
    """
    DATA_DIR = 'dataUpdated'
    STOCK_MAP = {
        '2330': '台積電',
        '2303': '聯電',
        '2454': '聯發科',
        '2317': '鴻海'
    }

    all_close_series = []
    
    if not os.path.exists(DATA_DIR):
        print(f"錯誤：資料夾 '{DATA_DIR}' 不存在。請先執行 download_data()。")
        return pd.DataFrame()

    for stock_code, stock_name in STOCK_MAP.items():
        # 尋找該股票的所有CSV檔案
        try:
            files = [f for f in os.listdir(DATA_DIR) if f.startswith(f"{stock_code}_") and f.endswith(".csv")]
            if not files:
                print(f"警告：在 '{DATA_DIR}' 中找不到 {stock_code} ({stock_name}) 的任何檔案。")
                continue

            # 根據檔名排序找到最新的檔案
            latest_file = sorted(files)[-1]
            filepath = os.path.join(DATA_DIR, latest_file)
            
            # 修正：讀取CSV時，直接將第一欄(column 0)設為索引，這樣更穩健，可避免 'Date' not in list 的錯誤
            df = pd.read_csv(filepath, index_col=0, parse_dates=[0], date_format='%Y-%m-%d')
            # 為了保持資料結構的一致性，手動將索引的名稱設為 'Date'
            df.index.name = 'Date'
            
            # 擷取'Close'欄位，並重新命名為中文名稱
            close_series = df['Close'].rename(stock_name)
            all_close_series.append(close_series)
            print(f"已讀取並處理檔案: {latest_file}")

        except Exception as e:
            print(f"處理 {stock_code} 的檔案時發生錯誤: {e}")

    if not all_close_series:
        print("沒有成功讀取任何股票資料，無法合併。")
        return pd.DataFrame()

    # 將所有 Series 合併成一個 DataFrame，日期會自動對齊
    # 缺失的日期會自動填上 NaN (顯示為空白)
    combined_df = pd.concat(all_close_series, axis=1)
    
    return combined_df

def main():
    download_data()
    
    # 建立並顯示合併後的收盤價 DataFrame
    close_df = create_close_price_df()
    if not close_df.empty:
        print("\n==================== 合併後的收盤價資料 (最後5筆) ====================")
        print(close_df.tail())
        print("======================================================================")

if __name__ == '__main__':
    main()