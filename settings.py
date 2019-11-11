debugMode = False                           
deepDebug = False                           
drawTree = False    
drawTreeBeforePruning = False                        
checkTree = False 
prunning = False                          
shuffleSet = False

debugMode = True                            # print debug logs  -->  helper.log()
#deepDebug = True                           # print deeper logs -->  helper.log2() if debugMode is ON
drawTree = True                            # draw computed tree
drawTreeBeforePruning = True                # draw tree before pruning
checkTree = True                            # check tree with checkset
prunning = True                             # ON/OFF pruning
shuffleSet = True                           # Shuffle dataset before split into trainset and checkset

# Select set froum resources 

#folder = 'db2'
#folder = 'db'
#folder = 'alco'
folder = 'pub'
#folder = 'pubPruning'
#folder = 'pubTrimed'
#folder = 'demo'
#folder = 'cardio'
#folder = 'heart'

trainFile = './resources/'+folder+'/trainSet.csv'  # path to train dataset

trainSetPercentage = 80 #part of dataset that will be trinSet, rest of will be checkSet

