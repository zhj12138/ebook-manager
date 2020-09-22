# 此文件存储用户的设置，以及一些重要的参数
# 需要将这些信息存储到一个文件中
# 每次打开应用时需要从文件中读取相应的参数
# 目前计划使用json文件存储
class GlobalVar:
    book_table_created = False
    booklist_table_created = False
    author_table_created = False
    history_table_created = False
    CUR_ID = 0
