import os
from math import floor, ceil

from PyQt5 import QtGui
from PyQt5.QtCore import QSize, Qt, pyqtSignal
from PyQt5.QtGui import QFont, QIcon, QPixmap, QMouseEvent
from PyQt5.QtWidgets import *

from basic import strListToString
from classes import Book
from typing import List

from mydatabase import MyDb


Books = List[Book]


class MyToolBar(QToolBar):
    sortModeChangedSignal = pyqtSignal()

    def __init__(self):
        super(MyToolBar, self).__init__()
        self.setMinimumSize(QSize(200, 200))
        self.setIconSize(QSize(100, 100))
        self.setFont(QFont("", 15))
        self.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.addbook = QAction(QIcon('img/add-2.png'), "添加书籍", self)
        self.inbook = QAction(QIcon('img/import-6.png'), "导入", self)
        self.editbook = QAction(QIcon('img/edit-5.png'), "编辑元数据", self)
        # self.sortbooks = QAction(QIcon('img/sortUp-2.png'), "排序", self)
        self.highSort = QAction(QIcon('img/sort-7.png'), "高级排序", self)
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

        self.sortMode = "name"
        self.sortByName = QAction("按书名排序", self)
        self.sortByAuthor = QAction("按作者排序", self)
        self.sortByPublisher = QAction("按出版社排序", self)
        self.sortByPubDate = QAction("按出版时间排序", self)
        self.sortByRating = QAction("按评分排序", self)

        self.sortByName.triggered.connect(lambda: self.changeSortMode("name"))
        self.sortByAuthor.triggered.connect(lambda: self.changeSortMode("author"))
        self.sortByPublisher.triggered.connect(lambda: self.changeSortMode("publisher"))
        self.sortByPubDate.triggered.connect(lambda: self.changeSortMode("pub_date"))
        self.sortByRating.triggered.connect(lambda: self.changeSortMode("rating"))

        self.sortMenu = QMenu()
        self.sortMenu.setFont(QFont("", 14))
        self.sortMenu.addActions([self.sortByName, self.sortByAuthor, self.sortByPublisher, self.sortByPubDate,
                                  self.sortByRating])
        self.sortBtn = QToolButton()
        self.sortBtn.setIcon(QIcon('img/sortUp-2.png'))
        # self.sortBtn.setIconSize(QSize(200, 200))
        self.sortBtn.setMenu(self.sortMenu)
        self.sortBtn.setPopupMode(QToolButton.MenuButtonPopup)

        self.addActions([self.addbook, self.inbook])
        self.addSeparator()
        self.addActions([self.editbook])
        self.addWidget(self.sortBtn)
        self.addActions([self.highSort])
        # self.addWidget(self.mBtn)
        self.addSeparator()
        self.addActions([self.readbook, self.convertbook, self.deletebook])
        self.addSeparator()
        self.addActions([self.booklist, self.bookshelf])
        self.addSeparator()
        self.addActions([self.export, self.share, self.star])
        self.addSeparator()
        self.addActions([self.setting])

    def changeSortMode(self, attr: str):
        self.sortMode = attr
        self.sortModeChangedSignal.emit()


