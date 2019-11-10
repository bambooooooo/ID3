debugMode = False                           
deepDebug = False                           
drawTree = False    
drawTreeBeforePruning = False                        
#checkTree = False 
prunning = False                          

debugMode = True                           # set to false in production
#deepDebug = True                           # print h.log2() as well
drawTree = True                            # draw flag
drawTreeBeforePruning = True               # draw tree before pruning aswell
checkTree = True                           # check tree with checkset
prunning = True

# Select directory froum resources 

#folder = 'db2'
#folder = 'db'
#folder = 'alco'
#folder = 'pub'
#folder = 'pubPruning'
#folder = 'pubTrimed'
#folder = 'demo'
#folder = 'cardio'
folder = 'heart'

trainFile = './resources/'+folder+'/trainSet.csv'  # path to train dataset
checkFile = './resources/'+folder+'/checkSet.csv'  # path to check dataset

