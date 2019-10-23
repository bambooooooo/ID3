import helper as h

class tree():
    
    def __init__(self):
        h.log("initializing tree...")           
        
        self.root = None                         #int default varibles
        self.trainDataSource = s.trainFile       #file with trainData
        self.data = []                           #data collection
        self.column = []                         #list of column
        
    def setData(self):
        h.log("fetching data from file")
        if self.loadData(self.trainDataSource) == False:
            return False
        
        
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
    
    def getColumns(self):
        return self.column
        
            
def main():
    t = tree()
    if t.setData() == False:
        return False
    print(t.getColumns())
    
    
    
    
    
    
    
    
    
    
main()