class MyTree(QTreeWidget):
    itemClickedSignal = pyqtSignal(list)

    def __init__(self, db: MyDb):
        super(MyTree, self).__init__()
        self.db = db
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
        self.itemClicked.connect(self.onItemClicked)

    def updateAuthors(self, author_list):
        self.authors.takeChildren()
        for author in author_list:
            node = QTreeWidgetItem(self.authors)
            node.setText(0, author)
            # print(node.parent().text(0))

    def updateBookLists(self, book_lists):
        self.booklists.takeChildren()
        for booklist in book_lists:
            node = QTreeWidgetItem(self.booklists)
            node.setText(0, booklist)

    def updateTags(self, tag_list):
        self.tags.takeChildren()
        for tag in tag_list:
            node = QTreeWidgetItem(self.tags)
            node.setText(0, tag)

    def updateLanguage(self, language_list):
        self.language.takeChildren()
        for language in language_list:
            node = QTreeWidgetItem(self.language)
            node.setText(0, language)

    def updatePublisher(self, pub_list):
        self.publisher.takeChildren()
        for publisher in pub_list:
            node = QTreeWidgetItem(self.publisher)
            node.setText(0, publisher)

    # def updateRating(self):
    #     self.rating.takeChildren()
    def onItemClicked(self, item: QTreeWidgetItem, col):
        # if not item.parent():  # 是顶层结点，更新booksview变为显示所有书籍
        books = self.db.getAllBooks()
        ITEM_TEXT = item.text(0)
        if item.parent():
            if item.parent().text(0) == "作者":
                books = [book for book in books if ITEM_TEXT in book.authors]
            elif item.parent().text(0) == "书单":
                books = [book for book in books if ITEM_TEXT in book.bookLists]
            elif item.parent().text(0) == "标签":
                books = [book for book in books if ITEM_TEXT in book.tags]
            elif item.parent().text(0) == "语言":
                books = [book for book in books if book.language == ITEM_TEXT]
            elif item.parent().text(0) == "出版社":
                books = [book for book in books if book.publisher == ITEM_TEXT]
            else:  # 评分
                if ITEM_TEXT == "5星":
                    books = [book for book in books if book.rating == 5]
                elif ITEM_TEXT == '4星':
                    books = [book for book in books if book.rating == 4]
                elif ITEM_TEXT == '3星':
                    books = [book for book in books if book.rating == 3]
                elif ITEM_TEXT == '2星':
                    books = [book for book in books if book.rating == 2]
                elif ITEM_TEXT == '1星':
                    books = [book for book in books if book.rating == 1]
                else:  # 尚未评分
                    books = [book for book in books if book.rating == 0]
        self.itemClickedSignal.emit(books)


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
        # print(parent.size().width(), parent.size().height())
        # self.father.resizeEvent = self.onResize
        # print(wid.size().width(), wid.size().height())
        self.setSpacing(30)
        self.lastActive = None
        self.dict = {}
        self.itemWidth = 365
        self.itemHeight = 458

    def updateView(self, books: Books):
        # children = self.findChildren(MyLabel)
        # for child in children:
        #     self.removeWidget(child)
        self.deleteAll()
        self.lastActive = None
        if not books:
            return
        total = len(books)
        # print(total)
        cols = 3
        # if self.scrollarea.size().width() > 1500:
        #     cols = 4
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
            if book.name:
                tempLabel.setToolTip(book.name)
            tempLabel.clicked.connect(self.onItemClicked)
            self.dict[tempLabel] = book.ID
            self.addWidget(tempLabel, *point)
        tempWid.setLayout(self)
        self.scrollarea.setWidget(tempWid)
        self.father = tempWid

    def deleteAll(self):
        while self.count():
            item = self.takeAt(0)
            widget = item.widget()
            widget.deleteLater()

    def onItemClicked(self):
        sender = self.sender()
        if self.lastActive:
            self.lastActive.setStyleSheet("")
        sender.setStyleSheet("border:4px solid blue;")
        self.lastActive = sender
        self.itemClicked.emit(self.dict[sender])  # 传回一个ID
        # print(sender.pixmap().size().width(), sender.pixmap().size().height())
        # print(sender.pixmap().)


