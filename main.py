# -*- coding: utf-8 -*-
import pickle
import csv
import os
import datetime
import random
import platform
class Question():
    def __init__(self, subject, kaisetu , option, ans, numCorrect, numWrong, latestAnsDate, kind):
        self.subject = subject
        self.kaisetu = kaisetu
        self.option = option
        self.ans = ans
        self.numCorrect = numCorrect
        self.numWrong = numWrong
        self.kind = kind
        lstDate = latestAnsDate.split(":")
        self.latestAnsDate = datetime.date(int(lstDate[0]), int(lstDate[1]), int(lstDate[2]))

    def addOption(self, option):
        if self.option[0] == "first":
            self.option[0] = option
        else:
            self.option.append(option)
    def getPercentageOfCorrect(self):
        if self.numCorrect + self.numWrong == 0:
            return 0
        return self.numCorrect / (self.numCorrect+self.numWrong)
    def getDelta(self, now):
        return (now - self.latestAnsDate).days
    def getDataForCSV(self):
        day = self.latestAnsDate.day
        month = self.latestAnsDate.month
        year = self.latestAnsDate.year
        strDate = str(year) + ":" + str(month) + ":" + str(day)
        return [self.subject, self.kaisetu, self.option[0], self.option[1], self.ans, self.numCorrect, self.numWrong, strDate, self.kind]
    def getCountOfAns(self):
        test = int(self.numCorrect) + int(self.numWrong)
        return int(self.numCorrect) + int(self.numWrong)
    def evalShouldAns(self):
        test =  self.getDelta(datetime.date.today())
        if(self.getDelta(datetime.date.today()) == 0):
            return 1
        return (self.getPercentageOfCorrect() * self.getCountOfAns() * 10) / int(self.getDelta(datetime.date.today())) 

def seqQuit():
    input()
    if(platform.system() == "Windows"):
        os.system("cls")
    else:
        os.system("clear")




loop = True
lstQuestion = []
isDevMode = False

with open('lstQuestion.csv', encoding="shift-jis") as f:
    reader = csv.reader(f)
    lstQuestionTmp = [row for row in reader]
for lst in lstQuestionTmp:
    if lst:
        ques = Question(lst[0], lst[1],lst[2:4], lst[4], int(lst[5]), int(lst[6]), lst[7], lst[8])
        lstQuestion.append(ques)

while(loop):
    mode = input("1:問題 2:回答統計 3:終了\n")
    #問題表示
    lstQuestion.sort(key = lambda lst: lst.evalShouldAns())
    if(mode == "1"):
        nCountTodayAns = 0
        for ques in lstQuestion:
            nCountTodayAns += 1
            nCountTodayPerAll = ((nCountTodayAns - 1) / len(lstQuestion)) * 100
            print("現在回答率:" + str(nCountTodayPerAll) + "%")
            print("正答率:" + str(ques.getPercentageOfCorrect() * 100) + "%")
            print("問題: " + ques.subject)
            for opt in ques.option:
                print("選択肢" + str(ques.option.index(opt)+1) + "番目: " + opt)
            userAns = input("正解は？")
            if(userAns == ques.ans):
                print("正解")
                print(ques.kaisetu)
                seqQuit()
                ques.numCorrect += 1
                ques.latestAnsDate = datetime.date.today()
            elif(userAns == "0"):
                print("終了します")
                print("今日の回答数は" + str(nCountTodayAns - 1) + "問でした。")
                print("回答率は" + str(nCountTodayPerAll) + "%です。")
                input()
                break
            else:
                print("不正解")
                print(ques.kaisetu)
                seqQuit()
                ques.numWrong += 1

    #問題統計モード
    elif(mode == "2"):
        length = len(lstQuestion)
        print("全問題数は" + str(length) + "問です")
        print("結果表示開発中")

    #終了処理
    elif(mode == "3"):
        loop = False
        #DevModeの場合はシリアライズせず終了する
        if not isDevMode:
            print("終了します")
            with open('lstQuestion.csv', 'w', encoding="shift-jis") as f:
                writer = csv.writer(f)
                for lst in lstQuestion:
                    writer.writerow(lst.getDataForCSV())

        else:
            print("DevModeなので、シリアライズせずに終了します")
    
    elif(mode == "4"):
        print("問題を全消去します.よろしいですか？")
        ans = input("yes:1/no:0")
        if ans == 1:
            lstQuestion.clear()

    elif(mode == "5"):
        for ques in lstQuestion:
            print(ques.subject)
            print(ques.getPercentageOfCorrect())
            print("日付:" + str(ques.getDelta(datetime.date.today())))

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