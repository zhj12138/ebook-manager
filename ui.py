# 此文件为UI程序
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from mywidgets import *


class BookManager(QMainWindow):
    def __init__(self):
        super(BookManager, self).__init__()
        self.toolbar = self.addToolBar("工具栏")
        self.generateToolBar()
        self.searchLine = MySearch()
        self.treeView = MyTree()
        self.booksView = MyTable()
        self.infoView = MyList()
        self.HBox = QHBoxLayout()
        self.VBox = QVBoxLayout()
        self.HBox.addWidget(self.treeView, stretch=1)
        self.HBox.addWidget(self.booksView, stretch=3)
        self.HBox.addWidget(self.infoView, stretch=1)
        self.VBox.addWidget(self.searchLine, stretch=0)
        self.widget = QWidget()
        self.widget.setLayout(self.HBox)
        self.VBox.addWidget(self.widget)
        self.setLayout(self.VBox)
        self.setWindowTitle("图书管理系统")
        desktop = QApplication.desktop()
        rect = desktop.availableGeometry()
        self.setWindowIcon(QIcon('img/icon-2.png'))
        self.setGeometry(rect)
        self.show()

    def generateToolBar(self):
        self.toolbar.setMinimumSize(QSize(200, 200))
        self.toolbar.setIconSize(QSize(100, 100))
        # self.toolbar.setTextSize(QSize(100, 100))
        self.toolbar.setFont(QFont("", 15))
        self.toolbar.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        addbook = QAction(QIcon('img/add-2.png'), "添加书籍", self.toolbar)
        inbook = QAction(QIcon('img/import-6.png'), "导入", self.toolbar)
        editbook = QAction(QIcon('img/edit-5.png'), "编辑元数据", self.toolbar)
        sortbooks = QAction(QIcon('img/sort-7.png'), "排序", self.toolbar)
        readbook = QAction(QIcon('img/read-2.png'), "阅读书籍", self.toolbar)
        convertbook = QAction(QIcon('img/convert-1.png'), "转换书籍", self.toolbar)
        deletebook = QAction(QIcon('img/delete-4.png'), "移除书籍", self.toolbar)
        booklist = QAction(QIcon('img/booklist-2.png'), "创建书单", self.toolbar)
        bookshelf = QAction(QIcon('img/bookshelf.png'), "打开书库", self.toolbar)
        export = QAction(QIcon('img/export-1.png'), "导出", self.toolbar)
        share = QAction(QIcon('img/share-7.png'), "分享", self.toolbar)
        star = QAction(QIcon('img/star-1.png'), "支持我们", self.toolbar)
        gethelp = QAction(QIcon("img/help-2.png"), "帮助", self.toolbar)
        setting = QAction(QIcon("img/setting-3.png"), "设置", self.toolbar)

        addbook.triggered.connect(self.addBook)
        inbook.triggered.connect(self.inBook)
        editbook.triggered.connect(self.editBook)
        sortbooks.triggered.connect(self.sortBooks)
        readbook.triggered.connect(self.readBook)
        convertbook.triggered.connect(self.convertBook)
        deletebook.triggered.connect(self.deleteBook)
        booklist.triggered.connect(self.addBookList)
        bookshelf.triggered.connect(self.openBookShelf)
        export.triggered.connect(self.export)
        share.triggered.connect(self.share)
        star.triggered.connect(self.giveusStar)
        gethelp.triggered.connect(self.getHelp)
        setting.triggered.connect(self.setSetting)

        self.toolbar.addActions([addbook, inbook])
        self.toolbar.addSeparator()
        self.toolbar.addActions([editbook, sortbooks])
        self.toolbar.addSeparator()
        self.toolbar.addActions([readbook, convertbook, deletebook])
        self.toolbar.addSeparator()
        self.toolbar.addActions([booklist, bookshelf])
        self.toolbar.addSeparator()
        self.toolbar.addActions([export, share, star, gethelp])
        self.toolbar.addSeparator()
        self.toolbar.addActions([setting])

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


