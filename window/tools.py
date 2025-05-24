#此為module，是一個.py檔，將函數存在此處，在主程式檔要叫用此處的函數時，函數前要加此處的檔名(tools)

#函數
def caculate_bmi(height:int,weight:int)->float: #def→定義 #caculate_bmi→函數 #h→參數 #:int→typehint(引數值的型別) #->float傳回浮點數
    return weight / (height / 100) ** 2

#函數
def get_state(bmi:float)->str:
    if bmi < 18.5:
        return "體重過輕"
    elif bmi < 24:
        return "正常範圍"
    elif bmi < 27:
        return "過重"
    elif bmi < 30:
        return "輕度肥胖"
    elif bmi < 35:
        return "中度肥胖"
    else:
        return "重度肥胖"