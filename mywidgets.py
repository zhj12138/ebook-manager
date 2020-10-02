from PyQt5.QtWidgets import QTreeWidget, QTableWidget, QListWidget, QWidget


class MyTree(QTreeWidget):
    def __init__(self):
        super(MyTree, self).__init__()


class MyTable(QTableWidget):
    def __init__(self):
        super(MyTable, self).__init__()


class MyList(QListWidget):
    def __init__(self):
        super(MyList, self).__init__()


class MySearch(QWidget):
    def __init__(self):
        super(MySearch, self).__init__()
