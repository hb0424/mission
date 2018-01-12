import re
import urllib.request
import urllib.parse
import json
import sys
import os
import threading
import datetime
import time
import ctypes
from novels import gNoversConfig
import sqlite3
from string import Template
#create table books
#(
# book_id INTEGER UNIQUE NOT NULL Primary Key autoincrement,
# book_name VARCHAR(256) NOT NULL,
# book_author VARCHAR(256),
# book_summary VARCHAR(2048)
#)
#
#create table chapters
#(
# chapter_id INTEGER UNIQUE NOT NULL Primary Key autoincrement,
# book_id INTEGER  NOT NULL,
# book_source VARCHAR(256) NOT NULL,
# book_chapter_name VARCHAR(256),
# book_chapter_url VARCHAR(2048),
# book_chapter_content TEXT(100000)
#)
#
#CREATE INDEX index_book_name
#ON books (book_name)
#
#CREATE INDEX index_book_id
#ON chapters (book_id)
#
#CREATE INDEX index_book_source
#ON chapters (book_source)
#
#CREATE INDEX index_book_chapter_name
#ON chapters (book_chapter_name)


def GetCurFileDir():
    path = sys.path[0]
    if os.path.isdir(path):
        return path
    elif os.path.isfile(path):
        return os.path.dirname(path)

def DecodeBytes(byteHtml):
    decodeTypes = ["utf-8", "gbk", "gb2312", "gb18030", "hz", "utf_16"]
    for decodeType in decodeTypes:
        try:
            strHtml = byteHtml.decode(decodeType)
        except UnicodeDecodeError as e:
            continue
        except UnicodeError as e:
            continue
        else:
            return strHtml
    

def download(url, num_retries=3):
    print('Downloading[', num_retries, ']:',  url)
    html = None
    try:
        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
        req = urllib.request.Request(url=url, headers=headers)
        html = urllib.request.urlopen(req).read()
    except urllib.error.HTTPError as e:
        print('Download HTTPError: ' + e.reason)
        html = None
        if num_retries > 0:
            return download(url, num_retries - 1)
    except urllib.error.URLError as e:
        print("download URLError: " + str(e.args))
        html = None
        if num_retries > 0:
            return download(url, num_retries - 1)
    except TimeoutError as e:
        print("download timeout: " + url)
        html = None
        if num_retries > 0:
            return download(url, num_retries - 1)
    except Exception as e:
        print("download Exception: " + url)
        html = None
        if num_retries > 0:
            return download(url, num_retries - 1)

    return html


def parseHtml(url, webRoul):
    strHtml = DecodeBytes(download(url))
    bookNames = re.findall(webRoul["book_name"], strHtml)
    if len(bookNames) <= 0:
        print("无法解析书名")
        return
    bookName = bookNames[0].strip(" \r\n\\")
    print("开始爬取：" + bookName)

    bookAuthors = re.findall(webRoul["book_author"], strHtml)
    bookAuthor = ""
    if len(bookAuthors) > 0:
        bookAuthor = bookAuthors[0].strip(" \r\n\\")

    bookSummarys = re.findall(webRoul["book_summary"], strHtml)
    bookSummary = ""
    if len(bookSummarys) > 0:
        bookSummary = bookSummarys[0].strip(" \r\n\\")

    bookChapters = re.findall(webRoul["book_chapter"], strHtml)
    if len(bookChapters) <= 0:
        print("无法解析书目录" + bookName)
        return

    ################
    # books:
    # book_id book_name book_author book_summary
    # chapters:
    # chapter_id book_id book_source book_chapter_name book_chapter_url book_chapter_content
    # ############
    databasePath = GetCurFileDir()
    databasePath += '\\novels.db'
    conn = sqlite3.connect(databasePath)
    bookId = 0
    try:
        cursor = conn.cursor()
        # 取book_id,没有book_id则增加新书
        results = cursor.execute(
            "select book_id, book_name, book_author, book_summary from books WHERE book_name=?", [bookName])
        books = results.fetchall()
        if len(books) <= 0:
            results = cursor.execute("INSERT INTO books (book_id, book_name, book_author, book_summary) \
                VALUES (NULL, ?, ?, ?)",
                                     [bookName, bookAuthor, bookSummary])
            books = results.fetchall()
            bookId = results.lastrowid
        else:
            bookId = books[0][0]
    except (sqlite3.Error,) as e:
        print('sqlite3 error: ' + str(e.args))
        conn.commit()
        conn.close()
        return

    for bookChapter in bookChapters:
        bookChapterNames = re.findall(
            webRoul["book_chapter_name"], bookChapter)
        if len(bookChapterNames) <= 0:
            print("无法解析章节名：" + bookChapter + " " +
                  webRoul["book_chapter_name"])
            continue
        bookChapterName = bookChapterNames[0].strip(" \r\n\\")

        bookChapterUrls = re.findall(webRoul["book_chapter_url"], bookChapter)
        if len(bookChapterUrls) <= 0:
            print("无法解析章节地址：" + bookChapter +
                  " " + webRoul["book_chapter_url"])
            continue

        if len(webRoul["hostname"]) > 0:
            bookChapterUrl = webRoul["hostname"] + bookChapterUrls[0]
        else:
            bookChapterUrl = url + bookChapterUrls[0]
        # 取chapter_id,没有chapter_id则增加新章节
        try:
            results = cursor.execute("select chapter_id, book_id, book_source, book_chapter_name from chapters \
            WHERE book_id=? and book_source=? and book_chapter_name=?",
                                     [bookId, webRoul["webname"], bookChapterName])
            chapters = results.fetchall()
            if len(chapters) <= 0:
                contentHtml = download(bookChapterUrl)
                if contentHtml == None:
                    print("下载章节内容为空：" + bookChapterUrl)
                    continue
                strContentHtml = DecodeBytes(contentHtml)

                bookChapterContents = re.findall(
                    webRoul["book_chapter_content"], strContentHtml)
                if len(bookChapterContents) <= 0:
                    print("无法解析章节内容：" + bookChapterName + " " +
                          bookChapterUrl + " " + webRoul["book_chapter_content"])
                    continue
                bookChapterContent = bookChapterContents[0].strip(" \r\n\\")

                results = cursor.execute("INSERT INTO chapters (chapter_id, book_id, book_source, book_chapter_name, book_chapter_url, book_chapter_content) \
                    VALUES (NULL, ?, ?, ?, ?, ?)", [bookId, webRoul["webname"], bookChapterName, bookChapterUrl, bookChapterContent])
                print("新增章节：" + bookName + ":" + bookChapterName)
        except (sqlite3.Error,) as e:
            print('sqlite3 error: ' + str(e.args))
            continue
        conn.commit()
    conn.close()
    print("爬取完成：" + bookName)


def main():
    webSites = gNoversConfig["websites"]
    books = gNoversConfig['books']
    for book in books:
        urls = book["urls"]
        for url in urls:
            urlObj = urllib.parse.urlparse(url)
            webRoul = webSites[urlObj.hostname]
            parseHtml(url, webRoul)
     print("爬取完成所有书目")


if __name__ == '__main__':
    main()
