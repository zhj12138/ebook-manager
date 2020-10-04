import os
from math import floor, ceil

from PyQt5 import QtGui
from PyQt5.QtCore import QSize, Qt, pyqtSignal
from PyQt5.QtGui import QFont, QIcon, QPixmap, QMouseEvent
from PyQt5.QtWidgets import QTreeWidget, QTableWidget, QListWidget, QToolBar, QTreeWidgetItem, QAction, QGridLayout, \
    QLabel, QPushButton, QTableWidgetItem, QWidget, QFormLayout, QFrame, QVBoxLayout, QComboBox, QLineEdit

from basic import strListToString
from classes import Book
from typing import List

Books = List[Book]


class MyToolBar(QToolBar):
    def __init__(self):
        super(MyToolBar, self).__init__()
        self.setMinimumSize(QSize(200, 200))
        self.setIconSize(QSize(100, 100))
        self.setFont(QFont("", 15))
        self.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.addbook = QAction(QIcon('img/add-2.png'), "添加书籍", self)
        self.inbook = QAction(QIcon('img/import-6.png'), "导入", self)
        self.editbook = QAction(QIcon('img/edit-5.png'), "编辑元数据", self)
        self.sortbooks = QAction(QIcon('img/sort-7.png'), "排序", self)
        self.readbook = QAction(QIcon('img/read-2.png'), "阅读书籍", self)
        self.convertbook = QAction(QIcon('img/convert-1.png'), "转换书籍", self)
        self.deletebook = QAction(QIcon('img/delete-4.png'), "移除书籍", self)
        self.booklist = QAction(QIcon('img/booklist-2.png'), "创建书单", self)
        self.bookshelf = QAction(QIcon('img/bookshelf.png'), "打开书库", self)
        self.export = QAction(QIcon('img/export-1.png'), "导出", self)
        self.share = QAction(QIcon('img/share-7.png'), "分享", self)
        self.star = QAction(QIcon('img/star-1.png'), "支持我们", self)
        self.gethelp = QAction(QIcon("img/help-2.png"), "帮助", self)
        self.setting = QAction(QIcon("img/setting-3.png"), "设置", self)

        self.addActions([self.addbook, self.inbook])
        self.addSeparator()
        self.addActions([self.editbook, self.sortbooks])
        self.addSeparator()
        self.addActions([self.readbook, self.convertbook, self.deletebook])
        self.addSeparator()
        self.addActions([self.booklist, self.bookshelf])
        self.addSeparator()
        self.addActions([self.export, self.share, self.star, self.gethelp])
        self.addSeparator()
        self.addActions([self.setting])


class MyTree(QTreeWidget):
    def __init__(self):
        super(MyTree, self).__init__()
        self.setColumnCount(1)
        self.setHeaderHidden(True)
        self.setFont(QFont("", 15))
        self.setIconSize(QSize(50, 50))
        self.authors = QTreeWidgetItem(self)
        self.authors.setText(0, "作者")
        self.authors.setIcon(0, QIcon('img/author-1.png'))
        self.booklists = QTreeWidgetItem(self)
        self.booklists.setText(0, "书单")
        self.booklists.setIcon(0, QIcon('img/list-1.png'))
        self.tags = QTreeWidgetItem(self)
        self.tags.setText(0, "标签")
        self.tags.setIcon(0, QIcon('img/tag-1.png'))
        self.language = QTreeWidgetItem(self)
        self.language.setText(0, "语言")
        self.language.setIcon(0, QIcon('img/language-3.png'))
        self.publisher = QTreeWidgetItem(self)
        self.publisher.setText(0, "出版社")
        self.publisher.setIcon(0, QIcon("img/publish-1.png"))
        self.rating = QTreeWidgetItem(self)
        self.rating.setText(0, "评分")
        self.rating.setIcon(0, QIcon('img/rate-3.png'))
        self.fiveScore = QTreeWidgetItem(self.rating)
        self.fiveScore.setText(0, "5星")
        self.fourScore = QTreeWidgetItem(self.rating)
        self.fourScore.setText(0, "4星")
        self.threeScore = QTreeWidgetItem(self.rating)
        self.threeScore.setText(0, "3星")
        self.twoScore = QTreeWidgetItem(self.rating)
        self.twoScore.setText(0, "2星")
        self.oneScore = QTreeWidgetItem(self.rating)
        self.oneScore.setText(0, "1星")
        self.noScore = QTreeWidgetItem(self.rating)
        self.noScore.setText(0, "尚未评分")

    def updateAuthors(self, author_list):
        for author in author_list:
            node = QTreeWidgetItem(self.authors)
            node.setText(0, author)

    def updateBookLists(self, book_lists):
        for booklist in book_lists:
            node = QTreeWidgetItem(self.booklists)
            node.setText(booklist)

    def updateTags(self, tag_list):
        for tag in tag_list:
            node = QTreeWidgetItem(self.tags)
            node.setText(tag)

    def updateLanguage(self, language_list):
        for language in language_list:
            node = QTreeWidgetItem(self.language)
            node.setText(language)

    def updatePublisher(self, pub_list):
        for publisher in pub_list:
            node = QTreeWidgetItem(self.publisher)
            node.setText(publisher)


