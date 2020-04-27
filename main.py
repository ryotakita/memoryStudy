# -*- coding: utf-8 -*-
import pickle
import csv
import os
import datetime
import random
import platform
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
class Question():
    def __init__(self, subject, kaisetu , option, ans, numCorrect, numWrong, latestAnsDate, kind):
        self.subject = subject
        self.kaisetu = kaisetu
        self.option = option
        self.ans = ans
        self.numCorrect = numCorrect
        self.numWrong = numWrong
        self.kind = kind
        if latestAnsDate == "":
            self.latestAnsDate = datetime.date(1996, 8, 20)
        else:
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
    def IsOk(self):
        return (self.getPercentageOfCorrect() > 0.9 and self.getCountOfAns() > 10)
    def IsAlmostOk(self):
        return (not self.IsOk()) and (self.getPercentageOfCorrect() > 0.8 and self.getCountOfAns() > 4)
    def getCountOfAns(self):
        return self.numCorrect + self.numWrong
    def evalShouldAns(self):
        if(self.getDelta(datetime.date.today()) == 0):
            return 1
        return (self.getPercentageOfCorrect() * self.getCountOfAns() * 10) / int(self.getDelta(datetime.date.today())) 

def seqQuit():
    input()
    if(platform.system() == "Windows"):
        os.system("cls")
    else:
        os.system("clear")

def createGraphData(lstOk, lstAlmostOk, lstNg, lstKind):
    for kind in lstKind:
        numOfOk = len(list(filter(lambda x: x.kind == kind and x.IsOk(), lstQuestion)))
        numOfAlmostOk = len(list(filter(lambda x: x.kind == kind and x.IsAlmostOk(), lstQuestion)))
        numOfNg = len(list(filter(lambda x: x.kind == kind and not x.IsAlmostOk() and not x.IsOk(), lstQuestion)))
        lstOk.append(numOfOk)
        lstNg.append(numOfNg)
        lstAlmostOk.append(numOfAlmostOk)

def showHistory():
    df = pd.read_csv('history.csv',
                     index_col='date',
                     parse_dates=True)
    df = df.set_index([df.index.year, df.index.month, df.index.day, df.index])
    df.index.names = ["year", "month", "day", "date"]

    # 月毎に集計
    summary = df.sum(level=('year', 'month', 'day'))        # 年月単位で合計を集計する
    summary = summary.reset_index()                  # マルチインデックスを解除する
    summary['year'] = summary['year'].astype(str)    # 「year」列を文字列にする
    summary['month'] = summary['month'].astype(str)  # 「month」列を文字列にする
    summary['day'] = summary['day'].astype(str)
    
    # 「year」と「month」列を「-」で繋ぎ、タイムスタンプに変換する
    date = pd.to_datetime(summary['year'].str.cat([summary['month'], summary['day']], sep='-'))
    
    # プロット用のデータをSeriesで抽出する
    numQuestion = summary['numQuestion']
    almostOK = summary['almostOK']
    OK = summary['OK']
    
    # ここからグラフ描画
    # フォントの種類とサイズを設定する
    plt.rcParams['font.size'] = 14
    plt.rcParams['font.family'] = 'Times New Roman'
    
    # 目盛を内側にする
    plt.rcParams['xtick.direction'] = 'in'
    plt.rcParams['ytick.direction'] = 'in'
    
    # グラフの上下左右に目盛線を付ける
    fig = plt.figure(figsize=(10, 3))
    ax1 = fig.add_subplot(111)
    ax1.yaxis.set_ticks_position('both')
    ax1.xaxis.set_ticks_position('both')
    
    # 軸のラベルを設定する
    ax1.set_ylabel('number of question')
    
    # データプロット
    ax1.plot(date, numQuestion, label='numQuestion', lw=2)
    ax1.plot(date, almostOK, label='almostOK', lw=1)
    ax1.plot(date, OK, label='OK', lw=1)
    
    # グラフを表示する
    plt.legend()
    plt.legend(bbox_to_anchor=(0, 1), loc='upper left', borderaxespad=0)
    plt.show()

    





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
                print("不正解!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                print(ques.kaisetu)
                input("")
                seqQuit()
                ques.numWrong += 1

    #問題統計モード
    elif(mode == "2"):
        length = len(lstQuestion)
        print("全問題数は" + str(length) + "問です")
        lstKind = ['計画', '建築史', '環境', '法規', '構造', '施工']
        lstOk = []
        lstAlmostOk = []
        lstNg = []
        createGraphData(lstOk, lstAlmostOk, lstNg, lstKind)
        dataset = pd.DataFrame([lstNg, lstAlmostOk, lstOk], 
                       #TODO:本当はlstKIndと合わせたいが日本語対応してないのでこれでしのぐ
                       columns=['Plan', 'History' ,'Environment', 'Law', 'Structure', 'Construction'], 
                       index=['NG', 'AlmostOK', 'OK'])
        fig, ax = plt.subplots(figsize=(10, 8))
        for i in range(len(dataset)):
            ax.bar(dataset.columns, dataset.iloc[i], bottom=dataset.iloc[:i].sum())
        ax.set(xlabel='Subject', ylabel='AllQuestion')
        ax.legend(dataset.index)
        plt.show()
        showHistory()
        

    #終了処理
    elif(mode == "3"):
        loop = False
        #DevModeの場合はシリアライズせず終了する
        #TODO:ここらへん汚すぎ
        if not isDevMode:
            print("終了します")
            lstQuestion.sort(key = lambda lst: lst.evalShouldAns()) #最新の順番に整理するためソート
            with open('lstQuestion.csv', 'w', encoding="shift-jis") as f:
                writer = csv.writer(f)
                for lst in lstQuestion:
                    writer.writerow(lst.getDataForCSV())
            #とりあえず日付ごとの状況を記録しておく
            lstHistory = []
            with open('history.csv', 'r', encoding='shift-jis') as f:
                reader = csv.reader(f)
                lstHistory = [row for row in reader]
                day = str(datetime.date.today().day)
                month = str(datetime.date.today().month)
                year = str(datetime.date.today().year)
                for lst in lstHistory:
                    if(lst and lst[0] == year+'-'+month+'-'+day):
                        lstHistory.remove(lst)

            with open('history.csv', 'w', encoding="shift-jis") as f:
                writer = csv.writer(f)
                nCount = 1
                writer.writerow(['date', 'numQuestion', 'almostOK', 'OK'])
                for lst in lstHistory:
                    if(nCount == 1):
                        nCount += 1
                        continue
                    if(lst):
                        writer.writerow(lst)
                day = datetime.date.today().day
                month = datetime.date.today().month
                year = datetime.date.today().year
                strDate = str(year) + "-" + str(month) + "-" + str(day)
                numOfOk = len(list(filter(lambda x: x.IsOk(), lstQuestion)))
                numOfAlmostOk = len(list(filter(lambda x: x.IsAlmostOk(), lstQuestion)))
                numOfNg = len(list(filter(lambda x: not x.IsAlmostOk() and not x.IsOk(), lstQuestion)))
                writer.writerow([strDate, numOfNg, numOfAlmostOk, numOfOk])

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

    #異常
    else:
        print("引数が不正です")
