#####       FILE MANAGEMENT HEADER    ######

def getFile():
    import sys
    fileFromTerm = ''
    for arg in sys.argv[1:]:
        fileFromTerm = arg
    if len(fileFromTerm) == 0:
        print 'No file inputed'
        return None
    else:
        print '\n \nOpened file: ' + fileFromTerm
        return fileFromTerm
        
def getFileName():
    import sys
    fileFromTerm = ''
    fileFromTermProc=''
    for arg in sys.argv[1:]:
        fileFromTerm = arg
    if len(fileFromTerm) == 0:
        print 'No file inputed'
        return None
    else:
        fileFromTermProc=fileFromTerm.split('.')
        return fileFromTermProc[0]
        
def readFile(file):
    if file == None:
        print 'No file to read'
    else:
        print 'Read file: ' + str(file)
        return open(file, "r")

def terminalImport():
    IMPORTED = getFile()
    FILE = readFile(IMPORTED)
    return FILE
    
def everythingParser(inFile):
    everythingList=[]
    for lines in inFile.readlines():
        everythingList.append(lines[:-1])
    
    print '\n'+ "Input file contains " + str(len(everythingList)) + ' lines'
    return everythingList
    
def ccp4ContactValidator(inFile):
    inFileYo=inFile
    for lines in inFileYo:
        if "NCONT" in lines:
            print "Input file was validated as a ccp4 contact output file!"
            return True
    else:
        return False
        
def contactParser(inFile):
    inFileYo=inFile
    contactList=[]
    for lines in inFileYo:
       if "]:" in lines:
           #print lines
           contactList.append(lines)
    print str(len(contactList)) + " contact lines detected"
    return contactList
    
def doesContactsMatch(everythingList, contactList):
    everythingListYo=everythingList
    contactListYo=contactList
    totalContactLine=''
    reference=0
    analyte=len(contactListYo)
    for lines in everythingListYo:
        if "Total" in lines and "contacts" in lines:
            totalContactLine += lines
    for s in totalContactLine.split(): 
        if s.isdigit():
            reference+=int(s)   
    if analyte == reference:
        print "projectContact recognised the same number of contacts as reported by CCP4!"
        return True
    else:
        print "projectContacts did not find all the contacts in the contact file!"
        return False
        
#####           MATHS           #######

## Line Filler ##

test=' /1/A/  65(ARG). / CG [ C]:  /1/E/  57(SER). / CB [ C]:   3.98'

def lineNeedsFilled(line):
    if line.count(":") == 1:
        return True
    else:
        return False
        
def sourceAtomsGrabber(line):
    splitLine = ''
    splitLine=line.split(':')
    return str(splitLine[0]+':')
    
def lineFiller(contactLines):
    print '\nFilling source atom lines...'
    newLines=[]
    positionCounter=0
    fillCounter=0
    for lines in contactLines:
        positionCounter+=1
        if lineNeedsFilled(lines) == False:
            newLines.append(lines)
    
        elif lineNeedsFilled(lines) == True:
            fillCounter+=1
            trackBackCounter=2
            newLine=''
            suffix=''
            prefix=''
            while str(sourceAtomsGrabber(contactLines[positionCounter-trackBackCounter])).count(' ') > 20:
                trackBackCounter+=1
            prefix=sourceAtomsGrabber(contactLines[positionCounter-trackBackCounter])
            suffix=lines[28:]
            newLine = prefix + ' ' + suffix
            newLines.append(newLine)
    print str(fillCounter) + " lines were filled with source atoms..."
    return newLines  
    
def contactMatrixRow(line):
    contactRow=[]
    contactRow.append(line[4])
    contactRow.append(int(line[6:10]))
    contactRow.append(line[11:14])
    contactRow.append(line[19:22])
    contactRow.append(line[24])
    contactRow.append(line[32])
    contactRow.append(int(line[34:38]))
    contactRow.append(line[39:42])
    contactRow.append(line[47:50])
    contactRow.append(line[52])
    contactRow.append(float(line[-4:]))
    return contactRow

    
