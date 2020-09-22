# 此文件存储核心的类和和类相关的方法
import sqlite3
from basic import parseListString, listToString, parseTags, tagsToString
import fitz
from settings import GlobalVar
from collections import deque
from time import ctime


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
        self.INFO = None
        self.isOpen = False  # 书籍是否已经打开

    def getMetadata(self):
        doc = fitz.open(self.INFO['file_path'])
        return doc.metadata
        # metadata['author']作者，['title']:标题，['modData']:修改时间

    def setMetadata(self):
        data = self.getMetadata()
        data['author'] = listToString(self.INFO['authors'])
        data['title'] = self.INFO['name']

    def getToC(self):
        data = self.getMetadata()
        return data.getToC()

    def getModDate(self):
        data = self.getMetadata()
        return data['modData']

    def updateINFO(self):
        self.INFO = createBookINFO(self.ID, self.name, self.authors, self.pub_date, self.publisher, self.isbn,
                                   self.language, self.cover_path, self.rating,
                                   self.file_path, self.tags, self.bookLists)

    # 应该调用此方法修改作者，而非直接通过属性修改
    def setAuthors(self, new_authors):
        for author in self.authors:
            obj = DataBase.getAuthorByName(author)
            obj.deleteBook(self.ID)
        self.authors = new_authors
        for author in self.authors:
            obj = DataBase.getAuthorByName(author)
            if not obj:  # 该作者不在数据库中
                obj = Author(author, [])
                DataBase.addAuthor(obj)
            obj.addBook(self.ID)

    # 把当前书添加到某个书单中
    # 传入一个BookList对象
    def addToList(self, booklist_name):
        booklist = DataBase.getBooksByList(booklist_name)
        if not booklist:  # 不存在，将创建一个新书单
            booklist = BookList(booklist_name, [])
            DataBase.addBooklist(booklist)
        booklist.addBook(self.ID)
        self.bookLists.append(booklist_name)

    # 每次修改信息后需主动调用updateDB()方法
    # 修改数据库内书籍的信息
    def updateDB(self):
        DataBase.updateBook(self)

    # 删除书籍
    def delete(self):
        DataBase.deleteBook(self)

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
    def addBook(self, book_id):
        self.books.append(book_id)
        self.updateDB()

    def deleteBook(self, book_id):
        if book_id in self.books:
            self.books.remove(book_id)
            if not self.books:
                # 已经没有该作者写的书了，应该在数据库中删去该作者的信息
                DataBase.deleteAuthor(self)
            else:
                self.updateDB()

    # 更新数据库的信息
    def updateDB(self):
        DataBase.updateAuthor(self)


class BookList:
    def __init__(self, name, books=None):
        if books is None:
            books = []
        self.name = name
        self.books = books  # 书籍的ID列表

    # 传入一个Book对象的ID属性
    def addBook(self, book_id):
        self.books.append(book_id)
        self.updateDB()

    def deleteBook(self, book_id):
        self.books.remove(book_id)
        # 书单内书的数量为空时，不需要删去该书单
        self.updateDB()

    def delete(self):
        DataBase.deleteBooklist(self)

    # 更新数据库信息
    def updateDB(self):
        DataBase.updateBooklist(self)

    # 可选功能，书单分享，生成一张分享图片
    def share(self):
        pass


class History:
    def __init__(self, size=5):
        self.histories = deque(maxlen=size)
        # 每一个history记录是一个元组(time,content)