class MyList(QVBoxLayout):
    def __init__(self, father):
        super(MyList, self).__init__(father)
        self.father = father
        self.picLabel = QLabel()
        self.picLabel.setPixmap(QPixmap('img/default-pic.png').scaled(365, 458))
        self.namelabel = QLabel("书名")
        self.authorlabel = QLabel("作者")
        self.pathlabel = QLabel("路径")
        self.formatlabel = QLabel("格式")
        self.tagslabel = QLabel("标签")
        self.booklistslabel = QLabel("书单")
        self.name = QLabel("未知")
        self.authors = QLabel("未知")
        self.path = MyLabel("无")
        self.format = MyLabel("无")
        self.tags = QLabel("无")
        self.booklists = QLabel("无")
        self.bookPath = None

        self.form = QFormLayout()
        self.form.insertRow(0, self.namelabel, self.name)
        self.form.insertRow(1, self.authorlabel, self.authors)
        self.form.insertRow(2, self.pathlabel, self.path)
        self.form.insertRow(3, self.formatlabel, self.format)
        self.form.insertRow(4, self.tagslabel, self.tags)
        self.form.insertRow(5, self.booklistslabel, self.booklists)

        # self.detaillabel = QLabel("书籍的详细信息")
        # vlay = QVBoxLayout()
        self.addWidget(self.picLabel)
        temwidget = QWidget()
        temwidget.setFont(QFont("", 14))
        temwidget.setLayout(self.form)
        self.scrollarea = QScrollArea()
        self.scrollarea.setFrameShape(QFrame.NoFrame)
        # self.scrollarea.setStyleSheet("border:none;QLabel{font-size:14px;}")
        self.scrollarea.setWidget(temwidget)
        # temwidget.setMaximumSize(200, 300)
        self.addWidget(self.scrollarea)
        # vlay.addWidget(self.detaillabel)
        # self.setLayout(vlay)

    def setDefault(self):
        self.picLabel.setPixmap(QPixmap('img/default-pic.png').scaled(365, 458))
        self.name = QLabel("未知")
        self.authors = QLabel("未知")
        self.path = MyLabel("无")
        self.format = MyLabel("无")
        self.tags = QLabel("无")
        self.booklists = QLabel("无")
        self.bookPath = None

    def updateView(self, book: Book):
        if book.cover_path:
            self.picLabel.setPixmap(QPixmap(book.cover_path).scaled(365, 458))
        else:
            self.picLabel.setPixmap(QPixmap('img/default-pic.png').scaled(365, 458))
        if book.name:
            self.name.setText(book.name)
        else:
            self.name.setText("未知")
        if book.authors:
            self.authors.setText(strListToString(book.authors))
        else:
            self.authors.setText("未知")
        if book.file_path:
            self.bookPath = book.file_path
            self.path.setText("<a style='color: blue'>打开</a>")
            self.format.setText("<a style='color: blue'>PDF</a>")
            self.format.clicked.connect(self.openFile)
            self.path.clicked.connect(self.openPath)
        else:
            self.bookPath = None
            self.path.setText("无")
            self.format.setText("无")
        if book.tags:
            self.tags.setText(strListToString(book.tags))
        else:
            self.tags.setText("无")
        if book.bookLists:
            self.booklists.setText(strListToString(book.bookLists))
        else:
            self.booklists.setText("无")
        temp = QWidget()
        temp.setFont(QFont("", 14))
        temp.setLayout(self.form)
        temp.setMinimumWidth(0)
        self.scrollarea.setWidget(temp)

    def openFile(self):
        os.startfile(self.bookPath)

    def openPath(self):
        mypath, fileName = os.path.split(self.bookPath)
        os.startfile(mypath)


class MySearch(QToolBar):
    def __init__(self):
        super(MySearch, self).__init__()
        self.setFont(QFont("", 15))
        self.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.searchModeLabel = QLabel("搜索模式")
        self.searchBy = QComboBox()
        # self.searchBy.setStyleSheet("background-color:white")
        self.searchBy.addItems(['按书名', '按作者', '按书单', '按标签', '按出版社', '按ISBN'])
        self.searchMode = QComboBox()
        self.searchMode.addItems(['准确匹配', '模糊匹配', '正则匹配'])
        self.inputLine = QLineEdit()
        self.inputLine.setPlaceholderText("选择搜索模式后，在此输入关键词")
        self.searchAct = QAction(QIcon("img/search-4.png"), "搜索", self)
        self.highSearchAct = QAction(QIcon('img/hsearch-1.png'), "高级搜索", self)
        self.historySearchAct = QAction(QIcon('img/history-1.png'), "历史搜索", self)

        self.searchAct.triggered.connect(self.onSearch)
        self.highSearchAct.triggered.connect(self.onHighSearch)
        self.historySearchAct.triggered.connect(self.onHistory)

        self.addWidget(self.searchModeLabel)
        self.addWidget(self.searchBy)
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
