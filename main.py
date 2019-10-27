import math

import helper as h
import settings as s

class tree():
    
    #constructors
    def __init__(self):
        h.log("initializing tree...")           
        
        self.root = None                         #int default varibles
        self.trainDataSource = s.trainFile       #file with trainData
        self.data = []                           #data collection
        self.column = []                         #list of column
    
    #initializing
    def loadData(self, source):
        h.log("fetching train data from " + str(source) + " file...")
        try:
            self.column = h.getColumnFromFile(source)
            self.data = h.getDataFromFile(source, self.column)
        except FileNotFoundError:
            h.log("Train data file not found", "e")
            return False
        
        h.log("Data loaded successfully")
        h.log("Loaded columns: " + str(len(self.column)))
        #h.log(self.column, "other")
        h.log("Loaded data: " + str(len(self.data)) + " rows")
        #h.log(self.data, "other")
        return True
    
    #setters
    def setData(self):
        h.log("fetching data from file")
        if self.loadData(self.trainDataSource) == False:
            return False
        
        
    #getters
    def getColumns(self):
        #todo: change call for this funtion to call getColumn() above
        return self.column
    
    def getData(self):
        return self.data
    
    def getColumn(self, S):
        return list(S[0].keys())
    
    def getValList(self, S, key):
        output = dict()
        for row in S:
            if row[key] in output.keys():
                output[row[key]] += 1
            else:
                output[row[key]] = 1
            
        return output
    
    def getAvailableDecision(self, S):
        #todo - get it after object's init cos he will not change itself
        output = []
        for row in S:
            if row[list(row)[-1]] in output:
                pass
            else:
                output.append(row[list(row)[-1]])
                
        return output
    
    def countDecisionWhereKeyEqual(self, S, key, value, decision):
        output = 0
        for row in S:
            if row[key] == value and row[list(row)[-1]] == decision:
                output += 1
                
        return output
    
    #compute
    def computeEntropy(self, S):
        h.log("Compute entropy for root")
        entropy = dict()
        #count 
        for row in S:
            decision = list(row)[-1]   
            
            if row[decision] in entropy.keys():
                entropy[row[decision]] += 1
            else:
                entropy[row[decision]] = 1
        
        omega = len(S)
        
        output = 0
        
        for item in entropy:
            #print(item, entropy[item])
            h.log2(str(entropy[item] / omega))
            output -= (entropy[item] / omega) * math.log((entropy[item] / omega), 2)
            
        h.log("Entropy for root: " + str(output))
        return output
    
    def computeGain(self, S, totalEnt):
        h.log("Compute conditional entropy...")
        output = dict()
        column = list(self.getColumn(S)[:-1])
        
        omega = len(S)
        
        for col in column:
            
            valList = self.getValList(S, col)
            ent = 0
            for value in valList:
                ents = dict()
                #h.log2("value: " + value)
                for decision in self.getAvailableDecision(S):    
                    ents[decision] = (self.countDecisionWhereKeyEqual(S, col, value, decision))
                    
                
                sumOfDecision = sum(ents.values())
                p = sumOfDecision / omega
                
                
                for decision in ents:
                    pi = ents[decision] / sumOfDecision
                    try:
                        ent -= p * pi * math.log2(pi)
                    except ValueError:
                        h.log2("log2(0)", "w")
                        pass
                

            output[col] = totalEnt - ent  
            h.log2("Condtional entropy(S, "+str(col)+"): " + str(totalEnt-ent))
                
            #print(value, ': ', sumOfDecision, '/', omega, ' = ', p)
            #print(valList)
        return output
        
    def getBestColumn(self, gainList):
        best = max(gainList.values())
        for key, value in gainList.items():
            if value == best:
                h.log2("The best gain is: " + key + "[" + str(value) + "]")
                return key
      
    def printData(self, data):
        for row in data:
            print(row)
             
            
def main():

    #initializing and validating data
    t = tree()
    if t.setData() == False:
        return False
    
    #compute entropy for root
    entRoot = t.computeEntropy(t.getData())
    
    #compute conditional entropy for root
    gainRoot = t.computeGain(t.getData(), entRoot)
    
    #print(gainRoot)
    
    print(t.getBestColumn(gainRoot))
    #t.printData(t.getData())
    
    
    
    #print(t.getAvailableDecision(t.getData()))
    
    
    
    
    
main()