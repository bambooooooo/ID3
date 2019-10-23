import settings as s

# 1. log() --> print info, warning, error while debug mode is enabled

def log(text, level="l"):
    if s.debugMode == False:
        return True
    
    if level == "l":
        print("[ LOG ] ", text)
        return True
    elif level == "w":
        print("[ WARNING ] ", text)
        return True
    elif level == "e":
        print("[ ERROR ] ", text)
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

def getDataFromFile(source, columnList):
    file = open(source)
    tmp = str(file.readline())   #TODO: move carret in better way
    
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