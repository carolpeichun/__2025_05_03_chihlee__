import streamlit as st
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.font_manager as fm

from lesson15_1 import download_data, create_close_price_df

st.set_page_config(
    page_title="股票儀表板",
    page_icon="📈",
    layout="wide"
)

@st.cache_data(ttl=3600)
def load_data():
    try:
        close_df = create_close_price_df()
    except FileNotFoundError:
        return pd.DataFrame()
    return close_df

def main():
    st.title("📈 股票趨勢分析儀表板")
    st.markdown("這是一個使用 Streamlit 建立的互動式儀表板，用來視覺化股票收盤價。")

    with st.sidebar:
        st.header("⚙️ 控制面板")
        if st.button("更新最新股價資料"):
            with st.spinner("正在下載最新資料..."):
                download_data()
                st.cache_data.clear()
                st.success("資料更新成功！")

        stock_data = load_data()

        if not isinstance(stock_data.index, pd.DatetimeIndex):
            stock_data.index = pd.to_datetime(stock_data.index, errors='coerce')

        if stock_data.empty or stock_data.index.isnull().all():
            st.warning("目前沒有可顯示的股票資料。請先點擊 '更新最新股價資料'。")
            return

        st.subheader("1. 選擇股票")
        available_stocks = stock_data.columns.tolist()
        selected_stocks = st.multiselect(
            label="選擇要分析的股票 (可複選)",
            options=available_stocks,
            default=available_stocks[:1]
        )

        st.subheader("2. 選擇日期區間")
        min_date = stock_data.index.min().to_pydatetime()
        max_date = stock_data.index.max().to_pydatetime()

        start_date = st.date_input(
            label="開始日期",
            value=min_date,
            min_value=min_date,
            max_value=max_date
        )

        end_date = st.date_input(
            label="結束日期",
            value=max_date,
            min_value=min_date,
            max_value=max_date
        )

        if start_date > end_date:
            st.error("錯誤：開始日期不能晚於結束日期。")
            return

    st.header("📊 分析結果")

    if not selected_stocks:
        st.info("請從左側的控制面板選擇至少一支股票以顯示圖表。")
    else:
        mask = (stock_data.index >= pd.to_datetime(start_date)) & (stock_data.index <= pd.to_datetime(end_date))
        filtered_data = stock_data.loc[mask, selected_stocks]

        if filtered_data.empty:
            st.warning("在選定的日期區間內沒有資料可顯示。")
        else:
            # 詳細數據在上（日期顯示年月日，金額小數點取到第一位）
            st.subheader("詳細數據 (最近50筆)")
            df_display = filtered_data.copy()
            df_display = df_display.sort_index(ascending=False).head(50)
            # 將所有金額欄位四捨五入到小數點第一位
            df_display = df_display.apply(pd.to_numeric, errors='coerce').round(1)
            df_display.index = df_display.index.strftime('%Y-%m-%d')
            st.dataframe(df_display)

            # 收盤價趨勢圖在下，y軸間距100，x軸以年為主刻度但顯示年月日
            st.subheader("收盤價趨勢圖")
            font_path = "ChineseFont.ttf"
            if not any(font_path in f.fname for f in fm.fontManager.ttflist):
                fm.fontManager.addfont(font_path)
            plt.rcParams['font.sans-serif'] = ['ChineseFont']
            plt.rcParams['axes.unicode_minus'] = False

            filtered_data_numeric = filtered_data.apply(pd.to_numeric, errors='coerce')
            if filtered_data_numeric.dropna(how='all').empty:
                st.warning("選定區間內沒有可繪圖的數值資料。")
            else:
                fig, ax = plt.subplots(figsize=(10, 5))
                filtered_data_numeric.plot(ax=ax)
                ax.set_ylabel("收盤價")
                ax.set_xlabel("日期")
                # 設定y軸間距
                ymin, ymax = ax.get_ylim()
                ax.set_yticks(range(int(ymin // 100 * 100), int(ymax // 100 * 100 + 200), 100))
                # 設定x軸主刻度為每年，標籤顯示年月日
                ax.xaxis.set_major_locator(mdates.YearLocator())
                ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
                plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right', fontsize=10)
                plt.tight_layout()
                st.pyplot(fig)

if __name__ == "__main__":
    main()