#主程式
#import edu                                     #way 1
#from edu.tools import caculate_bmi,get_state   #way 2      #from 後面只能用package(edu) or module(tools.py)
from edu.tools import caculate_bmi as a1        #way 3-1
from edu.tools import get_state as a2           #way 3-2

#函數
def main():
    height:int = int(input("請輸入身高(cm):")) #height後面+":"是表示後面要輸入typehint(引數值的型別), 即程式執行時會被要求要輸入的值的提示
    weight:int = int(input("請輸入體重(kg):"))

    bmi = a1(height, weight)

    print(bmi)
    print(a2(bmi))

#主程式
if __name__ == '__main__':
    main()