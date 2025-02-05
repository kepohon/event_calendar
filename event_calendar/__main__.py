from .event_calendar import Controller

if __name__ == '__main__':
    print("__main__.py")
    print("  メインプログラムの起点。")
    print("event calendar project")
    
    ctrl = Controller()
    ctrl._winRoot.mainloop()

    #main()