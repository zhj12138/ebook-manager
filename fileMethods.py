# 此文件存储pdf文件相关方法
import fitz
import os
from classes import *


def readInFile(file_path):
    doc = fitz.open(file_path)
    name = getTitle(doc)
    authors = getAuthors(doc)
    pub_date = getPubDate(doc)
    createNewBook(name, authors, pub_date)


def getTitle(doc):
    if doc.metadata['title']:
        return doc.metadata['title']
    else:
        name = doc.name[:-4]
        return name


def getAuthors(doc):
    if doc.metadata['author']:
        authors = parseListString(doc.metadata)
        return authors
    else:
        return None


def getPubDate(doc):
    if doc.metadata['creationDate']:
        return doc.metadata['createDate'][2:10]  # 格式：20200922
    return None


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