class DataBase:
    db_name = "test.db"
    book_table = "bookTable"
    booklist_table = "booklistTable"
    author_table = "authorTable"
    history_table = "historyTable"

    @staticmethod
    def connect():
        conn = sqlite3.connect(DataBase.db_name)
        cursor = conn.cursor()
        return conn, cursor

    @staticmethod
    def close(conn):
        conn.commit()
        conn.close()

    # 新建书籍表, 记住建表操作只能进行一次
    @staticmethod
    def createBookTable():
        conn, cursor = DataBase.connect()
        cursor.execute("create table %s (ID int primary key, name text, authors text, pub_date text, publisher text, "
                       "isbn text, language text, cover_path text, rating int, file_path text, tags text, "
                       "booklists text)" % DataBase.book_table)
        DataBase.close(conn)

    # 新建书单表
    @staticmethod
    def createBooklistTable():
        conn, cursor = DataBase.connect()
        cursor.execute("create table %s (name text primary key, books text)" % DataBase.booklist_table)
        DataBase.close(conn)

    # 新建历史搜索表
    @staticmethod
    def createHistoryTable():
        conn, cursor = DataBase.connect()
        cursor.execute('create table %s (time text, content text primary key )' % DataBase.history_table)
        DataBase.close(conn)

    # 新建作者表
    @staticmethod
    def createAuthorTable():
        conn, cursor = DataBase.connect()
        cursor.execute('create table %s (name text primary key , books text)' % DataBase.author_table)
        DataBase.close(conn)

    # 获取所有书籍，返回一个Book类型的列表
    @staticmethod
    def getAllBooks():
        conn, cursor = DataBase.connect()
        ret = cursor.execute('select * from %s' % DataBase.book_table)
        DataBase.close(conn)
        books = parseRetBooks(ret)
        if not books:
            return None
        return books

    # 传入一个书籍ID，获取该书籍的INFO属性
    @staticmethod
    def getBookINFOByID(ID):
        conn, cursor = DataBase.connect()
        ret = cursor.execute('select * from %s where ID=%s' % (DataBase.book_table, ID))
        DataBase.close(conn)
        books = parseRetBooks(ret)
        if not books:
            return None
        return books[0].INFO

    # 对书籍进行模糊搜索, attr_name对应数据库表的相应属性名，value则是需要查询的值(不支持列表，只能单个查询)
    @staticmethod
    def getBooksFuzzy(attr_name, value):
        conn, cursor = DataBase.connect()
        ret = cursor.execute('select * from %s where %s like "%%%s%%" ' % (DataBase.book_table, attr_name, value))
        DataBase.close(conn)
        books = parseRetBooks(ret)
        if not books:
            return None
        return books

    # 对书籍进行精确的搜索
    @staticmethod
    def getBooksAccurate(attr_name, value):
        conn, cursor = DataBase.connect()
        ret = cursor.execute("select * from %s where %s='%s'" % (DataBase.book_table, attr_name, value))
        DataBase.close(conn)
        books = parseRetBooks(ret)
        if not books:
            return None
        return books

    # 获取所有书单
    @staticmethod
    def getAllBookLists():
        conn, cursor = DataBase.connect()
        ret = cursor.execute('select * from %s' % DataBase.booklist_table)
        DataBase.close(conn)
        booklists = parseRetBooklists(ret)
        if not BookList:
            return None
        return booklists

    # 根据书单名进行检索，返回书籍ID列表
    @staticmethod
    def getBooksByList(list_name):
        books = []
        conn, cursor = DataBase.connect()
        ret = cursor.execute("select * from %s where name='%s'" % (DataBase.booklist_table, list_name))
        for row in ret:
            ID = parseListString(row[2])
            books.append(ID)
        DataBase.close(conn)
        return books

    # 获取所有的历史记录，返回一个History列表
    @staticmethod
    def getAllHistory(history):
        conn, cursor = DataBase.connect()
        ret = cursor.execute('select * from %s' % DataBase.history_table)
        for row in ret:
            time = row[0]
            content = row[1]
            history.histories.append((time, content))
        DataBase.close(conn)

    # 获取所有作者
    @staticmethod
    def getAllAuthors():
        conn, cursor = DataBase.connect()
        ret = cursor.execute('select * from %s' % DataBase.author_table)
        DataBase.close(conn)
        authors = parseRetAuthors(ret)
        if not authors:
            return None
        return authors

    # 根据作者名进行检索，返回书籍ID列表
    @staticmethod
    def getBooksByAuthor(author_name):
        conn, cursor = DataBase.connect()
        ret = cursor.execute("select * from %s where name='%s'" % (DataBase.author_table, author_name))
        books = []
        for row in ret:
            ID = parseListString(row[2])
            books.append(ID)
        DataBase.close(conn)
        if not books:
            return None
        return books

    # 传入一个作者的name，获取相应的Author对象
    @staticmethod
    def getAuthorByName(name):
        conn, cursor = DataBase.connect()
        ret = cursor.execute("select * from %s where name='%s'" % (DataBase.author_table, name))
        DataBase.close(conn)
        authors = parseRetAuthors(ret)
        if not authors:
            return None
        return authors[0]

    # 传入一个Book对象，添加到数据库中
    @staticmethod
    def addBook(book):
        conn, cursor = DataBase.connect()
        cursor.execute("insert into %s values(%s, '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s' ,'%s')" % (
            DataBase.book_table, book.ID, book.name, listToString(book.authors), book.pub_date, book.publisher,
            book.isbn, book.language, book.cover_path, book.rating, book.file_path, listToString(book.tags),
            listToString(book.bookLists)))
        DataBase.close(conn)

    # 传入一个Book对象，从数据库中删除
    @staticmethod
    def deleteBook(book):
        conn, cursor = DataBase.connect()
        cursor.execute('delete from %s where id=%s' % (DataBase.book_table, book.ID))
        DataBase.close(conn)

    # 传入一个Book对象，更新数据库中的数据
    @staticmethod
    def updateBook(book):
        conn, cursor = DataBase.connect()
        cursor.execute("update %s set name='%s', authors='%s', pub_date='%s', publisher='%s', isbn='%s', "
                       "language='%s', cover_path='%s', rating='%s', file_path='%s', tags='%s', booklists='%s' where "
                       "ID=%s" % (
                           DataBase.book_table, book.name, listToString(book.authors), book.pub_date, book.publisher,
                           book.isbn, book.language, book.cover_path, book.rating, book.file_path,
                           listToString(book.tags),
                           listToString(book.bookLists), book.ID))
        DataBase.close(conn)

    # 传入一个Book对象，倘若书籍在数据库中，则返回True,否则返回False
    @staticmethod
    def bookInDB(book):
        if not DataBase.getBookINFOByID(book.ID):
            return False
        return True

    # 传入一个Author对象，倘若作者在数据库中，返回True，否则False
    @staticmethod
    def authorInDB(author):
        if not DataBase.getAuthorByName(author.name):
            return False
        return True

    @staticmethod
    def addAuthor(author):
        conn, cursor = DataBase.connect()
        cursor.execute("insert into %s values('%s', '%s')" % (DataBase.author_table, author.name,
                                                              listToString(author.books)))
        DataBase.close(conn)

    @staticmethod
    def deleteAuthor(author):
        conn, cursor = DataBase.connect()
        cursor.execute("delete from %s where name='%s'" % (DataBase.author_table, author.name))
        DataBase.close(conn)

    @staticmethod
    def updateAuthor(author):
        conn, cursor = DataBase.connect()
        cursor.execute("update %s set books='%s' where name='%s'" % (DataBase.author_table, listToString(author.books),
                                                                     author.name))
        DataBase.close(conn)

    @staticmethod
    def historyInDB(content):
        conn, cursor = DataBase.connect()
        ret = cursor.execute("select * from %s where content='%s'" % (DataBase.history_table, content))
        histories = []
        for row in ret:
            time = row[0]
            content = row[1]
            histories.append((time, content))
        if not histories:
            return False
        return True

    @staticmethod
    def addHistory(time, content):
        conn, cursor = DataBase.connect()
        cursor.execute("insert into %s values('%s', '%s')" % (DataBase.history_table, time, content))
        DataBase.close(conn)

    @staticmethod
    def deleteHistory(content):
        conn, cursor = DataBase.connect()
        cursor.execute("delete from %s where content='%s'" % (DataBase.history_table, content))
        DataBase.close(conn)

    @staticmethod
    def updateHistory(time, content):
        conn, cursor = DataBase.connect()
        cursor.execute("update %s set time='%s' where content='%s'" % (DataBase.history_table, time, content))
        DataBase.close(conn)

    @staticmethod
    def booklistInDB(booklist):
        if not DataBase.getBooksByList(booklist.name):
            return False
        return True

    @staticmethod
    def addBooklist(booklist):
        conn, cursor = DataBase.connect()
        cursor.execute("insert into %s values('%s', '%s')" % (DataBase.booklist_table, booklist.name,
                                                              listToString(booklist.books)))
        DataBase.close(conn)

    @staticmethod
    def deleteBooklist(booklist):
        conn, cursor = DataBase.connect()
        cursor.execute("delete from %s where name='%s'" % (DataBase.booklist_table, booklist.name))
        DataBase.close(conn)

    @staticmethod
    def updateBooklist(booklist):
        conn, cursor = DataBase.connect()
        cursor.execute("update %s set books='%s' where name='%s'" % (DataBase.booklist_table,
                                                                     listToString(booklist.books), booklist.name))
        DataBase.close(conn)


