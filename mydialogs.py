import time
from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QDate, pyqtSignal
from basic import strListToString
from classes import Book
from mydatabase import MyDb
from mythreads import convertThread
from fileMethods import *


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
        self.publisherLabel = QLabel("出版社")
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


class ImportFileEditDialog(QDialog):
    changeSignal = pyqtSignal(str, list, str, int)

    def __init__(self, name=None, parent=None):
        super(ImportFileEditDialog, self).__init__(parent)
        self.nameLabel = QLabel("书名")
        self.nameInput = QLineEdit()
        if name:
            self.nameInput.setText(name)
        self.authorLabel = QLabel("作者")
        self.authorInput = QLineEdit()
        self.languageLabel = QLabel("语言")
        self.languageInput = QLineEdit()
        self.ratingLabel = QLabel("评分")
        self.ratingInput = QLineEdit()
        self.ratingInput.setValidator(QIntValidator(0, 5))
        self.okBtn = QPushButton("确定")
        self.okBtn.clicked.connect(self.onClicked)
        self.cancleBtn = QPushButton("取消转换")
        self.cancleBtn.clicked.connect(self.onCancle)
        self.form = QFormLayout()
        self.form.addRow(self.nameLabel, self.nameInput)
        self.form.addRow(self.authorLabel, self.authorInput)
        self.form.addRow(self.languageLabel, self.languageInput)
        self.form.addRow(self.ratingLabel, self.ratingInput)
        self.form.addRow(self.okBtn, self.cancleBtn)
        self.setLayout(self.form)

    def onClicked(self):
        name = self.nameInput.text()
        authors = parseStrListString(self.authorInput.text())
        language = self.languageInput.text()
        if self.ratingInput.text():
            rating = int(self.ratingInput.text())
        else:
            rating = 0
        self.changeSignal.emit(name, authors, language, rating)
        self.close()

    def onCancle(self):
        self.close()


class ImportFileDialog(QDialog):
    finishSignal = pyqtSignal(str, str, list, str, int)

    def __init__(self, basepath, db, parent=None):
        super(ImportFileDialog, self).__init__(parent)
        self.basePath = basepath
        self.db = db
        self.filepath, _ = QFileDialog.getOpenFileName(self, "选择文件", ".", "docx or markdown file(*.docx *.md)")
        if self.filepath:
            direcPath, file = os.path.split(self.filepath)
            self.filename, self.filesufix = file.split('.')
            dig = ImportFileEditDialog(self.filename, self)
            dig.changeSignal.connect(self.onConvert)
            dig.show()

    def onConvert(self, name, authors, language, rating):
        if not name:
            name = self.filename
        bookPath, bookFilePath = getFilePath(self.basePath, name, self.db.getID(), self.filepath)
        if not bookPath:
            return
        pdfFilePath = os.path.join(bookPath, name+'.pdf')
        if self.filesufix == 'md':
            t = convertThread(mdToPdf, (bookFilePath, pdfFilePath))
        else:  # docx
            t = convertThread(docxToPdf, (bookFilePath, pdfFilePath))
        t.finishSignal.connect(lambda: self.finishConvert(pdfFilePath, name, authors, language, rating))
        t.start()
        time.sleep(1)

    def finishConvert(self, pdfFilePath, name, authors, language, rating):
        self.finishSignal.emit(pdfFilePath, name, authors, language, rating)


class ExportINFODialog(QDialog):
    finishSignal = pyqtSignal(str)

    def __init__(self, db: MyDb, parent=None):
        super(ExportINFODialog, self).__init__(parent)
        self.db = db
        file_name, _ = QFileDialog.getSaveFileName(self, "保存文件", ".", "csv file(*.csv)")
        if file_name:
            rows = self.db.getAllBookRows()
            headers = ['书名', '作者', '出版日期', '出版社', 'ISBN', '语言', '文件路径', '封面路径', '评分', '标签', '书单']
            t = convertThread(toCSV, (file_name, headers, rows))
            t.finishSignal.connect(lambda: self.FinishExport(file_name))
            t.start()
            time.sleep(1)

    def FinishExport(self, filename):
        self.finishSignal.emit(filename)


class SettingDialog(QDialog):
    finishSignal = pyqtSignal()

    def __init__(self, parent=None):
        super(SettingDialog, self).__init__(parent)


class HighSearchDialog(QDialog):
    finishSignal = pyqtSignal()

    def __init__(self, parent=None):
        super(HighSearchDialog, self).__init__(parent)
