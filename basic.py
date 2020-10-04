# 此文件存储基础方法


# 解析字符串
def parseStrListString(input_str):
    if not input_str:
        return []
    temp_list = input_str.split(',')
    tag_list = []
    for i in temp_list:
        tag_list.append(i.strip())
    return tag_list


# 此函数将str列表转换成一个字符串
def strListToString(tag_list):
    if not tag_list:
        return ""
    tag_str = ", ".join(tag_list)
    return tag_str


# 将字符串转换成一个int型列表
def parseIntListString(list_str: str):
    if not list_str:
        return []
    temp_list = list_str.split(',')
    mylist = []
    for i in temp_list:
        mylist.append(int(i.strip()))
    return mylist


# 将int型列表转换成字符串
def intListToString(olist):
    if not olist:
        return ""
    str_list = [str(i) for i in olist]
    return strListToString(str_list)