class MyLabel(QLabel):
    clicked = pyqtSignal()

    def mousePressEvent(self, ev: QtGui.QMouseEvent) -> None:
        self.clicked.emit()
        super(MyLabel, self).mousePressEvent(ev)


class MyGrid(QGridLayout):
    itemClicked = pyqtSignal(int)

    def __init__(self, parent, scro):
        super(MyGrid, self).__init__(parent)
        self.father = parent
        self.scrollarea = scro
        print(parent.size().width(), parent.size().height())
        # self.father.resizeEvent = self.onResize
        # print(wid.size().width(), wid.size().height())
        self.setSpacing(30)
        self.lastActive = None
        self.dict = {}
        self.itemWidth = 365
        self.itemHeight = 458
        # book1 = MyLabel()
        # book1.setPixmap(QPixmap('testBookImage/1.png').scaled(self.itemWidth, self.itemHeight))
        # book1.clicked.connect(self.onItemClicked)
        # book2 = MyLabel()
        # book2.setPixmap(QPixmap('testBookImage/2.png').scaled(self.itemWidth, self.itemHeight))
        # book2.clicked.connect(self.onItemClicked)
        # # self.dict[book2] = "What"
        # book3 = MyLabel()
        # book3.setPixmap(QPixmap('testBookImage/3.png').scaled(self.itemWidth, self.itemHeight))
        # book3.clicked.connect(self.onItemClicked)
        # book4 = MyLabel()
        # book4.setPixmap(QPixmap('testBookImage/1.png').scaled(self.itemWidth, self.itemHeight))
        # book4.clicked.connect(self.onItemClicked)
        # book5 = MyLabel()
        # book5.setPixmap(QPixmap('testBookImage/2.png').scaled(self.itemWidth, self.itemHeight))
        # book5.clicked.connect(self.onItemClicked)
        # # self.dict[book2] = "What"
        # book6 = MyLabel()
        # book6.setPixmap(QPixmap('testBookImage/3.png').scaled(self.itemWidth, self.itemHeight))
        # book6.clicked.connect(self.onItemClicked)
        # book7 = MyLabel()
        # book7.setPixmap(QPixmap('testBookImage/1.png').scaled(self.itemWidth, self.itemHeight))
        # book7.clicked.connect(self.onItemClicked)
        # book8 = MyLabel()
        # book8.setPixmap(QPixmap('testBookImage/2.png').scaled(self.itemWidth, self.itemHeight))
        # book8.clicked.connect(self.onItemClicked)
        # # self.dict[book2] = "What"
        # book9 = MyLabel()
        # book9.setPixmap(QPixmap('testBookImage/3.png').scaled(self.itemWidth, self.itemHeight))
        # book9.clicked.connect(self.onItemClicked)
        # self.addWidget(book1, 0, 0)
        # self.addWidget(book2, 0, 1)
        # self.addWidget(book3, 0, 2)
        # self.addWidget(book4, 1, 0)
        # self.addWidget(book5, 1, 1)
        # self.addWidget(book6, 1, 2)
        # self.addWidget(book7, 2, 0)
        # self.addWidget(book8, 2, 1)
        # self.addWidget(book9, 2, 2)

    def updateView(self, books: Books):
        # print("A", self.itemWidth, self.itemHeight)
        # book11 = MyLabel()
        # # book11.setPixmap(QPixmap('testBookImage/11.png').scaled(wid, hei))
        # a = QPixmap('testBookImage/12.png').scaled(self.itemWidth, self.itemHeight)
        # print(a.size().width())
        # print(a.size().height())
        # book11.setPixmap(a)
        # book11.clicked.connect(self.handleMouse)
        total = len(books)
        # print(total)
        cols = 3
        rows = ceil(total / cols)
        # print(cols)
        # print(rows)
        points = [(i, j) for i in range(rows) for j in range(cols)]
        # print(points)
        tempWid = QWidget()
        for point, book in zip(points, books):
            tempLabel = MyLabel()
            tempLabel.setPixmap(QPixmap(book.cover_path).scaled(self.itemWidth, self.itemHeight))
            tempLabel.setScaledContents(True)
            tempLabel.clicked.connect(self.onItemClicked)
            self.dict[tempLabel] = book.ID
            self.addWidget(tempLabel, *point)
        tempWid.setLayout(self)
        self.scrollarea.setWidget(tempWid)
        self.father = tempWid

    def onItemClicked(self):
        sender = self.sender()
        if self.lastActive:
            self.lastActive.setStyleSheet("")
        sender.setStyleSheet("border:4px solid blue;")
        self.lastActive = sender
        # self.itemClicked.emit(self.dict[sender])  # 传回一个ID
        print(sender.pixmap().size().width(), sender.pixmap().size().height())
        # print(sender.pixmap().)


