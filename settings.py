debugMode = True                        #set to false in production
deepDebug = False                        #print h.log2() as well
trainFile = './resources/trainSet.csv'  #path to train dataset


'''

TODODOODODODO

decision is represented by the last column now. It should be changed to lastest set of column with prefix _
f.ex.
dochod | plec | pracuje | kredyt
                      decision now
                            
dochod | plec | pracuje | _kredyt | _kredyt_wielkosc
                            set of decisions
                            
                            
'''