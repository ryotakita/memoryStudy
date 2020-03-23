import pickle
import os
class Question():
    def __init__(self, subject):
        self.subject = subject
        self.option = [""]

    def addOption(self, option):
        self.option.append(option)


loop = True
lstQuestion = []
isDevMode = False

if os.path.getsize('lstQuestion.pickle') > 0:
    with open('lstQuestion.pickle', 'rb') as f:
        lstQuestion = pickle.load(f)

while(loop):
    mode = input("1:問題 2:問題追加 3:終了\n")
    if(mode == "1"):
        print("実装中")
        print(lstQuestion)
    elif(mode == "2"):
        subject = input("問題文を入力してください\n")
        question = Question(subject)
        print(question.subject)
        numOption = input("選択肢の数を入力してください(デフォルト=2)\n")
        if(numOption == ""):
            numOption = 2
        for i in range(int(numOption)):
            option = input("選択肢" + str(i+1) + "を入力してください\n")
            question.addOption(option)
        lstQuestion.append(question)
    elif(mode == "3"):
        loop = False
        #DevModeの場合はシリアライズせず終了する
        if not isDevMode:
            print("終了します")
            with open('lstQuestion.pickle', 'wb') as f:
                pickle.dump(lstQuestion, f)
        else:
            print("DevModeなので、シリアライズせずに終了します")
    elif(mode == ""):
        print("DevMode")
        print("現在までの問題をシリアライズします")
        with open('lstQuestion.pickle', 'wb') as f:
            pickle.dump(lstQuestion, f)
        print("シリアライズ終了")
        print("これ以降の問題追加は、シリアライズされません")
        isDevMode = True
    else:
        print("引数が不正です")