def createBookINFO(ID=0, name="", authors=None, pub_date="", publisher="", isbn="", language="", cover_path="",
                   rating=0, file_path="", tags=None, bookLists=None):
    # cover_path, 封面的存储位置，通过此信息加载封面
    # rating, 评分，int型数据，1星到5星，0表示未评分
    # file_path, 文件位置，可以根据此信息打开文件
    # tags, 书籍的标签，列表
    # bookLists, 所属的书单，列表
    if bookLists is None:
        bookLists = []
    if tags is None:
        tags = []
    if authors is None:
        authors = []
    info = {'ID': ID, 'name': name, 'authors': authors, 'pub_data': pub_date, 'publisher': publisher, 'isbn': isbn,
            'language': language, 'cover_path': cover_path, 'rating': rating, 'file_path': file_path, 'tags': tags,
            'bookLists': bookLists}

    return info


# 每次加入一本新书的时候调用该函数，将为该书分配ID，并将该书加入数据库中
def createNewBook(name="", authors=None, pub_date="", publisher="", isbn="", language="", cover_path="",
                  rating=0, file_path="", tags=None, bookLists=None):
    GlobalVar.CUR_ID += 1
    ID = GlobalVar.CUR_ID
    print(ID)
    book = Book(ID, name, authors, pub_date, publisher, isbn, language, cover_path, rating, file_path, tags,
                bookLists)
    book.setAuthors(authors)
    DataBase.addBook(book)
    return book


