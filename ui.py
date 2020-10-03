# 此文件为UI程序
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from mywidgets import *


class BookManager(QMainWindow):
    def __init__(self):
        super(BookManager, self).__init__()
        self.toolbar = MyToolBar()
        self.addToolBar(self.toolbar)
        self.generateToolBar()

        self.searchLine = MySearch()
        self.treeView = MyTree()
        self.treeView.setMaximumWidth(700)
        self.treeView.setMinimumWidth(200)
        tempwidget = QWidget()
        # tempwidget.setStyleSheet("QLabel{border:2px solid red;}")
        self.booksView = MyGrid()
        self.infoView = MyList()
        self.infoView.setMaximumWidth(700)
        self.infoView.setMinimumWidth(200)

        self.scrollarea = QScrollArea()
        self.scrollarea.setMinimumWidth(1000)
        self.scrollarea.setMaximumWidth(1200)
        tempwidget.setLayout(self.booksView)
        self.scrollarea.setWidget(tempwidget)

        splitter1 = QSplitter(Qt.Horizontal)
        splitter1.addWidget(self.scrollarea)
        splitter1.addWidget(self.infoView)
        splitter1.setSizes([1000, 400])
        splitter2 = QSplitter(Qt.Horizontal)
        splitter2.addWidget(self.treeView)
        splitter2.addWidget(splitter1)
        splitter2.setSizes([300, 1400])

        self.VBox = QVBoxLayout()
        self.VBox.addWidget(self.searchLine)
        self.VBox.addWidget(splitter2)
        self.mainwidget = QWidget()
        self.mainwidget.setLayout(self.VBox)
        self.setCentralWidget(self.mainwidget)

        self.setWindowTitle("图书管理系统")
        desktop = QApplication.desktop()
        rect = desktop.availableGeometry()
        self.setWindowIcon(QIcon('img/icon-2.png'))
        self.setGeometry(rect)
        self.show()

    def generateToolBar(self):
        self.toolbar.addbook.triggered.connect(self.addBook)
        self.toolbar.inbook.triggered.connect(self.inBook)
        self.toolbar.editbook.triggered.connect(self.editBook)
        self.toolbar.sortbooks.triggered.connect(self.sortBooks)
        self.toolbar.readbook.triggered.connect(self.readBook)
        self.toolbar.convertbook.triggered.connect(self.convertBook)
        self.toolbar.deletebook.triggered.connect(self.deleteBook)
        self.toolbar.booklist.triggered.connect(self.addBookList)
        self.toolbar.bookshelf.triggered.connect(self.openBookShelf)
        self.toolbar.export.triggered.connect(self.export)
        self.toolbar.share.triggered.connect(self.share)
        self.toolbar.star.triggered.connect(self.giveusStar)
        self.toolbar.gethelp.triggered.connect(self.getHelp)
        self.toolbar.setting.triggered.connect(self.setSetting)

    def addBook(self):
        pass

    def inBook(self):
        pass

    def editBook(self):
        pass

    def sortBooks(self):
        pass

    def readBook(self):
        pass

    def convertBook(self):
        pass

    def deleteBook(self):
        pass

    def addBookList(self):
        pass

    def openBookShelf(self):
        pass

    def export(self):
        pass

    def share(self):
        pass

    def giveusStar(self):
        pass

    def getHelp(self):
        pass

    def setSetting(self):
        pass


