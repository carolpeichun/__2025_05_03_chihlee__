import random

def play_game():    #default function  #define
    min = 1
    max = 99
    count = 0
    random_number = random.randint(min,max) #運算式random.randint(min,max)前面加=即變敘述式, 當運算式的值還要再用到時, 可改成敘述式將值丟進random_number
    print(random_number)  #先知道答案
    print("=====猜數字遊戲開始========\n")
    while(True): #while後不用空格的bool
        input_number = int(input(f"請輸入數字({min}~{max}):"))
        count += 1    
        if(input_number == random_number):
            print(f"賓果!猜對了, 答案是:{input_number}")
            print(f"您總共猜了{count}次")
            break
        elif(input_number>random_number):
            print(f"再小一點")  #字串插補, 程式執行中若無需加值可不需{}
            max = input_number - 1
        elif(input_number<random_number):
            print(f"再大一點")
            min = input_number + 1

    print(f"您已經猜了{count}次\n")
    
while(True):
    play_game()     #呼叫function
    play_again = input("再玩一次(y,n):")
    if(play_again == 'n'):
        break

print("Game Over")