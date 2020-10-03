from PyQt5 import QtGui
from PyQt5.QtCore import QSize, Qt, pyqtSignal
from PyQt5.QtGui import QFont, QIcon, QPixmap, QMouseEvent
from PyQt5.QtWidgets import QTreeWidget, QTableWidget, QListWidget, QToolBar, QTreeWidgetItem, QAction, QGridLayout, \
    QLabel, QPushButton, QTableWidgetItem, QWidget, QFormLayout, QFrame, QVBoxLayout, QComboBox, QLineEdit


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

    # def updateRating(self, rating_list):
    #     pass


class MyLabel(QLabel):
    clicked = pyqtSignal()

    def mousePressEvent(self, ev: QtGui.QMouseEvent) -> None:
        self.clicked.emit()
        super(MyLabel, self).mousePressEvent(ev)


class MyGrid(QGridLayout):
    def __init__(self):
        super(MyGrid, self).__init__()
        self.setSpacing(30)
        self.lastActive = None
        a = QPixmap('testBookImage/1.png')
        b = 1.5
        wid = a.width() / b
        hei = a.height() / b
        book1 = MyLabel()
        book1.setPixmap(QPixmap('testBookImage/1.png').scaled(wid, hei))
        book1.clicked.connect(self.handleMouse)
        self.dict = {book1: "hello"}
        book2 = MyLabel()
        book2.setPixmap(QPixmap('testBookImage/2.png').scaled(wid, hei))
        book2.clicked.connect(self.handleMouse)
        # self.dict[book2] = "What"
        book3 = MyLabel()
        book3.setPixmap(QPixmap('testBookImage/3.png').scaled(wid, hei))
        book3.clicked.connect(self.handleMouse)
        # self.dict[book3] = "Hi"
        book4 = MyLabel()
        book4.setPixmap(QPixmap('testBookImage/4.png').scaled(wid, hei))
        book4.clicked.connect(self.handleMouse)
        book5 = MyLabel()
        book5.setPixmap(QPixmap('testBookImage/5.png').scaled(wid, hei))
        book5.clicked.connect(self.handleMouse)
        book6 = MyLabel()
        book6.setPixmap(QPixmap('testBookImage/6.png').scaled(wid, hei))
        book6.clicked.connect(self.handleMouse)
        book7 = MyLabel()
        book7.setPixmap(QPixmap('testBookImage/7.png').scaled(wid, hei))
        book7.clicked.connect(self.handleMouse)
        book8 = MyLabel()
        book8.setPixmap(QPixmap('testBookImage/8.png').scaled(wid, hei))
        book8.clicked.connect(self.handleMouse)
        book9 = MyLabel()
        book9.setPixmap(QPixmap('testBookImage/9.png').scaled(wid, hei))
        book9.clicked.connect(self.handleMouse)
        book10 = MyLabel()
        book10.setPixmap(QPixmap('testBookImage/10.png').scaled(wid, hei))
        book10.clicked.connect(self.handleMouse)

        self.addWidget(book1, 0, 0)
        self.addWidget(book2, 0, 1)
        self.addWidget(book3, 0, 2)
        self.addWidget(book4, 1, 0)
        self.addWidget(book5, 1, 1)
        self.addWidget(book6, 1, 2)
        self.addWidget(book7, 2, 0)
        self.addWidget(book8, 2, 1)
        self.addWidget(book9, 2, 2)
        self.addWidget(book10, 3, 0)

    def handleMouse(self):
        sender = self.sender()
        if self.lastActive:
            self.lastActive.setStyleSheet("")
        sender.setStyleSheet("border:4px solid #87CEEB;")
        self.lastActive = sender
        # print(self.dict[sender])


class MyList(QWidget):
    def __init__(self):
        super(MyList, self).__init__()
        self.picLabel = QLabel()
        a = QPixmap('testBookImage/1.png')
        b = 1.5
        wid = a.width() / b
        hei = a.height() / b
        self.picLabel.setPixmap(QPixmap('testBookImage/1.png').scaled(wid, hei))
        self.form = QFormLayout()
        label1 = QLabel("书名")
        label2 = QLabel("作者")
        label3 = QLabel("路径")
        label4 = QLabel("格式")
        label5 = QLabel("标签")
        label6 = QLabel("书单")
        label11 = QLabel("算法")
        label21 = QLabel("李白")
        label31 = QLabel("AAA")
        self.form.insertRow(0, label1, label11)
        self.form.insertRow(1, label2, label21)
        self.detail = QLabel("书籍的详细信息")
        vlay = QVBoxLayout()
        vlay.addWidget(self.picLabel)
        temwidget = QWidget()
        temwidget.setLayout(self.form)
        temwidget.setMaximumSize(200, 300)
        vlay.addWidget(temwidget)
        vlay.addWidget(self.detail)
        self.setLayout(vlay)


class MySearch(QToolBar):
    def __init__(self):
        super(MySearch, self).__init__()
        self.setFont(QFont("", 15))
        self.searchModeLabel = QLabel("搜索模式")
        self.searchMode = QComboBox()
        self.searchMode.addItems(['普通模式', '正则表达式'])
        self.inputLine = QLineEdit()
        self.inputLine.setPlaceholderText("请输入您想要查找的书名")
        self.searchBtn = QPushButton(QIcon("img/search-4.png"), "搜索")
        self.highSearchBtn = QPushButton(QIcon('img/hsearch-1.png'), "高级搜索")
        self.historySearchBtn = QPushButton(QIcon('img/history-1.png'), "历史搜索")
        self.addWidget(self.searchModeLabel)
        self.addWidget(self.searchMode)
        self.addSeparator()
        self.addWidget(self.inputLine)
        self.addWidget(self.searchBtn)
        self.addSeparator()
        self.addWidget(self.highSearchBtn)
        self.addWidget(self.historySearchBtn)


