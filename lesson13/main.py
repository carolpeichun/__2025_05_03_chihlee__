import streamlit as st
import pandas as pd

def main():
    st.title("我的第一個 Streamlit App")
    st.write("歡迎來到我的 Streamlit 應用程式！")

    name = st.text_input("請輸入你的名字：")
    if name:
        st.write(f"你好, {name}!")

    age = st.slider("請選擇你的年齡：", 0, 100, 25)
    st.write(f"你的年齡是：{age}歲")

    if st.button("點擊我！"):
        st.success("你點擊了按鈕！")

    st.divider()

    st.header("顯示CSV資料")
    try:
        df = pd.read_csv("taiwan.csv")
        df.index = df.index + 1  # 將索引值從 1 開始
        st.write("以下是從 `taiwan.csv` 讀取的資料：")
        st.dataframe(df)
    except FileNotFoundError:
        st.error("錯誤：找不到 'taiwan.csv' 檔案。請確認檔案與您的 main.py 在同一個資料夾中。")

if __name__ == "__main__":
    main()
