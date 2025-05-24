#主程式
import tools

#函數
def main():
    height:int = int(input("請輸入身高(cm):")) #height後面+":"是表示後面要輸入typehint(引數值的型別), 即程式執行時會被要求要輸入的值的提示
    weight:int = int(input("請輸入體重(kg):"))

    bmi = tools.caculate_bmi(height, weight)

    print(bmi)
    print(tools.get_state(bmi))

#主程式
if __name__ == '__main__':
    main()