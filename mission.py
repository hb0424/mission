import json
import sys
import os
import threading
import datetime
import time
import ctypes

# 定时器时间间隔(单位：秒)
gSysConfig = {"timerInterval": 60}


def MessageBox(title, details):
    ctypes.windll.user32.MessageBoxW(0, details, title, 4096)


def AsynMessageBox(title, details):
    timer = threading.Timer(0.1, MessageBox, (title, details))
    timer.start()


def GetCurFileDir():
    path = sys.path[0]
    if os.path.isdir(path):
        return path
    elif os.path.isfile(path):
        return os.path.dirname(path)


def ReadMisstionConfig():
    configPath = GetCurFileDir()
    configPath += '\\missions.json'
    fileJson = open(configPath, 'r', encoding='utf8')
    fileJsonData = '{}'
    try:
        fileJsonData = fileJson.read()
    except IOError:
        print("Read file failed: %s" % (configPath))
    finally:
        fileJson.close()
    return json.loads(fileJsonData)


def ParseMisstionDay(item):
    title = item["title"]
    details = item["details"]
    hour = item["hour"]
    minute = item["minute"]
    curTime = time.localtime(time.time())
    misstionDate = datetime.datetime(
        curTime.tm_year, curTime.tm_mon, curTime.tm_mday, hour, minute)
    dateDiff = misstionDate.now() - misstionDate
    if dateDiff.days >= 0 and dateDiff.seconds <= gSysConfig["timerInterval"]:
        AsynMessageBox(title, details)


def ParseMisstionWeek(item):
    title = item["title"]
    details = item["details"]
    hour = item["hour"]
    minute = item["minute"]
    curTime = time.localtime(time.time())
    misstionDate = datetime.datetime(
        curTime.tm_year, curTime.tm_mon, curTime.tm_mday, hour, minute)
    dateDiff = misstionDate.now() - misstionDate
    wday = item["DaysOfWeek"] - 1
    if curTime.tm_wday == wday and dateDiff.days >= 0 and dateDiff.seconds <= gSysConfig["timerInterval"]:
        AsynMessageBox(title, details)


def ParseMisstionHour(item):
    title = item["title"]
    details = item["details"]
    hour = item["hour"]
    curTime = time.localtime(time.time())
    start = item["start"]
    end = item["end"]
    if curTime.tm_min != 0:
        return
    if curTime.tm_hour < start or curTime.tm_hour > end:
        return
    if curTime.tm_hour % hour == 0:
        AsynMessageBox(title, details)


def ParseMisstionMinute(item):
    title = item["title"]
    details = item["details"]
    minute = item["minute"]
    curTime = time.localtime(time.time())
    start = item["start"]
    end = item["end"]
    if curTime.tm_hour < start or curTime.tm_hour > end:
        return
    if curTime.tm_min % minute == 0:
        AsynMessageBox(title, details)


def MisstionTimer():
    missionConfig = ReadMisstionConfig()
    missions = missionConfig.get("missions", [])
    for item in missions:
        enable = item.get("enable", True)
        if not enable:
            continue
        loop = item["loop"]
        if loop == "day":
            ParseMisstionDay(item)
        if loop == "week":
            ParseMisstionWeek(item)
        if loop == "hour":
            ParseMisstionHour(item)
        if loop == "minute":
            ParseMisstionMinute(item)


def main():
    while True:
        timer = threading.Timer(gSysConfig["timerInterval"], MisstionTimer)
        timer.start()
        timer.join()


if __name__ == '__main__':
    main()
