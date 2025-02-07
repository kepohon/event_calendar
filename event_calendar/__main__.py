import os
#from .ymd import *
from .event_calendar import Controller

if __name__ == '__main__':
    print("__main__.py")
    print(os.getcwd())
    
    ctrl = Controller()
    ctrl._winRoot.mainloop()

    #main()