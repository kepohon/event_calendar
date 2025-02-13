import os
import pprint
import sys

from .event_calendar import Controller

if __name__ == '__main__':
    print("__main__.py IN")
    print(os.getcwd())
    pprint.pprint(sys.path)
    
    ctrl = Controller()
    ctrl._winRoot.mainloop()

    #main()