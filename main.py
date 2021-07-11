from signal_slots import MyWindow
import  sys
from PyQt5.QtWidgets import QApplication
import os
import sys

import PyQt5

dirname = os.path.dirname(PyQt5.__file__)
plugin_path = os.path.join(dirname,'Qt', 'plugins', 'platforms')
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = plugin_path



if __name__ == '__main__':
    myapp = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(myapp.exec_()) 