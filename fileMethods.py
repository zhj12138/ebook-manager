# 此文件存储pdf文件相关方法
import fitz
import os

from basic import parseStrListString
from classes import *
import shutil


def getTitle(doc):
    if doc.metadata['title']:
        return doc.metadata['title'].replace(' ', '_')
    else:
        name = doc.name.split('/')[-1][:-4]
        return name.replace(' ', '_')


def getAuthors(doc):
    if doc.metadata['author']:
        authors = parseStrListString(doc.metadata['author'])
        return authors
    else:
        return None


def getPubDate(doc):
    if doc.metadata['creationDate']:
        return doc.metadata['creationDate'][2:10]  # 格式：20200922
    return None


def getFilePath(basePath, name, ID, filename):
    if not os.path.exists(basePath):
        return
    os.chdir(basePath)
    bookPath = os.path.join(basePath, name+"_"+str(ID))
    # print(bookPath)
    try:
        os.mkdir(name+"_"+str(ID))
    except:
        print("File exists")
    bookFilePath = shutil.copy(filename, bookPath)
    # print(bookFilePath)
    return bookPath, bookFilePath


def getCover(doc, bookPath):
    zoom_x = 0.666  # horizontal zoom
    zomm_y = 0.666  # vertical zoom
    mat = fitz.Matrix(zoom_x, zomm_y)  # zoom factor 2 in each dimension
    pix = doc[0].getPixmap(matrix=mat)
    coverPath = os.path.join(bookPath, "cover.png")
    pix.writeImage(coverPath)
    return coverPath


def convertToTXT(file_path, to_path):
    doc = fitz.open(file_path)
    with open(to_path, 'w', encoding='utf-8') as f:
        for page in doc:
            text = page.getText('text')
            f.write(text)


def convertToHTML(file_path, to_path):
    doc = fitz.open(file_path)
    with open(to_path, 'w', encoding='utf-8') as f:
        for page in doc:
            text = page.getText('html')
            f.write(text)


def convertToPNG(file_path, to_path, from_page, to_page=-1):
    doc = fitz.open(file_path)
    os.chdir(to_path)
    os.mkdir('img')
    os.chdir('img')
    if to_page < from_page:
        pass


def subPDF(file_path, from_page, to_page=-1):
    doc = fitz.open()
    if to_page < from_page:
        pass

# 文件转换除了自己提供的简单转换外，计划支持pandoc的文件转换
