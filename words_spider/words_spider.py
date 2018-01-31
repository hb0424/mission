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
from string import Template
import sqlite3


# create table words
#(
# word_id INTEGER UNIQUE NOT NULL Primary Key autoincrement,
# word VARCHAR(256) NOT NULL,
# word_meaning VARCHAR(2048)
#)
#create table users
#(
# user_id INTEGER UNIQUE NOT NULL Primary Key autoincrement,
# user_name VARCHAR(256) NOT NULL,
# user_email VARCHAR(256) NOT NULL,
# user_last_id INTEGER NOT NULL,
# send_count INTEGER NOT NULL
#)

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
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
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


def parseHtml(url):
    strHtml = DecodeBytes(download(url))
    lists = re.findall(
        '<a href="([a-z//0-9]+)">(wordlist [0-9/-]+)</a>', strHtml)
    if len(lists) <= 0:
        print("无法解析单词分组列表")
        return
    databasePath = GetCurFileDir()
    databasePath += '\\words.db'
    conn = sqlite3.connect(databasePath)
    wordId = 0
    allWord = {}
    for wordList in lists:
        wordListUrl = wordList[0].strip(" \r\n\\")
        wordListName = wordList[1].strip(" \r\n\\")
        i = 1
        while i < 6:
            strUrl = 'https://www.shanbay.com/' + wordListUrl
            strUrl = strUrl + "?page="
            s = Template("$index")
            strUrl += s.substitute(index=i)
            strHtmlWords = DecodeBytes(download(strUrl))
            wordRows = re.findall(
                ' <tr class="row">([.\s\S]+?)</tr>\\n', strHtmlWords)
            for wordRow in wordRows:
                words = re.findall(
                    '<td class="span2"><strong>(.*?)</strong></td>', wordRow)
                wordMeans = re.findall(
                    '<td class="span10">([.\s\S]*?)</td>', wordRow)
                if len(words) <= 0:
                    continue
                if len(wordMeans) <= 0:
                    continue
                if words[0] in allWord:
                    continue
                allWord[words[0]] = True
                try:
                    cursor = conn.cursor()
                    results = cursor.execute("INSERT INTO words (word_id, word, word_meaning) \
                        VALUES (NULL, ?, ?)", [words[0], wordMeans[0]])
                    books = results.fetchall()
                    bookId = results.lastrowid
                except (sqlite3.Error,) as e:
                    print('sqlite3 error: ' + str(e.args))
                    conn.commit()
            i = i + 1
    conn.commit()
    conn.close()


def main():
    parseHtml('https://www.shanbay.com/wordbook/103867/')
    print("爬取完成")


if __name__ == '__main__':
    main()
