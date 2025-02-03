# カレンダーイベント
# 2025-01-24 by kepohon

import tkinter as tk
import datetime
import calendar
from tkinter import messagebox
import sqlite3

class EventCalendar(tk.Tk): # tkinterを継承
    _dbName = "memo.db"
    
    _year = [0] * 2
    _month = [0] * 2
    _day = None
    _today = None
    _clickedDay = None
    _currentID = None
    
    _winRoot = None
    
    def __init__(self):
        super().__init__()
        self._winRoot = self
        
        self.geometry("480x280")
        self.title("イベントカレンダー")
        self.resizable(0, 0)
        self.config(bg="yellow")
        
        self.getTodaysDate()
        
        self._frameLeft = FrameLeft(self)
        self._frameLeft.grid( row=0, column=0, padx=10 )
        
        self._frameRight = FrameRight(self)
        self._frameRight.grid( row=0, column=1 )
        
        pass
        
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
    
    # 今日の年月日を取得する
    def getTodaysDate(self):
        self._year = [datetime.date.today().year] * 2
            # _year[0] :: 変数として、 _year[1] :: バックアップ
        self._month = [datetime.date.today().month] * 2
            # _month[0] :: 変数として、 _month[1] : バックアップ
        self._today = datetime.date.today().day     # 今日の日付バックアップ
        self._clickedDay = self._today
        self._day = self._today
    
    def setCurrentYMD(self, year, month, day):
        self._year[0] = year
        self._year[1] = year
        self._month[0] = month
        self._month[1] = month
        self._day = day
        self._today = day
    
    # 日付文字列を作る関数
    def make_text_1( self, y, m, d ):
        return str( y ) + '年' + str( m ) + '月' + str( d ) + '日'
    
    # メモデータの保存（保存ボタンのが押されたときの処理）
    def saveMemo( self, year, month, day ):
        if self.is_there_memo_with_that_date( year, month, day ):
            if self._frameRight._textMemo.get( '1.0', 'end-1c' ) == "":
                # メモテキストが空の場合、レコードの削除処理
                conn = sqlite3.connect(self._dbName)
                cur = conn.cursor()
                sql = f"delete from daily where year = {year} and month = {month} and day = {day};"
                results = cur.execute(sql)
                conn.commit()
                conn.close()
                self._frameLeft._frameCalendar.displayCalendar( 0 )
                return
                
            # メモデータありの場合（レコードの更新）
            conn = sqlite3.connect(self._dbName)
            cur = conn.cursor()
            
            sql = 'select * from daily where year = ? and month = ? and day = ?;'
            results = cur.execute(sql, (year, month, day,) )
            for row in results:
                id = row[0]     # メモデータ在りのidを取得する
            sql = 'update daily set memo=? where id=?'
            cur.execute( sql, ( self._frameRight._textMemo.get( '1.0', 'end-1c' ), id, ) )
            conn.commit()
            conn.close()
        else:
            # メモデータなしの場合（レコードの挿入）
            if self._frameRight._textMemo.get( '1.0', 'end-1c' ) == "":
                # メモテキストが空の場合、何もしない
                return
            
            conn = sqlite3.connect(self._dbName)
            cur = conn.cursor()
            sql = 'replace into daily(year, month, day, memo) values(?, ?, ?, ?)'
            cur.execute( sql, ( year, month, day, self._frameRight._textMemo.get( '1.0', 'end-1c' ) ) )
            conn.commit()
            conn.close()
            messagebox.showinfo( 'メッセージ', 'データを保存しました' )
            self._frameLeft._frameCalendar.displayCalendar( 0 )


class FrameLeft(tk.Frame):
    _master = None              # rootウィンドウ
    _winRoot = None             # rootウィンドウ
    _frameCalendar = None       # カレンダーフレームオブジェクト
    
    # 各ウィジェットのオブジェクト
    _labelCalendarTitle = None  # カレンダーのタイトルラベル
    _buttonPreviousMonth = None # 前月ボタンオブジェクト
    _buttonNextMonth = None     # 次月ボタンオブジェクト
    
    def __init__(self, master=None):
        super().__init__(master)
        self._master = master
        self._winRoot = master
        #self._frameRight = master._frameRight
        
        self.createWidget()
        
        self._frameCalendar = FrameCalendar(self)
        self._frameCalendar.grid( row=1, column=0, columnspan=3 )
        
        self._master.setCurrentYMD(self._master._year[0], self._master._month[0], self._master._today)
        self._frameCalendar.displayCalendar(0)
    
    def createWidget(self):
        # カレンダータイトル
        self._labelCalendarTitle = tk.Label( self, font=('', 10))
        self._labelCalendarTitle.grid( row=0, column=1 )
        self._labelCalendarTitle.bind( '<ButtonRelease-1>', self.click_label_calendar_title )
        
        # 前月ボタン
        self._buttonPreviousMonth = tk.Button(
            self,
            text='<',
            font=('', 10),
            command=lambda:self._frameCalendar.displayCalendar(-1))
        self._buttonPreviousMonth.grid( row=0, column=0, pady=10 )
        
        # 次月ボタン
        self._buttonNextMonth = tk.Button(
            self,
            text='>',
            font=('', 10),
            command=lambda:self._frameCalendar.displayCalendar(1))
        self._buttonNextMonth.grid( row=0, column=2 )
        
    # カレンダーのタイトルがクリックされたら、今日に戻る
    def click_label_calendar_title(self, event):
        
        self._master._clickedDay = self._master._today
        self._master._year[0] = self._master._year[1]
        self._master._month[0] = self._master._month[1]
        self._frameCalendar.displayCalendar(0)
        
        self._master._frameRight._frameMemo.setLabelMemoTitle(self._master.make_text_1( self._master._year[0], self._master._month[0], self._master._clickedDay ) + 'のメモ')
        
        
        
        #self._labelMemoTitle['text'] = self._master.make_text_1( self._master._year[0], self._master._month[0], self._master._clickedDay ) + 'のメモ'
        self._master._frameRight._textMemo.delete( '1.0', 'end' )
        self._master._frameRight._textMemo.insert( '1.0', self._master.get_memo_from_db( self._master._year[0], self._master._month[0], self._master._clickedDay ) )
    

