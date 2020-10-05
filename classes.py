# 此文件存储核心的类和和类相关的方法
import re
from basic import strListToString
import fitz
import shutil
import os


class Book:
    def __init__(self, ID=0, name="", authors=None, pub_date="", publisher="", isbn="", language="", cover_path="",
                 rating=0, file_path="", tags=None, bookLists=None):
        if bookLists is None:
            bookLists = []
        if tags is None:
            tags = []
        if authors is None:
            authors = []
        self.ID = ID  # 序号，每本书的序号将作为它的关键码，不能有重复，对用户是不可见的
        self.name = name
        self.authors = authors
        self.pub_date = pub_date
        self.publisher = publisher
        self.isbn = isbn  # 以字符串形式存储
        self.language = language
        self.cover_path = cover_path  # 封面的存储位置，通过此信息加载封面
        self.rating = rating  # 评分，int型数据，1星到5星，0表示未评分
        self.file_path = file_path  # 文件位置，可以根据此信息打开文件
        self.tags = tags  # 书籍的标签，列表
        self.bookLists = bookLists  # 所属的书单，列表
        self.isOpen = False  # 书籍是否已经打开

    def getMetadata(self):
        doc = fitz.open(self.file_path)
        return doc.metadata
        # metadata['author']作者，['title']:标题，['modData']:修改时间

    def setMetadata(self):
        data = self.getMetadata()
        data['author'] = strListToString(self.authors)
        data['title'] = self.name

    def getToC(self):
        data = self.getMetadata()
        return data.getToC()

    def getModDate(self):
        data = self.getMetadata()
        return data['modData']

    # 应该调用此方法修改作者，而非直接通过属性修改
    def setAuthors(self, db, new_authors):
        for author in self.authors:
            obj = db.getAuthorByName(author)
            if obj:
                obj.deleteBook(db, self.ID)
        self.authors = new_authors
        self.updateDB(db)
        for author in self.authors:
            obj = db.getAuthorByName(author)
            if not obj:  # 该作者不在数据库中
                obj = Author(author, [])
                db.addAuthor(obj)
            obj.addBook(db, self.ID)

    # 把当前书添加到某个书单中
    # 传入一个BookList对象
    def addToList(self, db, booklist_name):
        booklist = db.getBookListByName(booklist_name)
        if not booklist:  # 不存在，将创建一个新书单
            booklist = BookList(booklist_name, [])
            db.addBooklist(booklist)
        booklist.addBook(db, self.ID)
        if booklist_name not in self.bookLists:
            self.bookLists.append(booklist_name)

    # 传入书单名数组
    def setBookLists(self, db, bookLists):
        for bookList in self.bookLists:
            obj = db.getBookListByName(bookList)
            if obj:
                obj.deleteBook(db, self.ID)
        for boolist in bookLists:
            self.addToList(db, boolist)

    # 每次修改信息后需主动调用updateDB()方法
    # 修改数据库内书籍的信息
    def updateDB(self, db):
        db.updateBook(self)

    # 删除书籍
    def delete(self, db):
        for author in self.authors:
            obj = db.getAuthorByName(author)
            if obj:
                obj.deleteBook(db, self.ID)
        for booklist in self.bookLists:
            obj = db.getBookListByName(booklist)
            if obj:
                obj.deleteBook(db, self.ID)
        path, file = os.path.split(self.file_path)
        shutil.rmtree(path)
        db.deleteBook(self.ID)

    def hasAnthorFuzzy(self, author_name):  # 模糊搜索
        for author in self.authors:
            if author_name in author:
                return True
        return False

    def hasAuthorRegExp(self, author_name):
        for author in self.authors:
            if re.match(author_name, author):
                return True
        return False

    def inBooklistFuzzy(self, booklist_name):
        for booklist in self.bookLists:
            if booklist_name in booklist:
                return True
        return False

    def inBooklistRegExp(self, booklist_name):
        for booklist in self.bookLists:
            if re.match(booklist_name, booklist):
                return True
        return False

    def hasTagFuzzy(self, tag_name):
        for tag in self.tags:
            if tag_name in tag:
                return True
        return False

    def hasTagRegExp(self, tag_name):
        for tag in self.tags:
            if re.match(tag_name, tag):
                return True
        return False

    # 打开当前书籍
    def openBook(self):
        self.isOpen = True
        # 与UI界面的按钮对接，打开阅读器窗口

    # 关闭当前书籍
    def closeBook(self):
        # 与UI界面按钮对接，关闭书籍是记得调用此函数以改变isOpen的状态
        self.isOpen = False

    # 自动生成封面，可选功能
    def generateCover(self):
        pass

    # 生成二维码，分享给别人，可选功能
    def QRcode(self):
        pass


class Author:
    def __init__(self, name, books=None):
        if books is None:
            books = []
        self.name = name
        self.books = books  # 书籍的ID列表

    # 传入Book对象的ID属性
    def addBook(self, db, book_id):
        self.books.append(book_id)
        self.updateDB(db)

    def deleteBook(self, db, book_id):
        if book_id in self.books:
            self.books.remove(book_id)
            if not self.books:
                # 已经没有该作者写的书了，应该在数据库中删去该作者的信息
                db.deleteAuthor(self.name)
            else:
                self.updateDB(db)

    # 更新数据库的信息
    def updateDB(self, db):
        db.updateAuthor(self)


class BookList:
    def __init__(self, name, books=None):
        if books is None:
            books = []
        self.name = name
        self.books = books  # 书籍的ID列表

    # 传入一个Book对象的ID属性
    def addBook(self, db, book_id):
        self.books.append(book_id)
        self.updateDB(db)

    def deleteBook(self, db, book_id):
        if book_id in self.books:
            self.books.remove(book_id)
        # 书单内书的数量为空时，不需要删去该书单
            self.updateDB(db)

    def delete(self, db):
        db.deleteBooklist(self)

    # 更新数据库信息
    def updateDB(self, db):
        db.updateBooklist(self)

    # 可选功能，书单分享，生成一张分享图片
    def share(self):
        pass

