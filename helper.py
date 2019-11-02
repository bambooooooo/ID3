import settings as s
import os

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
        item = dict()
        for i, column in enumerate(columnList):
            item[column] = itemData[i]
        data.append(item)
        row = file.readline()
    
    file.close()
    
    return data

# 5. deleteRow -->  #deleting specified rows
def deleteRow(source, rowList):
#    confirm = input("Confirm deleting "+str(len(rowList))+" rows: [Y]/[N]")
    if len(rowList) <= 0:
        return True
    confirm = 'y'
    if not (confirm == 'y' or confirm == 'Y'):
        return False
    try:
        file = open(source)
        outFile = open(source.replace(".csv","T.csv"), "w")

        data = file.readlines()
        for i, row in enumerate(data):
            if i in rowList:    
                print("remove ["+str(i)+"] row")
            else:
                outFile.write(row)
        outFile.close()
        file.close()
        
        checkAsTrain(source)
        return False
    except FileNotFoundError:
        log("File does not exists", "e")
        return False
    
def checkAsTrain(source):
    #ONLY DEBUG FUNCTION
    os.remove(s.trainFile)
    os.remove(s.checkFile)
    
    os.rename(source.replace(".csv","T.csv"), s.trainFile)
    source = open(s.trainFile)
    check = open(s.checkFile, "a")
    check.writelines(source.readlines())
    check.close()
    source.close()
    

def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()

def BP():
    input('[ DEBUG ] Waiting for key...') # Debbuger Break Point HERE

