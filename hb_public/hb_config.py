import json

def GetCurFileDir():
    path = sys.path[0]
    if os.path.isdir(path):
        return path
    elif os.path.isfile(path):
        return os.path.dirname(path)


def ReadMisstionConfig(fileName):
    configPath = GetCurFileDir()
    configPath += fileName
    fileJson = open(configPath, 'r', encoding='utf8')
    fileJsonData = '{}'
    try:
        fileJsonData = fileJson.read()
    except IOError:
        print("Read file failed: %s" % (configPath))
    finally:
        fileJson.close()
    return json.loads(fileJsonData)