def contactMatrix(contactLines):
    omitCounter = 0
    print '\nCreating contact matrix...'
    contactMatrix=[]
    for lines in contactLines:
        if 'HOH' in lines:
            omitCounter +=1 
        else:
            contactMatrix.append(contactMatrixRow(lines))
    print str(omitCounter) + ' contacts were omitted due to water "HOH"...' 
    return sorted(contactMatrix, key=lambda items: (items[0], items[1]))
                
def isHBond(contactRow):
    if contactRow[4]=='N' and contactRow[9]=='O' and 3.4 <= contactRow[10] <= 4.0:
        #print(contactRow)
        #print 'H-bond hit 1'
        return True
    if contactRow[4]=='O' and contactRow[9]=='N' and 3.4 <= contactRow[10] <= 4.0:
        #print(contactRow)
        #print 'H-bond hit 2'
        return True
    if contactRow[4]=='N' and contactRow[9]=='N' and 3.4 <= contactRow[10] <= 4.0:
        #print(contactRow)
        #print 'H-bond hit 3'
        return True
    if contactRow[4]=='O' and contactRow[9]=='O' and 3.4 <= contactRow[10] <= 4.0:
        #print(contactRow)
        #print 'H-bond hit 4'
        return True       

def isSaltBridge(contactRow):
    #positive first#
    if contactRow[2] == 'LYS' and contactRow[3] == 'NZ':
        if contactRow[7] == 'GLU' and contactRow[8] in ['OE1','OE2']:
            if contactRow[10] <= 3.4:
                return True
        elif contactRow[7] == 'ASP' and contactRow[8] in ['OD1','OD2']:
            if contactRow[10] <= 3.4:
                return True
    elif contactRow[2] == 'ARG' and contactRow[3] in ['NE','NH1','NH2']:
        if contactRow[7] == 'GLU' and contactRow[8] in ['OE1','OE2']:
            if contactRow[10] <= 3.4:
                return True
        elif contactRow[7] == 'ASP' and contactRow[8] in ['OD1','OD2']:
            if contactRow[10] <= 3.4:
                return True
    #elif contactRow[2] == 'HIS' and contactRow[8] in ['NE1','NE2','CE1']:
       # if contactRow[7] == 'GLU' and contactRow[8] in ['OE1','OE2']:
            #if contactRow[10] <= 4.0:
             #   return True
      #  elif contactRow[7] == 'ASP' and contactRow[8] in ['OD1','OD2']:
           # if contactRow[10] <= 4.0:
                #return True
    #negatives first#
    elif contactRow[2] == 'ASP' and contactRow[3] in ['OD1','OD2']:
        if contactRow[7] == 'ARG' and contactRow[8] in ['NE','NH1','NH2']:
                if contactRow[10] <= 3.4:
                    return True
        #if contactRow[7] == 'HIS' and contactRow[8] in ['NE1','NE2','CE1']:
         #       if contactRow[10] <= 4.0:
            #        return True
       # if contactRow[7] == 'LYS' and contactRow[8] == 'NZ':     
            #    if contactRow[10] <= 4.0:
                  #  return True        
    elif contactRow[2] == 'GLU' and contactRow[3] in ['OE1','OE2']:
        if contactRow[7] == 'ARG' and contactRow[8] in ['NE','NH1','NH2']:
                if contactRow[10] <= 3.4:
                    return True
       # if contactRow[7] == 'HIS' and contactRow[8] in ['NE1','NE2','CE1']:
               # if contactRow[10] <= 4.0:
                #    return True
        if contactRow[7] == 'LYS' and contactRow[8] == 'NZ':     
                if contactRow[10] <= 3.4:
                    return True 
    else:                       
        return False       
    
def isVdW(contactRow):
    if contactRow[2] == contactRow[7]:
        if contactRow[3] == contactRow[8]:
            if contactRow[4] == contactRow[8]:
                return False
    if contactRow[10] <= 4.0:
        return True
        
def bondAnnotator(contactsRow):
    contactsRow.append('NO') 

    if isVdW(contactsRow)==True:
        contactsRow[11] ='VW'
    if isHBond(contactsRow)==True:
        contactsRow[11] ='HB'
    if isSaltBridge(contactsRow)==True:
        contactsRow[11] ='SB'
        
