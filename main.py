import math
import pydotplus as ptp
import time


import helper as h
import settings as s

from PIL import Image

 
class treeDrawer(): # accumulator for all nodes and egdes
    
    def __init__(self):
        self.edges = []
        self.nodes = []
        self.counter = 0
        
    def addNode(self, index, label):
        self.nodes.append((index, label))
        
    def addEdge(self, fromIndex, toIndex, label):
        self.edges.append((fromIndex, toIndex, label))
        
    def addIndex(self):
        self.counter += 1
        return self.counter
    
    def getLast(self):
        return self.counter
    
tc = treeDrawer()
    

class leaf(): # LEAF - specific decision
    
    def __init__(self, response):
        
        self.response = response                    # eq - decision value
        tc.addNode(tc.addIndex(), self.response)    # add edge to accumulator
        self.itemIndex = tc.getLast()               # set Index to instance
        
    def getItemIndex(self):
        return self.itemIndex                       # [!] must match with root.getItemIndex()
    
    def getDecision(self):
        return self.response
        
class node():
    def __init__(self, S, column, value, fromIndex): # Edge instance
        self.S = S
        self.column = column
        self.value = value
        self.end = self.addNodeEnd()                 # Check if it going to be [LEAF] or another [ROOT]
        self.fromIndex = fromIndex                   # Index of root that is parent to node - to edge in diagram
        self.endIndex = self.getNodeEndIndex()       # Index of [ROOT] or [LEAF] that ends node instance
        
        tc.addEdge(self.fromIndex, self.endIndex, self.value)   # add node to accumulator
        
    def getDecisionFromRow(self, row):
        return row[list(row)[-1]]                    # Get last value from dictionary
        #for example {'firstName': 'Will', 'lastName': 'Smith', 'decsion': 'boy'} ===> 'boy'
    
    def getNodeEnd(self):
        return self.end
    
    def getNodeValue(self):
        return self.value
    
    def addNodeEnd(self):
        #check amount of decision for specified value of key
        firstDecision = None
        for row in self.S:
            if row[self.column] == self.value and firstDecision == None:
                firstDecision = self.getDecisionFromRow(row)
                continue
            
            if firstDecision != self.getDecisionFromRow(row) and row[self.column] == self.value:
                h.log("End of node will be: root") #for specified value for some column we have different decision
                                                   #it will be another root
                return root(self.trimSetByColumn(self.S, self.column, self.value))
        h.log("End of node will be: leaf")
        return leaf(firstDecision)                 # decisions for value are the same so we are sure we got an answear
    
    def getNodeEndIndex(self):
        return self.end.getItemIndex()
        
                
    def trimSetByColumn(self, S, column, keyValue):
        # removing every row where value of column not match with given
        # removing given colum also
        # [TODO]: use map / filter / recude instead of building output like now
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
    
    def __init__(self, S):  # RRRRROOT instance
        
        #ROOT LIFECYCLE
        self.node = []
        self.S = S
        self.column = self.getColumn()
        self.bestGain = 0
        
        self.selectColumn() # Set of functions that calculate Entropy
                            #                                 Conditional Entropy
                            #                                 Gain
                            #          for select column with the best gain that will represents root instance
        
        h.log("Another root ["+self.column+"]")

        tc.addNode(tc.addIndex(), self.column)  # add node to accumulator
        
        self.itemIndex = tc.getLast()
        self.addNodes()                         # add list with every kind of value for selected column
        
    
    #HELPER FUNCTIONS
    def getNodeByValue(self, value):
        for item in self.node:
            if item.getNodeValue() == value:
                return item
    
    def getItemIndex(self):
        return self.itemIndex
    
    def getColumn(self):
        return list(self.S[0].keys())[:-1]  #get list of column without, of course, decision which is the last item
    
    def computeEntropy(self, S):
        h.log("Compute entropy...")     # Computing entropy for root instance
                                        # Ent(S)
        entropy = dict()
        
        # [TODO]: move to helper class
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
        h.log("Computing gain for nodes...") # prepare set of gains to select best of them later
                                             # Gain = Ent(S) - Ent(S|a)
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
        # return column name with the best gain
        # [TODO]: make it better cos it sucks
        best = max(gainList.values())
        for key, value in gainList.items():
            if value == best:
                h.log("The best gain is: " + key + "[" + str(value) + "]")
                return key
            
    def countDecisionWhereKeyEqual(self, S, key, value, decision):
        #something like SQL: SELECT COUNT(decision) WHERE column = value AND decision = given decision
        output = 0
        for row in S:
            if row[key] == value and row[list(row)[-1]] == decision:
                output += 1
                
        return output
            
    def getAvailableDecision(self, S):
        #return list of available decision, for example ['YES', 'NO']
        output = []
        for row in S:
            if row[list(row)[-1]] in output:
                pass
            else:
                output.append(row[list(row)[-1]])

        return output
    
    def getValList(self, S, key):
        # count occurs the same value of key in given S
        output = dict()
        for row in S:
            if row[key] in output.keys():
                output[row[key]] += 1
            else:
                output[row[key]] = 1
            
        return output
    
    def trimRowByColumn(self, row, column):
        # removing given colum 
        # [TODO]: use map / filter / recude instead of building output like now
        singleRow = dict()

        for key, value in row.items():
            if key != column:
                singleRow[key] = value
           
        return singleRow
            
    
        
    #ROOT ACTIONS
    def selectColumn(self):
        self.entropy = self.computeEntropy(self.S)           #   Ent(S)
        gainList = self.computeGain(self.S, self.entropy)    #   Ent(S|a)
        self.column = self.getBestColumn(gainList)           #   The Best Gain(S|a) - column / representant
        
    def addNodes(self):
        # for    each value that can occur for root's column
        
        for value in list(self.getValList(self.S, self.column).keys()):
            h.log("Append node (S,"+self.column+", "+value +")")
            self.node.append(node(self.S, self.column, value, self.itemIndex))
            # add node, add node, ...
            
    def getDecision(self, requestRow):
        #print("requestRow: ", requestRow)
        if len(requestRow) <= 0:
            h.log("Insufficient or broken request, unknown decision", "e")
            return False
        else:
            h.log2("-"+self.column+"?")
            nextNode = requestRow[self.column]
            h.log2("---"+nextNode)
            nextItem = self.getNodeByValue(nextNode)
            nodeEnd = nextItem.getNodeEnd()
            if nodeEnd.__class__.__name__ == 'root':
                return nodeEnd.getDecision(self.trimRowByColumn(requestRow, self.column))
            elif nodeEnd.__class__.__name__ == 'leaf':
                h.log2("[Decision]: " + nodeEnd.getDecision())
                return nodeEnd.getDecision()
            else:
                h.log("Something is not yes here", "e")
             
            
