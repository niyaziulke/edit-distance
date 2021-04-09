from sys import argv

# dictionary for mapping some integers to operation names
operation_dict = {
        0 : 'Insert' ,
        1 : 'Delete' ,
        2 : ('Replace','Copy') ,
        3 : 'Transpose'
    }

# the words to calculate edit distance
w1 = argv[1].lower()
w2 = argv[2].lower()

# store table sizes
(rows,cols) = (len(w1) +1,  len(w2)+1)

arrow = " -> "

# initializes the first row and column of the distance table
def distInit(i,j):
    if(i==0 and j==0):
        return 0
    elif(i==0):
        return j
    elif(j==0):
        return i
    else:
        return -1

# initializes the first row and column of the operation table
def opInit(i,j):
    if(i==0 and j==0):
        return 'x'
    elif(i==0):
        return 'Delete'
    elif(j==0):
        return 'Insert'
    else:
        return -1
    
# prints distance table with format, also prints letters of words.
def printArray(arr):
    print("{:8}".format(''),end='')
    
    # print w2 like the first row
    for index in range(cols-1):
        print("{:4}".format(w2[index]), end ='')
    
    print()
    for i in range(rows):
        if i == 0:
            print(' ',end='')
            
        for j in range (cols):
            # print w1 like the first column
            if i!=0 and j==0:
                print(w1[i-1],end='')
            print("{:4}".format(arr[i][j]), end = '')
        print()
    print()    
# reads operations from operation table starting from lower right corner until upper left corner,
# reverses the order of operations and passes them to printOperations function
def readPrintOperations(oparr):
    i = rows - 1
    j = cols - 1
    
    operationList = []
    while(i>0 or j>0):
        
        operationList.append(oparr[i][j])
        if(oparr[i][j]=='Insert'):
            j -= 1
                 
        elif(oparr[i][j] == 'Delete'):
            i -= 1
            
        elif(oparr[i][j]==('Replace','Copy')):
            i -= 1
            j -= 1
            
        elif(oparr[i][j] == 'Transpose'):
            i -= 2
            j -= 2
    printOperations(operationList[::-1])
    
# prints operations in order by examining operationList, also detects and prints intermediate states of the word.
def printOperations(operationList): 
    # trStr is for information about operations
    trStr = ''
    word = w1
    # flowStr is for printing intermediate steps
    flowStr = word
    i = 0
    j = 0
    for operation in operationList:
          
        if(operation == 'Insert'):
            trStr += 'Insert\t' + w2[j] + '\n' 
            
            word = word[:i]+ w2[j] + word[i:]
            j += 1
            i += 1
            flowStr +=  arrow + word 
            
        elif(operation == 'Delete'):
            trStr += 'Delete\t' + word[i] + '\n' 
            
            word = word[:i]+ word[i+1:]
            flowStr += arrow + word   
        
        elif(operation == ('Replace','Copy')):
            # distinguish between replace and copy operations
            
            if(word[i]!=w2[j]):
                trStr +='Replace {} with {}\n'.format( word[i], w2[j]) 
                word = word[:i] + w2[j] + word[i+1:]
                flowStr += arrow + word 
            else:
                trStr += 'Copy\t' + w2[j]+ '\n'
            i += 1
            j += 1
                
        else:
            trStr +='Transpose {} with {}\n'.format( word[i], word[i+1]) 
            
            word = word[:i] + word[i+1] + word[i] + word[i+2:]
            i += 2
            j += 2
            flowStr += arrow + word 
    print("Operations are:\n"+ trStr)
    print("Changes: "+flowStr)

        
    
# calculates Levenshtein distance with dynamic programming approach
def levDist():
    # distance table
    distarr = [[distInit(i,j) for i in range(cols)] for j in range(rows)]
   
    # operation table
    oparr = [[opInit(i,j) for i in range(cols)] for j in range(rows)]
    
    for i in range(1,rows):
        for j in range(1,cols):
            # list for comparing distances provided by different operations
            compList = [    distarr[i][j-1]+1 ,                             
                            distarr[i-1][j]+1 ,
                            distarr[i-1][j-1] + (w1[i-1] != w2[j-1])
                        ]
            
            distarr[i][j] = min(compList)
            # use operations dictionary to detect which operation has provided min. distance, store the operation in the table
            oparr[i][j] = operation_dict[compList.index(distarr[i][j])]
            
           
            
    print('Levenshtein distance of the words:', distarr[rows-1][cols-1])
    print('Edit table for Levenshtein distance:')
    printArray(distarr)
    readPrintOperations(oparr)
    
    print('o------------------------------------o')
    

# calculates Damerau-Levenshtein distance and 
def damLevDist():
    # distance table
    distarr = [[distInit(i,j) for i in range(cols)] for j in range(rows)]
   
    # operation table
    oparr = [[opInit(i,j) for i in range(cols)] for j in range(rows)]
    
    for i in range(1,rows):
        for j in range(1,cols):
            # list for comparing distances provided by different operations
            compList = [    distarr[i][j-1]+1 ,                             
                            distarr[i-1][j]+1 ,
                            distarr[i-1][j-1] + (w1[i-1] != w2[j-1])
                        ]
            # check if transposition could be beneficial
            if(i>=2 and j>=2 and w1[i-1] == w2[j-2] and w1[i-2] == w2[j-1]):
                compList.append(distarr[i-2][j-2]+1)               
            
            distarr[i][j] = min(compList)
            # use operations dictionary to detect which operation has provided min. distance, store the operation in the table
            oparr[i][j] = operation_dict[compList.index(distarr[i][j])] 
            
           
            
    
    print('Damerau-Levenshtein distance of the words:',distarr[rows-1][cols-1])
    print('Edit table for Damerau-Levenshtein distance:')
    printArray(distarr)
    readPrintOperations(oparr)

# call distance calculation methods
levDist()
damLevDist()


