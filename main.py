import math

import helper as h
import settings as s

class leaf():
    def __init__(self, response):
        self.response = response
        
class node():
    def __init__(self, S, column, value):
        self.S = S
        self.column = column
        self.value = value
        self.end = self.getNodeEnd()
        
    def getDecisionFromRow(self, row):
        return row[list(row)[-1]]
        
    
    def getNodeEnd(self):
        #check amount of decision for specified key
        firstDecision = None
        for row in self.S:
            if row[self.column] == self.value and firstDecision == None:
                firstDecision = self.getDecisionFromRow(row)
                continue
            
            if firstDecision != self.getDecisionFromRow(row) and row[self.column] == self.value:
                h.log("End of node will be: root")
                return root(self.trimSetByColumn(self.S, self.column, self.value))
                
        h.log("End of node will be: leaf")
        return leaf(self.value)
                
    def trimSetByColumn(self, S, column, keyValue):
        output = []
        for row in S:
            singleRow = dict()
            add = True 
            for key, value in row.items():
                
                if key != column:
                    singleRow[key] = value
               
                if column == key and keyValue != value:
                    add = False
                    
                    
            if bool(singleRow) == True and add == True:     
                output.append(singleRow)
            
        return output

class root():
    
    def __init__(self, S):
        #ROOT LIFECYCLE
        self.node = []
        self.S = S
        self.column = self.getColumn()
        self.bestGain = 0
        
        self.selectColumn()
        
        h.log("Another root ["+self.column+"]")
        
        self.addNodes()
        
        #print(self.node)
    
    #HELPER FUNCTIONS
    def getColumn(self):
        return list(self.S[0].keys())[:-1]
    
    def computeEntropy(self, S):
        h.log("Compute entropy...")
        entropy = dict()
        
        for row in S:
            decision = list(row)[-1]   
            
            if row[decision] in entropy.keys():
                entropy[row[decision]] += 1
            else:
                entropy[row[decision]] = 1
        
        omega = len(S)
        
        output = 0
        
        for item in entropy:
            h.log2(str(entropy[item] / omega))
            output -= (entropy[item] / omega) * math.log((entropy[item] / omega), 2)
            
        h.log2("Entropy is: " + str(output))
        return output
    
    def computeGain(self, S, totalEnt):
        h.log("Computing gain for nodes...")
        output = dict()
        column = self.getColumn()
        
        omega = len(S)
        
        for col in column:
            
            valList = self.getValList(S, col)
            ent = 0
            for value in valList:
                ents = dict()
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
        
        #print(output)
        
        return output
    
    def getBestColumn(self, gainList):
        best = max(gainList.values())
        for key, value in gainList.items():
            if value == best:
                h.log("The best gain is: " + key + "[" + str(value) + "]")
                return key
            
    def countDecisionWhereKeyEqual(self, S, key, value, decision):
        output = 0
        for row in S:
            if row[key] == value and row[list(row)[-1]] == decision:
                output += 1
                
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
    
    def getValList(self, S, key):
        output = dict()
        for row in S:
            if row[key] in output.keys():
                output[row[key]] += 1
            else:
                output[row[key]] = 1
            
        return output
    
        
    #ROOT ACTIONS
    def selectColumn(self):
        self.entropy = self.computeEntropy(self.S)           #   Ent(S)
        gainList = self.computeGain(self.S, self.entropy)    #   Ent(S|a)
        self.column = self.getBestColumn(gainList)           #   The Best Gain(S|a)
        
    def addNodes(self):
         
        # for    specific   value   in     set of possibles
        for value in list(self.getValList(self.S, self.column).keys()):
            h.log("Append node (S,"+self.column+", "+value +")")
                        
            self.node.append(node(self.S, self.column, value))    
             
            
def main():
    
    
    data = h.getDataFromFile(s.trainFile)
    tree = root(data)
    
    
    
    
main()