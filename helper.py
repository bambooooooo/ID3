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
    
# 2. log2() --> same as log, but for deeper logs that can be also disabled
    
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

# 3. getColumnFromFile --> get list of column that takes place in the first row of file
    
def getColumnFromFile(source):
    try:
        file = open(source)
        columnList = str(file.readline())
        columnList = columnList.replace("\n", "")
        columnList = columnList.split(';')
        file.close()
        return columnList
    except FileNotFoundError:
        log("Train data file ["+s.trainFile+"] does not exists", "e")
        return False

# 4. getDataFromFile --> return list of object row each row of data
def getDataFromFile(source):
    columnList = getColumnFromFile(source)
    
    if not columnList:
        return False
    
    file = open(source)
    tmp = str(file.readline())   #TODO: move caret in better way, cos it sucks
    
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
    input('[ DEBUG ] Waiting for key...') # Debbuger Break Point HERE

