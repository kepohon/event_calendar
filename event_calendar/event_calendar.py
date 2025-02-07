# イベントカレンダー （大改造版）
# 2025-02-04 by kepohon

import tkinter as tk
import datetime
import calendar
from tkinter import messagebox
import sqlite3
import os
import pprint
import sys

sys.path.append(os.path.join(os.path.dirname(__file__)))

print(__file__)
pprint.pprint(sys.path)

from ymd import YMD

# 全体を制御するクラス
class Controller:
    _dbName = ""
    
    def __init__(self):
        print("event_calendar.py")
        print(os.getcwd())
        
        dirname = os.path.dirname(__file__)
        self._dbName = os.path.join(dirname, "memo.db")
        
        self._today = YMD()         # 今日の日付
        self._currentDay = YMD()    # プログラムで指定されている日付
        
        year = self._today.year
        month = self._today.month
        day = self._today.day
        
        # ルートウィンドウの生成
        self._winRoot = WindowRoot()
        
        # 左側フレームの生成
        self._frameLeft = FrameLeft(self._winRoot, self)
        self._frameLeft.grid( row=0, column=0, padx=10 )
        
        # カレンダーフレームの生成
        self._frameCalendar = FrameCalendar(self._frameLeft, self)
        self._frameCalendar.grid( row=1, column=0, columnspan=3 )
        
        # カレンダーの日付を表示する
        self._frameCalendar.displayCalendar(0, year, month, day)
        
        # 右側フレームの生成
        self._frameRight = FrameRight(self._winRoot, self, self._today)
        self._frameRight.grid( row=0, column=1 )
        
        # メモフレームの生成
        self._frameMemo = FrameMemo(self._frameRight, self, self._currentDay)
        self._frameMemo.grid( row=0, column=0, pady=10 )
        
    # 前年に戻るボタンが押されたときの処理
    def clickButtonPreviousYear(self):
        print("previous year button")
        year = self._currentDay.year
        month = self._currentDay.month
        day = self._currentDay.day
        day = 1
        year -= 1
        self._currentDay.year = year
        self._currentDay.month = month
        self._currentDay.day = day
        print(f"Y:{year}, M:{month}")
        self._frameCalendar.displayCalendar(0, year, month, day)
    
    # 前月に戻るボタンが押されたときの処理
    def clickButtonPreviousMonth(self):
        print("previous button")
        year = self._currentDay.year
        month = self._currentDay.month
        day = self._currentDay.day
        day = 1
        month -= 1
        if month < 1:
            year -= 1
            month = 12
        self._currentDay.year = year
        self._currentDay.month = month
        self._currentDay.day = day
        print(f"Y:{year}, M:{month}")
        self._frameCalendar.displayCalendar(0, year, month, day)
    
    # 次月へボタンが押されたときの処理
    def clickButtonNextMonth(self):
        print("next button")
        year = self._currentDay.year
        month = self._currentDay.month
        day = self._currentDay.day
        day = 1
        month += 1
        if month > 12:
            year += 1
            month = 1
        self._currentDay.year = year
        self._currentDay.month = month
        self._currentDay.day = day
        print(f"Y:{year}, M:{month}")
        self._frameCalendar.displayCalendar(0, year, month, day)
    
    # 次年へボタンが押されたときの処理
    def clickButtonNextYear(self):
        print("next year button")
        year = self._currentDay.year
        month = self._currentDay.month
        day = self._currentDay.day
        day = 1
        year += 1
        self._currentDay.year = year
        self._currentDay.month = month
        self._currentDay.day = day
        print(f"Y:{year}, M:{month}")
        self._frameCalendar.displayCalendar(0, year, month, day)
    
    # カレンダー上の日付ラベルが押されたときの処理
    def clickLabelDay(self, day):
        print(f"clicked day button: {day}")
        # event: label_dayオブジェクト
        
        self._currentDay.day = day
        year = self._currentDay.year
        month = self._currentDay.month
        
        self._frameMemo.setLabelMemoTitle(f"{year}年{month}月{day}日のメモ")
        
        # 画面のメモタイトルを更新する
        self._frameRight._textMemo.delete( '1.0', 'end' )
        self._frameRight._textMemo.insert( '1.0', self.get_memo_from_db(year, month, day) )
    
    # カレンダーのタイトルがクリックされたら、今日に戻る
    def click_label_calendar_title(self, event):
        # カレント年月日を今日の年月日に戻す
        year = self._today.year
        month = self._today.month
        day = self._today.day
        self._currentDay.year = year
        self._currentDay.month = month
        self._currentDay.day = day
        
        # カレンダー再表示
        self._frameCalendar.displayCalendar(0, year, month, day)
        
        # タイトル文字列の作成
        self._frameMemo.setLabelMemoTitle(f"{year}年{month}月{day}日のメモ")
        
        # DBから年月日が一致するメモデータを取得してテキストエリアにセットする
        self._frameRight._textMemo.delete( '1.0', 'end' )
        self._frameRight._textMemo.insert( '1.0', self.get_memo_from_db(year, month, day) )
    
    # 画面のメモデータをDBに保存、または削除する
    def saveMemo(self):
        print("save memo")
        pass
        year = self._currentDay.year
        month = self._currentDay.month
        day = self._currentDay.day
        memoText = self._frameRight._textMemo.get( '1.0', 'end-1c' )
        if self.is_there_memo_with_that_date( year, month, day ):
            # DBに、指定した年月日のメモがある場合の処理
            
            if memoText == "":
                # 画面のメモテキストが空の場合、レコードを削除する
                conn = sqlite3.connect(self._dbName)
                cur = conn.cursor()
                sql = f"delete from daily where year = {year} and month = {month} and day = {day};"
                results = cur.execute(sql)
                conn.commit()
                conn.close()
                self._frameCalendar.displayCalendar(0, year, month, day)
                return
                
            # 画面のメモデータが有る場合はレコードを更新する
            conn = sqlite3.connect(self._dbName)
            cur = conn.cursor()
            
            sql = 'select * from daily where year = ? and month = ? and day = ?;'
            results = cur.execute(sql, (year, month, day,) )
            for row in results:
                id = row[0]     # メモデータ在りのidを取得する
            sql = 'update daily set memo=? where id=?'
            cur.execute( sql, ( memoText, id, ) )
            conn.commit()
            conn.close()
            
        else:
            # DBに該当する年月日のメモデータが無い場合、レコードを挿入する
            if memoText == "":
                # 画面のメモテキストが空の場合、何もしない
                return
            
            # 画面のメモデータが有る場合、レコードを挿入する
            conn = sqlite3.connect(self._dbName)
            cur = conn.cursor()
            sql = 'replace into daily(year, month, day, memo) values(?, ?, ?, ?)'
            cur.execute( sql, ( year, month, day, memoText ) )
            conn.commit()
            conn.close()
            messagebox.showinfo( 'メッセージ', 'データを保存しました' )
            self._frameCalendar.displayCalendar(0, year, month, day)

    # データベースに引数の日付のメモがあればTrue、なければFalseを返す関数
    def is_there_memo_with_that_date( self, y, m, d ):
        if self.get_memo_from_db( y, m, d ) != '':
            return True
        return False
    
    # 日付を引数にしてメモを取得する関数
    def get_memo_from_db(self, year, month, day):
        conn = sqlite3.connect(self._dbName)
        cur = conn.cursor()
        today_memo = ''
        sql = 'select * from daily where year = ? and month = ? and day = ?;'
        results = cur.execute(sql, (year, month, day,) )
        for row in results:
            self._currentID = row[0]
            today_memo = row[4]
        conn.close()
        return today_memo
    