# 每次新建一个书单时调用该方法
# 新建书单的两种方式：1、通过按钮新建一个空书单 2、通过书籍的右键菜单，添加到书单，如果用户填写的书单不存在，将自动新建一个书单，
# 并将相应的书籍添加进去
def createNewBooklist(name):
    booklist = BookList(name, [])
    DataBase.addBooklist(booklist)
    return booklist


# 不提供主动新建作者的方法
def addHistory(content):
    time = ctime()
    if DataBase.historyInDB(content):
        DataBase.updateHistory(time, content)
    else:
        DataBase.addHistory(time, content)


def deleteHistory(content):
    DataBase.deleteHistory(content)


def parseRetBooks(ret):
    books = []
    for row in ret:
        ID = row[0]
        name = row[1]
        authors = parseListString(row[2])
        pub_date = row[3]
        publisher = row[4]
        isbn = row[5]
        language = row[6]
        cover_path = row[7]
        rating = row[8]
        file_path = row[9]
        tags = parseTags(row[10])
        booklists = parseListString(row[11])
        book = Book(ID, name, authors, pub_date, publisher, isbn, language, cover_path, rating, file_path, tags,
                    booklists)
        books.append(book)
    return books


def parseRetBooklists(ret):
    booklists = []
    for row in ret:
        name = row[0]
        ID = parseListString(row[1])
        booklist = BookList(name, ID)
        booklists.append(booklist)
    return booklists


def parseRetAuthors(ret):
    authors = []
    for row in ret:
        name = row[0]
        books = parseListString(row[1])
        author = Author(name, books)
        authors.append(author)
    return authors
