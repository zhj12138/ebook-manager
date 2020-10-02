# 主程序
from ui import BookManager
from PyQt5.QtWidgets import QApplication
import sys


app = QApplication(sys.argv)
bookManager = BookManager()
sys.exit(app.exec_())


