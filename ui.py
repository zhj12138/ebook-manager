# 此文件为UI程序
import time

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from mywidgets import *
from mydatabase import MyDb
from fileMethods import *
import os


class BookManager(QMainWindow):
    def __init__(self):
        super(BookManager, self).__init__()
        self.toolbar = MyToolBar()
        self.addToolBar(self.toolbar)
        self.generateToolBar()

        self.searchLine = MySearch()
        self.treeView = MyTree()
        self.treeView.setMaximumWidth(1000)
        self.treeView.setMinimumWidth(200)
        self.scrollarea = QScrollArea()
        tempwidget = QWidget()
        # tempwidget.setStyleSheet("QLabel{border:2px solid red;}")
        self.booksView = MyGrid(tempwidget, self.scrollarea)
        self.booksView.itemClicked.connect(self.updateInfo)
        tempinfo = QWidget()
        # tempinfo.setMinimumWidth(0)
        self.infoView = MyList(tempinfo)
        # self.infoView.setMaximumWidth(700)
        # self.infoView.setMinimumWidth(200)

        # self.scrollarea.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        # self.scrollarea.setSizePolicy()
        self.scrollarea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scrollarea.setMinimumWidth(1190)
        self.scrollarea.setMaximumWidth(1800)
        # self.scrollarea.resizeEvent = self.resizeUpdate
        # tempwidget.setLayout(self.booksView)
        self.scrollarea.setWidget(tempwidget)
        # self.scrollarea.setLayout(self.booksView)
        tempinfo.setLayout(self.infoView)
        splitter1 = QSplitter(Qt.Horizontal)
        splitter1.addWidget(self.scrollarea)
        splitter1.addWidget(tempinfo)
        splitter1.setSizes([1000, 400])
        splitter2 = QSplitter(Qt.Horizontal)
        splitter2.addWidget(self.treeView)
        splitter2.addWidget(splitter1)
        splitter2.setSizes([400, 1400])

        self.VBox = QVBoxLayout()
        self.VBox.addWidget(self.searchLine)
        self.VBox.addWidget(splitter2)
        self.mainwidget = QWidget()
        self.mainwidget.setLayout(self.VBox)
        self.setCentralWidget(self.mainwidget)

        self.mainExePath = os.getcwd()
        self.db = MyDb(os.path.join(self.mainExePath, 'info.db'))
        self.bookShelfPath = os.path.join(self.mainExePath, "books")
        # print(self.path)

        # 打开时读取数据
        self.curShowBooks = self.db.getAllBooks()
        # print("Hello")
        os.chdir(self.mainExePath)
        self.booksView.updateView(self.curShowBooks)
        self.updateTreeView()
        # time.sleep(1)

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
        os.chdir(self.mainExePath)
        filename, _ = QFileDialog.getOpenFileName(self, "选择文件", ".", "PDF file(*.pdf)")
        if filename:
            doc = fitz.open(filename)
            name = getTitle(doc)
            authors = getAuthors(doc)
            pub_date = getPubDate(doc)
            book_path, file_path = getFilePath(self.bookShelfPath, name, self.db.getID(), filename)
            cover_path = getCover(doc, book_path)
            self.db.createNewBook(name, authors, pub_date, file_path=file_path, cover_path=cover_path)
            # print("Hi")
            self.curShowBooks = self.db.getAllBooks()
            # print("Hello")
            os.chdir(self.mainExePath)
            self.booksView.updateView(self.curShowBooks)
            self.updateTreeView()
            time.sleep(1)
            # print("Hi")

    def updateInfo(self, ID):
        book = self.db.getBookByID(ID)
        self.infoView.updateView(book)

    def updateTreeView(self):
        authors = {author.name for author in self.db.getAllAuthors()}
        self.treeView.updateAuthors(authors)
        booklists = {booklist.name for booklist in self.db.getAllBookLists()}
        self.treeView.updateBookLists(booklists)
        tags = self.db.getAllTags()
        self.treeView.updateTags(tags)
        languages = self.db.getAllLanguages()
        print(languages)
        self.treeView.updateLanguage(languages)
        publishers = self.db.getAllPublishers()
        print(publishers)
        self.treeView.updatePublisher(publishers)

    # def resizeUpdate(self, ev):
    #     if self.scrollarea.size().width() > 1500:
    #         self.booksView.updateView(self.curShowBooks)

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