class WindowRoot(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self._winRoot = self
        
        self.geometry("480x280")
        self.title("イベントカレンダー")
        self.resizable(0, 0)
        self.config(bg="yellow")
    
class FrameLeft(tk.Frame):
    _master = None              # rootウィンドウ
    _winRoot = None             # rootウィンドウ
    _frameCalendar = None       # カレンダーフレームオブジェクト
    
    # 各ウィジェットのオブジェクト
    _labelCalendarTitle = None  # カレンダーのタイトルラベル
    _buttonPreviousMonth = None # 前月ボタンオブジェクト
    _buttonNextMonth = None     # 次月ボタンオブジェクト
    
    def __init__(self, master=None, controller=None):
        super().__init__(master)
        
        self._master = master
        self._winRoot = master
        self._ctrl = controller
        
        self.createWidget()
    
    def createWidget(self):
        # カレンダータイトル
        self._labelCalendarTitle = tk.Label( self, font=('', 10))
        self._labelCalendarTitle.grid( row=0, column=2 )
        self._labelCalendarTitle.bind( '<ButtonRelease-1>', self._ctrl.click_label_calendar_title )
        
        # 前年ボタン
        self._buttonPreviousYear = tk.Button(
            self,
            text='<<',
            font=('', 10),
            command = lambda: self._ctrl.clickButtonPreviousYear()
            )
        self._buttonPreviousYear.grid( row=0, column=0, pady=10 )
        
        # 前月ボタン
        self._buttonPreviousMonth = tk.Button(
            self,
            text='<',
            font=('', 10),
            command = lambda: self._ctrl.clickButtonPreviousMonth()
            )
        self._buttonPreviousMonth.grid( row=0, column=1, pady=10 )
        
        # 次月ボタン
        self._buttonNextMonth = tk.Button(
            self,
            text='>',
            font=('', 10),
            command = lambda: self._ctrl.clickButtonNextMonth()
            )
        self._buttonNextMonth.grid( row=0, column=3 )
        
        # 次年ボタン
        self._buttonNextYear = tk.Button(
            self,
            text='>>',
            font=('', 10),
            command= lambda: self._ctrl.clickButtonNextYear()
            )
        self._buttonNextYear.grid( row=0, column=4 )
    

class FrameCalendar(tk.Frame):
    # 表示するカレンダーの生成
    _WEEK = [ '日', '月', '火', '水', '木', '金', '土' ]
    _WEEK_COLOR = [ 'red', 'black', 'black', 'black', 'black', 'black', 'blue' ]
    #_dbName = "memo.db"
    
    def __init__(self, master=None, controller=None):
        super().__init__(master)
        self._master = master
        self._ctrl = controller
        self._frameLeft = master
        self._winRoot = master._master
    
    # カレンダーを表示する
    def displayCalendar(self, arg, year, month, day ):
        today = self._ctrl._today
        
        self._master._labelCalendarTitle['text'] = f"{year}年{month}月"
        
        # カレンダーオブジェクトの作成
        self._objectCalendar = calendar.Calendar( firstweekday=6 )
        
        # 該当年月のカレンダーを取得
        self._calendarData = self._objectCalendar.monthdayscalendar( year, month )
        
        # カレンダーフレーム上のウィジェットをすべて削除する
        for widget in self.winfo_children():
            widget.destroy()
        
        # カレンダーの曜日行の表示
        self._currentRow = 0
        # 曜日配列を取得
        for index, value in enumerate( self._WEEK ):
            # enumerate関数は、インデックスと要素を同時に取得できる関数
            
            # 曜日表示行の設定と配置
            self._labelDay = tk.Label(
                self,
                text = value,
                font = ( '', 10 ),
                width = 3,
                fg = self._WEEK_COLOR[index] )
            # 曜日を配置する
            self._labelDay.grid( row = self._currentRow, column = index, pady = 1 )
        
        # カレンダーの日付を表示
        self._currentRow = 1
        # カレンダー配列を取得
        for week in self._calendarData:
            for index, dayNumber in enumerate( week ):
                # enumerate関数は、インデックスと要素を同時に取得できる関数
                self._dayNumber = ' ' if dayNumber == 0 else dayNumber
                self._labelDay = tk.Label(
                    self,
                    text = self._dayNumber,
                    font = ( '', 10 ),
                    fg = self._WEEK_COLOR[index],
                    borderwidth = 1 )
                
                # 日付が今日なら枠線を付ける
                if ( year, month, self._dayNumber ) == ( today.year, today.month, today.day ):
                    self._labelDay[ 'relief' ] = 'solid'
                
                # 現在の日付のデータが有れば、背景色を黄色にする
                if self._ctrl.is_there_memo_with_that_date( year, month, self._dayNumber ):
                    self._labelDay[ 'background' ] = 'yellow'
                
                # 日付が押されたときの処理を設定する
                self._labelDay.bind( '<ButtonRelease-1>', self.clickLabelDay )
                
                # 日付を配置する
                self._labelDay.grid( row=self._currentRow, column=index, padx=2, pady=1 )
            
            # 次の行へ
            #self._currentRow = self._currentRow + 1
            self._currentRow += 1
    
    # 日付がクリックされたとき
    def clickLabelDay(self, event):
        print(f"event.widget['text']:{event.widget['text']}")
        self._ctrl.clickLabelDay(event.widget['text'])
    
    
class FrameRight(tk.Frame):
    
    def __init__(self, master=None, controller=None, today=None):
        super().__init__(master)
        #self._master = master
        self._winRoot = master
        self._ctrl = controller
        self._today = today
        #self._frameLeft = master._frameLeft
        
        self.createWidget()
        
    
    def createWidget(self):
        # メモ用のTextウィジェット
        self._textMemo = tk.Text(
            self,
            width=30,
            height=14)
        self._textMemo.grid( row=4, column=0 )
        
        # メモ表示画面のスクロールバーオブジェクト
        self._scrollbarV = tk.Scrollbar( self,
                                    orient = tk.VERTICAL,
                                    command = self._textMemo.yview )
        self._scrollbarV.grid( row=4, column=1, sticky=tk.N+tk.S )
        
        self._textMemo["yscrollcommand"] = self._scrollbarV.set
        self._textMemo.insert('1.0', self._ctrl.get_memo_from_db( self._today.year, self._today.month, self._today.day ))
        
    

class FrameMemo(tk.Frame):
    _master = None
    _frameRight = None
    _winRoot = None
    
    _labelMemoTitle = None
    _buttonSave = None
    
    def __init__(self, master=None, controller=None, currentDay=None):
        super().__init__(master)
        self._master = master
        self._frameRight = master
        self._ctrl = controller
        self._currentDay = currentDay
        
        self.createWidget()
    
    def createWidget(self):
        year = self._currentDay.year
        month = self._currentDay.month
        day = self._currentDay.day
        self._labelMemoTitle = tk.Label(
                    self,
                    text = f"{year}年{month}月{day}日のメモ",
                    font = ('', 12 )
                    )
        self._labelMemoTitle.grid( row=0, column=0, padx=20 )
        
        # 保存ボタン
        self._buttonSave = tk.Button(
            self,
            text = '保存',
            command = lambda: self._ctrl.saveMemo() )
        self._buttonSave.grid( row=0, column=1 )
        
        self.grid( row=0, column=0, pady=10 )
        
    def setLabelMemoTitle(self, str):
        self._labelMemoTitle['text'] = str
    
"""
class YMD:
    _year = 0
    _month = 0
    _day = 0
    
    def __init__(self):
        self._year = datetime.date.today().year
        self._month = datetime.date.today().month
        self._day = datetime.date.today().day
    
    # Getter
    @property
    def year(self):
        return self._year
    
    @property
    def month(self):
        return self._month
    
    @property
    def day(self):
        return self._day
    
    # Setter
    @year.setter
    def year(self, value):
        if value >= 0 and value < 10000:
            self._year = value
        else:
            print("year number error!")
    
    @month.setter
    def month(self, value):
        if value >= 1 and value <= 12:
            self._month = value
        else:
            print("month number error!")
    
    @day.setter
    def day(self, value):
        if value >= 1 and value <= 31:
            self._day = value
        else:
            print("day number error!")
"""

if __name__ == '__main__':
    #from .ymd import YMD
    #from ymd import YMD
    ctrl = Controller()
    ctrl._winRoot.mainloop()