class MyList(QWidget):
    def __init__(self):
        super(MyList, self).__init__()
        self.setFont(QFont("", 15))

        self.picLabel = QLabel()
        self.picLabel.setPixmap(QPixmap('img/default-pic.png').scaled(286, 320))
        self.namelabel = QLabel("书名")
        self.authorlabel = QLabel("作者")
        self.pathlabel = QLabel("路径")
        self.formatlabel = QLabel("格式")
        self.tagslabel = QLabel("标签")
        self.booklistslabel = QLabel("书单")
        self.name = QLabel("无")
        self.authors = QLabel("无")
        self.path = QLabel("无")
        self.format = QLabel("无")
        self.tags = QLabel("无")
        self.booklists = QLabel("无")

        self.form = QFormLayout()
        self.form.insertRow(0, self.namelabel, self.name)
        self.form.insertRow(1, self.authorlabel, self.authors)
        self.form.insertRow(2, self.pathlabel, self.path)
        self.form.insertRow(3, self.formatlabel, self.format)
        self.form.insertRow(4, self.tagslabel, self.tags)
        self.form.insertRow(5, self.booklistslabel, self.booklists)

        # self.detaillabel = QLabel("书籍的详细信息")
        vlay = QVBoxLayout()
        vlay.addWidget(self.picLabel)
        temwidget = QWidget()
        temwidget.setLayout(self.form)
        temwidget.setMaximumSize(200, 300)
        vlay.addWidget(temwidget)
        # vlay.addWidget(self.detaillabel)
        self.setLayout(vlay)

    def updateView(self, book: Book):
        self.picLabel.setPixmap(QPixmap(book.cover_path))
        if book.name:
            self.name.setText(book.name)
        if book.authors:
            self.authors.setText(strListToString(book.authors))
        if book.file_path:
            self.path.setText("<a style='color: blue'>{}</a>".format(book.file_path))
            self.format.setText("<a style='color: blue'>PDF</a>")
            self.format.mousePressEvent = self.openFile
            self.path.mousePressEvent = self.openPath
        if book.tags:
            self.path.setText(strListToString(book.tags))
        if book.bookLists:
            self.booklists.setText(strListToString(book.bookLists))

    def openFile(self, ev):
        os.startfile(self.path.text())

    def openPath(self, ev):
        os.startfile(self.path.text()[:-1])


class MySearch(QToolBar):
    def __init__(self):
        super(MySearch, self).__init__()
        self.setFont(QFont("", 15))
        self.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.searchModeLabel = QLabel("搜索模式")
        self.searchMode = QComboBox()
        self.searchMode.addItems(['普通模式', '正则表达式'])
        self.inputLine = QLineEdit()
        self.inputLine.setPlaceholderText("请输入您想要查找的书名")
        self.searchAct = QAction(QIcon("img/search-4.png"), "搜索", self)
        self.highSearchAct = QAction(QIcon('img/hsearch-1.png'), "高级搜索", self)
        self.historySearchAct = QAction(QIcon('img/history-1.png'), "历史搜索", self)

        self.searchAct.triggered.connect(self.onSearch)
        self.highSearchAct.triggered.connect(self.onHighSearch)
        self.historySearchAct.triggered.connect(self.onHistory)

        self.addWidget(self.searchModeLabel)
        self.addWidget(self.searchMode)
        self.addSeparator()
        self.addWidget(self.inputLine)
        self.addAction(self.searchAct)
        self.addSeparator()
        self.addActions([self.highSearchAct, self.historySearchAct])

    def onSearch(self):
        pass

    def onHighSearch(self):
        pass

    def onHistory(self):
        pass
