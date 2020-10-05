import sqlite3
import time

from basic import parseIntListString, strListToString, intListToString, parseStrListString
from classes import BookList, Book, Author


class MyDb:
    def __init__(self, name):
        self.db_name = name
        self.book_table = "bookTable"
        self.booklist_table = "booklistTable"
        self.author_table = "authorTable"
        self.history_table = "historyTable"
        self.id_table = "idTable"
        self.email_table = 'emailTable'
        self.conn = None
        self.cursor = None
        try:
            self.createEmailTable()
            self.createAuthorTable()
            self.createBookTable()
            self.createHistoryTable()
            self.createBooklistTable()
            self.createIDTable()
        except:
            pass

    def connect(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()

    def close(self):
        self.conn.commit()
        self.conn.close()

    # 新建kindle邮箱表
    def createEmailTable(self):
        self.connect()
        self.cursor.execute("create table %s(mail text primary key )" % self.email_table)
        self.close()

    # 新建书籍表
    def createBookTable(self):
        self.connect()
        self.cursor.execute("create table %s (ID int primary key, name text, authors text, pub_date text, publisher "
                            "text, isbn text, language text, cover_path text, rating int, file_path text, tags text, "
                            "booklists text)" % self.book_table)
        self.close()

    # 新建书单表
    def createBooklistTable(self):
        self.connect()
        self.cursor.execute("create table %s (name text primary key, books text)" % self.booklist_table)
        self.close()

    # 新建历史搜索表
    def createHistoryTable(self):
        self.connect()
        self.cursor.execute('create table %s (time float, content text primary key )' % self.history_table)
        self.close()

    # 新建作者表
    def createAuthorTable(self):
        self.connect()
        self.cursor.execute('create table %s (name text primary key , books text)' % self.author_table)
        self.close()

    def createIDTable(self):
        self.connect()
        self.cursor.execute('create table %s (ID int primary key)' % self.id_table)
        self.cursor.execute("insert into %s values (1)" % self.id_table)
        self.close()

    def getID(self):
        self.connect()
        ret = self.cursor.execute('select * from %s' % self.id_table)
        ids = []
        for row in ret:
            ids.append(row[0])
        self.close()
        return ids[0]

    def updateID(self, ID):
        self.connect()
        # print("1")
        self.cursor.execute('delete from %s' % self.id_table)
        # print("2")
        self.cursor.execute('insert into %s values (%s)' % (self.id_table, ID))
        # print("3")
        self.close()

    # 获取所有书籍，返回一个Book类型的列表
    def getAllBooks(self):
        self.connect()
        ret = self.cursor.execute('select * from %s' % self.book_table)
        books = parseRetBooks(ret)
        # print("Ok")
        self.close()
        # print("Ok")
        if not books:
            return []
        return books

    def getAllBookRows(self):
        self.connect()
        ret = self.cursor.execute('select * from %s' % self.book_table)
        rows = parseRetBookRows(ret)
        # print("Ok")
        self.close()
        return rows

    def getAllBookNames(self):
        names = set()
        self.connect()
        ret = self.cursor.execute('select * from %s' % self.book_table)
        for row in ret:
            names.add(row[1])
        self.close()
        return names

    def getAllISBNs(self):
        isbns = set()
        self.connect()
        ret = self.cursor.execute('select * from %s' % self.book_table)
        for row in ret:
            isbns.add(row[5])
        self.close()
        return isbns

    # 传入一个书籍ID，获取该书籍，为Book类型
    def getBookByID(self, ID):
        self.connect()
        ret = self.cursor.execute('select * from %s where ID=%s' % (self.book_table, ID))
        books = parseRetBooks(ret)
        self.close()
        if not books:
            return []
        return books[0]

    # 对书籍进行模糊搜索, attr_name对应数据库表的相应属性名，value则是需要查询的值(不支持列表，只能单个查询)
    def getBooksFuzzy(self, attr_name, value):
        self.connect()
        ret = self.cursor.execute('select * from %s where %s like "%%%s%%" ' % (self.book_table, attr_name, value))
        books = parseRetBooks(ret)
        self.close()
        return books

    # 对书籍进行精确的搜索
    def getBooksAccurate(self, attr_name, value):
        self.connect()
        ret = self.cursor.execute("select * from %s where %s='%s'" % (self.book_table, attr_name, value))
        books = parseRetBooks(ret)
        self.close()
        return books

    # 获取所有书单
    def getAllBookLists(self):
        self.connect()
        ret = self.cursor.execute('select * from %s' % self.booklist_table)
        booklists = parseRetBooklists(ret)
        self.close()
        return booklists

    # 根据书单名进行检索，返回相应书单
    def getBookListByName(self, list_name):
        self.connect()
        ret = self.cursor.execute("select * from %s where name='%s'" % (self.booklist_table, list_name))
        booklists = parseRetBooklists(ret)
        self.close()
        if not booklists:
            return []
        return booklists[0]

    # 获取所有的历史记录，返回一个(time, content)列表
    def getAllHistory(self):
        self.connect()
        histories = []
        ret = self.cursor.execute('select * from %s' % self.history_table)
        for row in ret:
            t = row[0]
            content = row[1]
            histories.append((t, content))
        self.close()
        return histories

    # 获取所有作者
    def getAllAuthors(self):
        self.connect()
        ret = self.cursor.execute('select * from %s' % self.author_table)
        authors = parseRetAuthors(ret)
        self.close()
        return authors

    def getAllTags(self):
        taglists = [book.tags for book in self.getAllBooks()]
        tags = []
        for taglist in taglists:
            tags.extend(taglist)
        return set(tags)

    def getAllLanguages(self):
        languageList = {book.language for book in self.getAllBooks() if book.language != ''}
        return languageList

    def getAllPublishers(self):
        publisherList = {book.publisher for book in self.getAllBooks() if book.publisher != ''}
        return publisherList

    # 根据作者名进行检索，返回书籍ID列表
    def getBooksByAuthor(self, author_name):
        self.connect()
        ret = self.cursor.execute("select * from %s where name='%s'" % (self.author_table, author_name))
        books = []
        for row in ret:
            ID = parseIntListString(row[2])
            books.append(ID)
        self.close()
        return books

    # 传入一个作者的name，获取相应的Author对象
    def getAuthorByName(self, name):
        self.connect()
        ret = self.cursor.execute("select * from %s where name='%s'" % (self.author_table, name))
        authors = parseRetAuthors(ret)
        self.close()
        if not authors:
            return []
        return authors[0]

    # 传入一个Book对象，添加到数据库中
    def addBook(self, book):
        self.connect()
        self.cursor.execute("insert into %s values(%s, '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s' ,"
                            "'%s')" % (
                                self.book_table, book.ID, book.name, strListToString(book.authors), book.pub_date,
                                book.publisher, book.isbn, book.language, book.cover_path, book.rating,
                                book.file_path, strListToString(book.tags), strListToString(book.bookLists)))
        self.close()

    # 传入一个Book id，从数据库中删除
    def deleteBook(self, book_id):
        self.connect()
        self.cursor.execute('delete from %s where id=%s' % (self.book_table, book_id))
        self.close()

    # 传入一个Book对象，更新数据库中的数据
    def updateBook(self, book):
        self.connect()
        self.cursor.execute(
            "update %s set name='%s', authors='%s', pub_date='%s', publisher='%s', isbn='%s', language='%s',"
            " cover_path='%s', rating=%s, file_path='%s', tags='%s', booklists='%s' where ID=%s" % (
                self.book_table, book.name, strListToString(book.authors), book.pub_date,
                book.publisher, book.isbn, book.language, book.cover_path, book.rating,
                book.file_path, strListToString(book.tags), strListToString(book.bookLists), book.ID))
        self.close()

    # 传入一个Book Id，倘若书籍在数据库中，则返回True,否则返回False
    def bookInDB(self, book_id):
        if not self.getBookByID(book_id):
            return False
        return True

    # 传入一个Author name，倘若作者在数据库中，返回True，否则False
    def authorInDB(self, author_name):
        if not self.getAuthorByName(author_name):
            return False
        return True

    def addAuthor(self, author):
        self.connect()
        self.cursor.execute("insert into %s values('%s', '%s')" % (self.author_table, author.name,
                                                                   intListToString(author.books)))
        self.close()

    def deleteAuthor(self, author_name):
        self.connect()
        self.cursor.execute("delete from %s where name='%s'" % (self.author_table, author_name))
        self.close()

    def updateAuthor(self, author):
        self.connect()
        self.cursor.execute(
            "update %s set books='%s' where name='%s'" % (self.author_table, intListToString(author.books),
                                                          author.name))
        self.close()

    def historyInDB(self, content):
        self.connect()
        ret = self.cursor.execute("select * from %s where content='%s'" % (self.history_table, content))
        histories = []
        for row in ret:
            t = row[0]
            content = row[1]
            histories.append((t, content))
        self.close()
        if not histories:
            return False
        return True

    def addHistory(self, curtime, content):
        self.connect()
        self.cursor.execute("insert into %s values(%s, '%s')" % (self.history_table, curtime, content))
        self.close()

    def deleteHistory(self, content):
        self.connect()
        self.cursor.execute("delete from %s where content='%s'" % (self.history_table, content))
        self.close()

    def updateHistory(self, curtime, content):
        self.connect()
        self.cursor.execute("update %s set time=%s where content='%s'" % (self.history_table, curtime, content))
        self.close()

    def booklistInDB(self, booklist):
        if not self.getBookListByName(booklist.name):
            return False
        return True

    def addBooklist(self, booklist):
        self.connect()
        self.cursor.execute("insert into %s values('%s', '%s')" % (self.booklist_table, booklist.name,
                                                                   intListToString(booklist.books)))
        self.close()

    def deleteBooklist(self, booklist):
        self.connect()
        self.cursor.execute("delete from %s where name='%s'" % (self.booklist_table, booklist.name))
        self.close()

    def updateBooklist(self, booklist):
        self.connect()
        self.cursor.execute("update %s set books='%s' where name='%s'" % (self.booklist_table,
                                                                          intListToString(booklist.books),
                                                                          booklist.name))
        self.close()

    # 每次加入一本新书的时候调用该函数，将为该书分配ID，并将该书加入数据库中
    def createNewBook(self, name="", authors=None, pub_date="", publisher="", isbn="", language="", cover_path="",
                      rating=0, file_path="", tags=None, bookLists=None):
        ID = self.getID()
        ID += 1
        self.updateID(ID)
        book = Book(ID, name, None, pub_date, publisher, isbn, language, cover_path, rating, file_path, tags,
                    bookLists)
        self.addBook(book)
        if authors:
            book.setAuthors(self, authors)

    # 每次新建一个书单时调用该方法
    # 新建书单的两种方式：1、通过按钮新建一个空书单 2、通过书籍的右键菜单，添加到书单，如果用户填写的书单不存在，将自动新建一个书单，
    # 并将相应的书籍添加进去
    def createNewBooklist(self, name):
        booklist = BookList(name, [])
        self.addBooklist(booklist)
        # return booklist

    # 不提供主动新建作者的方法
    def addAHistory(self, content):
        curtime = time.time()
        if self.historyInDB(content):
            self.updateHistory(curtime, content)
        else:
            self.addHistory(curtime, content)

    def deleteAHistory(self, content):
        self.deleteHistory(content)

    def getAllKindleMail(self):
        self.connect()
        ret = self.cursor.execute("select * from %s" % self.email_table)
        emailList = []
        for row in ret:
            email = row[0]
            emailList.append(email)
        self.close()
        return emailList

    def mailInDB(self, mail):
        self.connect()
        ret = self.cursor.execute("select * from %s where mail='%s'" % (self.email_table, mail))
        tem = []
        for row in ret:
            tem.append(row)
        self.close()
        if not tem:
            return False
        return True

    def addKindleMail(self, email):
        self.connect()
        self.cursor.execute("insert into %s values ('%s')" % (self.email_table, email))
        self.close()


def parseRetBooks(ret):
    books = []
    for row in ret:
        ID = row[0]
        name = row[1]
        authors = parseStrListString(row[2])
        pub_date = row[3]
        publisher = row[4]
        isbn = row[5]
        language = row[6]
        cover_path = row[7]
        rating = row[8]
        file_path = row[9]
        tags = parseStrListString(row[10])
        booklists = parseStrListString(row[11])
        book = Book(ID, name, authors, pub_date, publisher, isbn, language, cover_path, rating, file_path, tags,
                    booklists)
        books.append(book)
    return books


def parseRetBookRows(ret):
    rows = []
    for row in ret:
        name = row[1]
        authors = row[2]
        pub_date = row[3]
        publisher = row[4]
        isbn = row[5]
        language = row[6]
        cover_path = row[7]
        rating = row[8]
        file_path = row[9]
        tags = row[10]
        booklists = row[11]
        rows.append((name, authors, pub_date, publisher, isbn, language, file_path, cover_path, rating, tags,
                     booklists))
    return rows


def parseRetBooklists(ret):
    booklists = []
    for row in ret:
        name = row[0]
        ID = parseIntListString(row[1])
        booklist = BookList(name, ID)
        booklists.append(booklist)
    return booklists


def parseRetAuthors(ret):
    authors = []
    for row in ret:
        name = row[0]
        books = parseIntListString(row[1])
        author = Author(name, books)
        authors.append(author)
    return authors
