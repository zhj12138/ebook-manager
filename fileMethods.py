# 此文件存储pdf文件相关方法
import fitz
import os
from basic import parseStrListString
import shutil
import PySimpleGUI as sg
import pdfkit
import markdown
import win32com.client as win32
from pdf2docx import parse
import csv


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
    bookPath = os.path.join(basePath, name + "_" + str(ID))  # 目录路径
    # print(bookPath)
    try:
        os.mkdir(name + "_" + str(ID))
    except:
        print("File exists")
        return None, None
    bookFilePath = shutil.copy(filename, bookPath)  # 新的文件路径
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


def docxToPdf(file_path: str, to_name: str):
    word = win32.gencache.EnsureDispatch('Word.Application')
    pdfForm = 17
    if os.path.exists(file_path):
        if file_path.endswith('.docx'):
            doc = word.Documents.Open(file_path)
            doc.SaveAs(to_name, FileFormat=pdfForm)
            doc.Close()


def picsToPdf(filenames: list, to_name: str):
    doc = fitz.open()
    total = len(filenames)
    count = 0
    for filename in filenames:
        count += 1
        if os.path.exists(filename) and filename.endswith(('.png', '.jpg', 'jpeg')):
            img = fitz.open(filename)
            rect = img[0].rect
            pdfbytes = img.convertToPDF()
            img.close()
            imgPdf = fitz.open("pdf", pdfbytes)
            page = doc.newPage(width=rect.width, height=rect.height)
            page.showPDFpage(rect, imgPdf, 0)
            sg.OneLineProgressMeter("convert images", count, total)
    doc.save(to_name)


def htmlToPdf(url, to_name):
    try:
        pdfkit.from_url(url, to_name)
    except:
        return False
    else:
        return True


def mdToPdf(file_path, to_name):
    extensions = [
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        'markdown.extensions.legacy_em',
        'markdown.extensions.toc',
        'markdown.extensions.wikilinks',
        'markdown.extensions.admonition',
        'markdown.extensions.legacy_attrs',
        'markdown.extensions.meta',
        'markdown.extensions.nl2br',
        'markdown.extensions.sane_lists',
        'markdown.extensions.smarty',
    ]
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()
    html = markdown.markdown(text, output_format='html', extensions=extensions)
    pdfkit.from_string(html, to_name, options={'encoding': 'utf-8'})


def tocToMd(file_path, to_name):
    f = open(to_name, "w", encoding='utf-8')
    doc = fitz.open(file_path)
    toc = doc.getToC()
    print("[TOC]", file=f)
    if doc.metadata['title']:
        title = doc.metadata['title']
    else:
        title = doc.name.split('/')[-1][:-4]
    print("# " + title, file=f)
    for line in toc:
        layer, title, page = line
        if layer >= 6:
            continue
        print((layer + 1) * '#' + " " + title, file=f)
    f.close()


def pdfToImg(file_path, to_path):
    doc = fitz.open(file_path)
    total = doc.pageCount
    for i, page in enumerate(doc):
        pix = page.getPixmap()
        pix.writeImage(os.path.join(to_path, "{}.png".format(i + 1)))
        sg.OneLineProgressMeter("converting to image", i + 1, total)


def pdfToHtmlorTxt(file_path, to_path, type):
    doc = fitz.open(file_path)
    total = doc.pageCount
    f = open(to_path, 'w', encoding='utf-8')
    for i, page in enumerate(doc):
        text = page.getText(type)
        print(text, file=f)
        sg.OneLineProgressMeter("converting to html", i + 1, total)
    f.close()


def pdfToDocx(file_path, to_path):
    doc = fitz.open(file_path)
    count = doc.pageCount
    parse(file_path, to_path, start=0, end=count - 1)


def toCSV(filename, headers, rows):
    with open(filename, 'w') as f:
        f_csv = csv.writer(f)
        f_csv.writerow(headers)
        f_csv.writerows(rows)