class FrameCalendar(tk.Frame):
    # 表示するカレンダーの生成
    _WEEK = [ '日', '月', '火', '水', '木', '金', '土' ]
    _WEEK_COLOR = [ 'red', 'black', 'black', 'black', 'black', 'black', 'blue' ]
    
    def __init__(self, master=None):
        super().__init__(master)
        self._master = master
        self._frameLeft = master
        self._winRoot = master._master
    
    # カレンダーを表示する
    def displayCalendar( self, arg ):
        self._winRoot._month[0] += arg
        
        if self._winRoot._month[0] < 1:
            #self._month[0], self._year[0] = 12, self._year[0] - 1
            self._winRoot._month[0] = 12
            self._winRoot._year[0] -= 1
        elif self._master._master._month[0] > 12:
            #self._month[0], self._year[0] = 1, self._year[0] + 1
            self._winRoot._month[0] = 1
            self._winRoot._year[0] += 1
    
        self._master._labelCalendarTitle['text'] = str( self._winRoot._year[0] ) + '年' + str( self._winRoot._month[0] ) + '月'
        
        # カレンダーオブジェクトの作成
        self._objectCalendar = calendar.Calendar( firstweekday=6 )
        
        # 該当年月のカレンダーを取得
        self._calendarData = self._objectCalendar.monthdayscalendar( self._winRoot._year[0], self._winRoot._month[0] )
        
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
                if ( self._winRoot._year[0], self._winRoot._month[0], self._dayNumber ) == ( self._winRoot._year[1], self._winRoot._month[1], self._winRoot._today ):
                    self._labelDay[ 'relief' ] = 'solid'
                
                # 現在の日付のデータが有れば、背景色を黄色にする
                if self._winRoot.is_there_memo_with_that_date( self._winRoot._year[0], self._winRoot._month[0], self._dayNumber ):
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
        # event: label_dayオブジェクト
        
        self._winRoot._clickedDay = event.widget['text']
        n = str( self._winRoot._year[0] ) + '_' + str( self._winRoot._month[0] ) + '_' + str( self._winRoot._clickedDay )
        
        self._winRoot._frameRight._frameMemo.setLabelMemoTitle(self._winRoot.make_text_1( self._winRoot._year[0], self._winRoot._month[0], self._winRoot._clickedDay ) + 'のメモ')
        
        #self._labelMemoTitle['text'] = self._master._master.make_text_1( self._master._master._year[0], self._master._master._month[0], self._master._master._clickedDay ) + 'のメモ'
        self._winRoot._frameRight._textMemo.delete( '1.0', 'end' )
        self._winRoot._frameRight._textMemo.insert( '1.0', self._winRoot.get_memo_from_db( self._winRoot._year[0], self._winRoot._month[0], self._winRoot._clickedDay ) )
    
    
class FrameRight(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self._master = master
        self._winRoot = master
        #self._frameLeft = master._frameLeft
        
        self.createWidget()
        
        self._frameMemo = FrameMemo(self)
        self._frameMemo.grid( row=0, column=0, pady=10 )
        
    
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
        self._textMemo.insert('1.0', self._master.get_memo_from_db( self._master._year[0], self.master._month[0], self._master._today ))
        
    

class FrameMemo(tk.Frame):
    _master = None
    _frameRight = None
    _winRoot = None
    
    _labelMemoTitle = None
    _buttonSave = None
    
    def __init__(self, master=None):
        super().__init__(master)
        self._master = master
        self._frameRight = master
        self._winRoot = master._master
        
        self.createWidget()
    
    def createWidget(self):
        self._labelMemoTitle = tk.Label(
                    self,
                    text = self._winRoot.make_text_1( self._winRoot._year[0], self._winRoot._month[0], self._winRoot._clickedDay ) + 'のメモ',
                    font = ('', 12 )
                    )
        self._labelMemoTitle.grid( row=0, column=0, padx=20 )
        
        # 保存ボタン
        self._buttonSave = tk.Button(
            self,
            text = '保存',
            command = lambda: self._winRoot.saveMemo( self._winRoot._year[0], self._winRoot._month[0], self._winRoot._clickedDay ) )
        self._buttonSave.grid( row=0, column=1 )
        
        self.grid( row=0, column=0, pady=10 )
        
    def setLabelMemoTitle(self, str):
        self._labelMemoTitle['text'] = str
    

if __name__ == '__main__':
    ec = EventCalendar()
    ec.mainloop()
