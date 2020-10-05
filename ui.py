# 此文件为UI程序
import time

from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from mywidgets import *
from mydatabase import MyDb
from fileMethods import *
import os
from mydialogs import *


class BookManager(QMainWindow):
    def __init__(self):
        super(BookManager, self).__init__()
        self.toolbar = MyToolBar()
        self.addToolBar(self.toolbar)
        self.generateToolBar()

        self.mainExePath = os.getcwd()
        self.db = MyDb(os.path.join(self.mainExePath, 'info.db'))
        self.bookShelfPath = os.path.join(self.mainExePath, "books")

        self.searchLine = MySearch()
        self.treeView = MyTree(self.db)
        self.treeView.itemClickedSignal.connect(self.onTreeItemClicked)
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

        self.importfiledialog = None

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

        # 打开时读取数据
        self.curShowBooks = self.db.getAllBooks()
        # print("Hello")
        os.chdir(self.mainExePath)
        self.booksView.updateView(self.curShowBooks)
        self.updateTreeView()
        # time.sleep(1)
        QToolTip.setFont(QFont("", 14))
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
        self.toolbar.sortBtn.clicked.connect(self.sortBooks)
        self.toolbar.highSort.triggered.connect(self.HighSort)
        self.toolbar.readbook.triggered.connect(self.readBook)
        self.toolbar.convertbook.triggered.connect(self.convertBook)
        self.toolbar.deletebook.triggered.connect(self.deleteBook)
        self.toolbar.booklist.triggered.connect(self.addBookList)
        self.toolbar.bookshelf.triggered.connect(self.openBookShelf)
        self.toolbar.export.triggered.connect(self.export)
        self.toolbar.share.triggered.connect(self.share)
        self.toolbar.star.triggered.connect(self.giveusStar)
        # self.toolbar.gethelp.triggered.connect(self.getHelp)
        self.toolbar.setting.triggered.connect(self.setSetting)
        self.toolbar.sortModeChangedSignal.connect(self.sortBooks)

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
            # time.sleep(1)
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
        # print(languages)
        # print("Lan", languages)
        self.treeView.updateLanguage(languages)
        publishers = self.db.getAllPublishers()
        # print("Pub", publishers)
        # print(publishers)
        self.treeView.updatePublisher(publishers)

    def onTreeItemClicked(self, books):
        self.curShowBooks = books
        self.booksView.updateView(books)
    # def resizeUpdate(self, ev):
    #     if self.scrollarea.size().width() > 1500:
    #         self.booksView.updateView(self.curShowBooks)

    def inBook(self):
        self.importfiledialog = ImportFileDialog(self.bookShelfPath, self.db, self)
        self.importfiledialog.finishSignal.connect(self.onInBook)
        self.importfiledialog.show()

    def onInBook(self, pdfFilePath, name, authors, language, rating):
        doc = fitz.open(pdfFilePath)
        book_path, _ = os.path.split(pdfFilePath)
        cover_path = getCover(doc, book_path)
        self.db.createNewBook(name=name, authors=authors, language=language, rating=rating, file_path=pdfFilePath,
                              cover_path=cover_path)
        self.curShowBooks = self.db.getAllBooks()
        # print("Hello")
        os.chdir(self.mainExePath)
        self.booksView.updateView(self.curShowBooks)
        self.updateTreeView()
        self.importfiledialog.close()

    def editBook(self):
        if not self.booksView.lastActive:
            return
        book = self.db.getBookByID(self.booksView.dict[self.booksView.lastActive])
        if book:
            dig = EditDataDialog(self.db, book, self)
            dig.changeSignal.connect(self.onDataChanged)
            dig.show()

    def onDataChanged(self, ID):
        self.updateTreeView()
        self.updateInfo(ID)

    def sortBooks(self):
        if self.toolbar.sortMode == 'name':
            books = sorted(self.curShowBooks, key=lambda book: book.name)
            if books == self.curShowBooks:
                self.toolbar.sortBtn.setIcon(QIcon(os.path.join(self.mainExePath, 'img/sortUp-2.png')))
                self.curShowBooks = sorted(self.curShowBooks, key=lambda book: book.name, reverse=True)
            else:
                self.toolbar.sortBtn.setIcon(QIcon(os.path.join(self.mainExePath, 'img/sortDown.png')))
                self.curShowBooks = books
        elif self.toolbar.sortMode == 'author':
            books = sorted(self.curShowBooks, key=lambda book: strListToString(book.authors))
            if books == self.curShowBooks:
                self.toolbar.sortBtn.setIcon(QIcon(os.path.join(self.mainExePath, 'img/sortUp-2.png')))
                self.curShowBooks = sorted(self.curShowBooks, key=lambda book: strListToString(book.authors),
                                           reverse=True)
            else:
                self.toolbar.sortBtn.setIcon(QIcon(os.path.join(self.mainExePath, 'img/sortDown.png')))
                self.curShowBooks = books
        elif self.toolbar.sortMode == 'publisher':
            books = sorted(self.curShowBooks, key=lambda book: book.publisher)
            if books == self.curShowBooks:
                self.toolbar.sortBtn.setIcon(QIcon(os.path.join(self.mainExePath, 'img/sortUp-2.png')))
                self.curShowBooks = sorted(self.curShowBooks, key=lambda book: book.publisher, reverse=True)
            else:
                self.toolbar.sortBtn.setIcon(QIcon(os.path.join(self.mainExePath, 'img/sortDown.png')))
                self.curShowBooks = books
        elif self.toolbar.sortMode == 'pub_date':
            books = sorted(self.curShowBooks, key=lambda book: book.pub_date)
            if books == self.curShowBooks:
                self.toolbar.sortBtn.setIcon(QIcon(os.path.join(self.mainExePath, 'img/sortUp-2.png')))
                self.curShowBooks = sorted(self.curShowBooks, key=lambda book: book.pub_date, reverse=True)
            else:
                self.toolbar.sortBtn.setIcon(QIcon(os.path.join(self.mainExePath, 'img/sortDown.png')))
                self.curShowBooks = books
        else:  # sort by rating
            books = sorted(self.curShowBooks, key=lambda book: book.rating)
            if books == self.curShowBooks:
                self.toolbar.sortBtn.setIcon(QIcon(os.path.join(self.mainExePath, 'img/sortUp-2.png')))
                self.curShowBooks = sorted(self.curShowBooks, key=lambda book: book.rating, reverse=True)
            else:
                self.toolbar.sortBtn.setIcon(QIcon(os.path.join(self.mainExePath, 'img/sortDown.png')))
                self.curShowBooks = books
        self.booksView.updateView(self.curShowBooks)

    def HighSort(self):
        pass

    def readBook(self):
        if self.booksView.lastActive:
            book = self.db.getBookByID(self.booksView.dict[self.booksView.lastActive])
            os.startfile(book.file_path)

    def convertBook(self):
        pass

    def deleteBook(self):
        if self.booksView.lastActive:
            book = self.db.getBookByID(self.booksView.dict[self.booksView.lastActive])
            book.delete(self.db)
            self.updateTreeView()
            self.curShowBooks = self.db.getAllBooks()
            self.booksView.updateView(self.curShowBooks)
            self.infoView.setDefault()
            # self.booksView.lastActive = None

    def addBookList(self):
        pass

    def openBookShelf(self):
        os.startfile(self.bookShelfPath)

    def export(self):
        pass

    def share(self):
        pass

    def giveusStar(self):
        QDesktopServices.openUrl(QUrl('https://github.com/zhj12138/ebook-manager'))

    # def getHelp(self):
    #     pass

    def setSetting(self):
        pass


