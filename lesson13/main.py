import streamlit as st

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

if __name__ == "__main__":
    main()