def main():
    
    trainData = h.getDataFromFile(s.trainFile)   # open data file
    if not trainData:
        return False                        # data open error - exit
    
    tree = root(trainData)                       # power on carousel - load data from training source
    
    
    #printing diagram
    #[TODO] - pack it into treeDrawer.draw()
    if s.drawTree:
        graph = ptp.Dot(graph_type='graph')
        color = 'white'
        
        for e in tc.edges:
            h.log("Add node from " + str(e[0]) + " to " + str(e[1]))
            edge = ptp.Edge(src=e[0], dst=e[1], label=e[2])
            graph.add_edge(edge)
        for n in tc.nodes:
            node = ptp.Node(name=n[0], label= n[1], fillcolor="white", style="filled", shape="box" )
            graph.add_node(node)
        
        graph.write_png("tree.png")
        
        img = Image.open("tree.png")
        img.show()
        
    # check tree's accuary    
    h.log("Checking tree with check dataset...")
    checkData = h.getDataFromFile(s.checkFile)
    correctAmount = 0
    
    l = len(checkData)
    printProgressBar(0, l, prefix = 'Checking:', suffix = 'Complete', length = 50)
    
    invalidRows = []
    
    for i, row in enumerate(checkData):
        decision = row[list(row)[-1]]
        
        singleRow = dict()

        for key, value in row.items():
            if key != list(row)[-1]:
                singleRow[key] = value
           
        
        correctDecision = tree.getDecision(singleRow)
        #print(decision, " vs ", correctDecision)
        if decision == correctDecision:    
            #h.log("["+str(i)+"] Decision correct")
            correctAmount += 1
        else:
            invalidRows.append(i)
            #h.log("["+str(i)+"] Decision incorrect ")
        
        time.sleep(0.2)
        printProgressBar(i + 1, l, prefix = 'Checking:', suffix = 'Complete', length = 50)
            
    accuary = correctAmount / len(checkData)
    h.log("Tree accuary is: " + str(correctAmount) + "/" + str(len(checkData))  + " ("+ str(accuary*100) + "%)")
    
main()