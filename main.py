class Question():
    def __init__(self):
        self.question = ""
        self.option = [""]

    def addOption(self, option):
        self.option.append(option)



loop = True
lstQuestion = []

while(loop):
    mode = input("1:問題 2:問題追加 3:終了")
    if(mode == "1"):
        print("実装中")
    elif(mode == "2"):
        print("問題追加実装注")
    elif(mode == "3"):
        print("終了します")
        loop = False
    else:
        print("引数が不正です")