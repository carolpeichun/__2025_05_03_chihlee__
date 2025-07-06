"""
主應用程式入口點，提供命令列介面（CLI）功能。
"""
import argparse
import pandas as pd


def process_csv_to_excel(csv_path: str, excel_path: str):
    """
    讀取CSV檔案，建立樞紐表，並輸出為Excel檔案。
    依據 lesson17_2.ipynb 的處理方式：
    - 重新命名欄位
    - 計算小費比例
    - 依吸煙者與日期分組，計算小費與總票價的數量、平均、最大值
    """
    tips_df = pd.read_csv(csv_path)
    tips_df.columns = ['總票價', '小費', '吸煙者', '日期', '時間', '大小']
    tips_df['小費比例'] = tips_df['小費'] / tips_df['總票價']
    grouped = tips_df.groupby(by=['吸煙者', '日期'])
    functions = [('數量', 'count'), ('平均', 'mean'), ('最大值', 'max')]
    tips_df3 = grouped[['小費', '總票價']].agg(functions)
    tips_df3.to_excel(excel_path)
    print(f"已將樞紐表輸出至 {excel_path}")


def main():
    """主程式，負責解析命令列參數。"""
    parser = argparse.ArgumentParser(description="CSV 樞紐表轉 Excel 工具")
    parser.add_argument('--csv', type=str, required=True, help='輸入的 CSV 檔案路徑')
    parser.add_argument('--excel', type=str, required=True, help='輸出的 Excel 檔案路徑')
    args = parser.parse_args()
    process_csv_to_excel(args.csv, args.excel)

if __name__ == "__main__":
    main()