def annotateAllWrapper(contactMatrix):
    print 'Anotating contacts...'
    for row in contactMatrix:
        bondAnnotator(row)
    
    
    
#####        STATISTICS        #######

def totalHB(contactMatrix):
    totalHB = 0
    
    for contactRow in contactMatrix:
        if contactRow[11] =='HB':
            totalHB += 1
    return totalHB
    
def totalSB(contactMatrix):
    totalSB = 0
    
    for contactRow in contactMatrix:
        if contactRow[11] =='SB':
            totalSB += 1
    return totalSB
    
def totalVW(contactMatrix):
    totalVW = 0
    
    for contactRow in contactMatrix:
        if contactRow[11] =='VW':
            totalVW += 1
    return totalVW
    
#####       Questions        #######

def whatChains(contactMatrix):
    chains=[]
    
    for contactRow in contactMatrix:
        if contactRow[0] not in chains:
            chains.append(contactRow[0])
        if contactRow[5] not in chains:
            chains.append(contactRow[5])            
    return sorted(chains)

def defineChains():
    TCRa=raw_input('Which chain is TCRa: ')
    TCRb=raw_input('Which chain is TCRb: ')
    MHCa=raw_input('Which chain is MHCa: ')
    MHCb=raw_input('Which chain is MHCb:')
    pep=raw_input('Which chain is the peptide: ')
    
    return [TCRa,TCRb,MHCa,MHCb,pep]

        
#####       INITIALISER        #######
# Openers #
print('\n''     ~  Running projectContacts.py v0.1  ~')
inFile = terminalImport()
inFileName = getFileName()
if type(inFileName) != str:
    raise IOError('No file was loaded. Please view usage and provide a valid file to be processed')
allLines=everythingParser(inFile)
contactLines=contactParser(allLines)

# Validation #
if ccp4ContactValidator(allLines)==False:
    raise IOError("Input file was NOT validated as a ccp4 contact output file! /n Please see usage for information")
if doesContactsMatch(allLines, contactLines) == False:
    raise IOError("projectContacts did not find all the contacts in the contact file!")
    
# All checks good.. create outputs etc #
    

outFile = open(str(inFileName) + '_out.txt' , 'w')
output=''


#####           BODY           #######
contactMatrixS=[]
contactLines=lineFiller(contactLines)
contactMatrix=contactMatrix(contactLines)
annotateAllWrapper(contactMatrix)
print whatChains(contactMatrix)
print defineChains()






for x in contactMatrix:
    print x
    
print '\n Building statistics...\n'
print str(len(contactMatrix)) + ' contacts in the matrix\n'
print str(totalSB(contactMatrix)) + ' salt bridge contacts in the matrix\n'
print str(totalHB(contactMatrix)) + ' hydrogen bond contacts in the matrix\n'
print str(totalVW(contactMatrix)) + ' van der Waals contacts in the matrix\n'
    
#####   OUTPUT GENERATOR       #######   
            
outFile = open(str(inFileName) + '_out.txt' , 'w')
output1=''
output2=''
output1 += 'Parameter \tNumber \n' \
'Total contacts (=<4.0A) \t' + str(len(contactMatrix)) + '\n' \
'Salt Bridges =< 4.0\t' + str(totalSB(contactMatrix)) + '\n' \
'H-bonds (=< 3.4A)\t' + str(totalHB(contactMatrix)) + '\n'\
'vdW (=< 4.0A) \t' + str(totalVW(contactMatrix)) + '\n'

print output1
output2+= 'Chain \tResNum \tResCode \tPosition \tAtom \tChain \tResNum \tResCode \tPosition \tAtom \tDistance \tType\n'
for x in contactMatrix:
    for y  in x:
        output2+=str(y) + '\t'
    output2+='\n'

outFile.write(output2)
print '\nOutputted file: ' + str(inFileName)+ '_out.txt'
print('\n''     ~  End ProjectContacts.py v0.1      ~')
