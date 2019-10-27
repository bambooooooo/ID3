import settings as s

from termcolor import colored

# 1. log() --> print info, warning, error while debug mode is enabled

def log(text, level="l"):
    if s.debugMode == False:
        return True
    
    if level == "l":
        print(colored("[ LOG ] ", 'cyan'), text)
        return True
    elif level == "w":
        print(colored("[ WARNING ] ", 'yellow'), text)
        return True
    elif level == "e":
        print(colored("[ ERROR ] ", 'red'), text)
        return False
    else:
        print(text)
        return False
    
def log2(text, level="l"):
    if s.debugMode == False or s.deepDebug == False:
        return True
    
    if level == "l":
        print(colored("[ LOG ] ", 'cyan'), text)
        return True
    elif level == "w":
        print(colored("[ WARNING ] ", 'yellow'), text)
        return True
    elif level == "e":
        print(colored("[ ERROR ] ", 'red'), text)
        return False
    else:
        print(text)
        return False
    
def getColumnFromFile(source):
    file = open(source)
    columnList = str(file.readline())
    columnList = columnList.replace("\n", "")
    columnList = columnList.split(';')
    file.close()
    return columnList

def getDataFromFile(source):
    columnList = getColumnFromFile(source)
    
    file = open(source)
    tmp = str(file.readline())   #TODO: move caret in better way
    
    data = []
    
    row = file.readline()
    
    while row:
        itemData = str(row).replace("\n","").split(';')
        item = {}
        for i, column in enumerate(columnList):
            item[column] = itemData[i]
        data.append(item)
        row = file.readline()
    
    file.close()
    
    return data

def BP():
    input('[ DEBUG ] Waiting for key...')

'''TODO

getDataFromFile + logs in helper.py as for tree in main

'''
