import pickle
import os
import datetime
class Question():
    def __init__(self, subject):
        self.subject = subject
        self.option = ["first"]
        self.ans = 0
        self.numCorrect = 0
        self.numWrong = 0
        self.latestAnsDate = datetime.datetime.now()

    def addOption(self, option):
        if self.option[0] == "first":
            self.option[0] = option
        else:
            self.option.append(option)


loop = True
lstQuestion = []
isDevMode = False

if os.path.getsize('lstQuestion.pickle') > 0:
    with open('lstQuestion.pickle', 'rb') as f:
        lstQuestion = pickle.load(f)

while(loop):
    mode = input("1:問題 2:問題追加 3:終了\n")
    #問題表示
    if(mode == "1"):
        for ques in lstQuestion:
            print("問題: " + ques.subject)
            for opt in ques.option:
                print("選択肢" + str(ques.option.index(opt)+1) + "番目: " + opt)
            userAns = input("正解は？")
            if(int(userAns) == ques.ans):
                print("正解")
            else:
                print("不正解")

    #問題追加モード
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
        Ans = input("正解の選択肢を入力してください")
        question.ans = int(Ans)
        lstQuestion.append(question)


    #終了処理
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

    #異常
    else:
        print("引数が不正です")