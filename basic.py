# 此文件存储基础方法


# 解析用户输入的tag字符串，
# 输入支持语法 `tag1, tag2, tag3, tag4`，应该允许用户输入多余的空格，但是显示的时候不显示多余的空格
# 此函数将将输入字符串转换成列表[tag1, tag2, tag3, tag4]并返回
def parseTags(input_str):
    temp_list = input_str.split(',')
    tag_list = []
    for i in temp_list:
        tag_list.append(i.strip())
    return tag_list


# 此函数将解析后的tag列表再转换成一个字符串
def tagsToString(tag_list):
    if not tag_list:
        return ""
    tag_str = ""
    for tag in tag_list:
        tag_str += tag
        tag_str += ", "
    tag_str -= ", "
    return tag_str


def parseListString(list_str):
    return parseTags(list_str)


def listToString(olist):
    return tagsToString(olist)



