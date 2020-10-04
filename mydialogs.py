from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QDate, pyqtSignal

from basic import strListToString, parseStrListString
from classes import Book
from mydatabase import MyDb


class EditDataDialog(QDialog):
    changeSignal = pyqtSignal(int)

    def __init__(self, db: MyDb, book: Book, parent=None):
        super(EditDataDialog, self).__init__(parent)
        self.db = db
        self.book = book
        self.form = QFormLayout()
        self.nameLabel = QLabel("书名")
        self.nameInput = QLineEdit()
        if book.name:
            self.nameInput.setText(book.name)
        self.authorLabel = QLabel("作者")
        self.authorInput = QLineEdit()
        if book.authors:
            self.authorInput.setText(strListToString(book.authors))
        self.pub_dateLabel = QLabel("出版日期")
        self.pub_dateInput = QDateEdit()
        if book.pub_date:
            date = QDate()
            self.pub_dateInput.setDate(date.fromString(book.pub_date, 'yyyyMMdd'))
        self.publisherLabel = QLabel("出版商")
        self.publisherInput = QLineEdit()
        if book.publisher:
            self.publisherInput.setText(book.publisher)
        self.isbnLabel = QLabel("ISBN")
        self.isbnInput = QLineEdit()
        if book.isbn:
            self.isbnInput.setText(book.isbn)
        self.languageLabel = QLabel("语言")
        self.languageInput = QLineEdit()
        if book.language:
            self.languageInput.setText(book.language)
        self.ratingLabel = QLabel("评分")
        self.ratingInput = QLineEdit()
        self.ratingInput.setValidator(QIntValidator(0, 5))
        if book.rating:
            self.ratingInput.setText(str(book.rating))
        self.tagsLabel = QLabel("标签")
        self.tagsInput = QLineEdit()
        if book.tags:
            self.tagsInput.setText(strListToString(book.tags))
        self.booklistLabel = QLabel("书单")
        self.booklistInput = QLineEdit()
        if book.bookLists:
            self.booklistInput.setText(strListToString(book.bookLists))
        self.okButton = QPushButton("保存并退出")
        self.cancleButton = QPushButton("不保存退出")
        self.form.addRow(self.nameLabel, self.nameInput)
        self.form.addRow(self.authorLabel, self.authorInput)
        self.form.addRow(self.pub_dateLabel, self.pub_dateInput)
        self.form.addRow(self.publisherLabel, self.publisherInput)
        self.form.addRow(self.isbnLabel, self.isbnInput)
        self.form.addRow(self.languageLabel, self.languageInput)
        self.form.addRow(self.ratingLabel, self.ratingInput)
        self.form.addRow(self.tagsLabel, self.tagsInput)
        self.form.addRow(self.booklistLabel, self.booklistInput)
        self.form.addRow(self.okButton, self.cancleButton)
        self.setLayout(self.form)
        self.okButton.clicked.connect(self.onOK)
        self.cancleButton.clicked.connect(self.onCancle)

    def onOK(self):
        self.book.name = self.nameInput.text()
        self.book.setAuthors(self.db, parseStrListString(self.authorInput.text()))
        self.book.pub_date = self.pub_dateInput.date().toString('yyyyMMdd')
        self.book.publisher = self.publisherInput.text()
        self.book.isbn = self.isbnInput.text()
        self.book.language = self.languageInput.text()
        if self.ratingInput.text():
            self.book.rating = int(self.ratingInput.text())
        else:
            self.book.rating = 0
        self.book.tags = parseStrListString(self.tagsInput.text())
        self.book.setBookLists(self.db, parseStrListString(self.booklistInput.text()))
        self.book.updateDB(self.db)
        self.changeSignal.emit(self.book.ID)
        self.close()

    def onCancle(self):
        self.close()


