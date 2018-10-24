"""
preprocess.py
Scope: Preprocessing script to identify NUM and DATE objects.
Authors: Bill Cramer
"""

import re
import os
import fnmatch
import bs4 as bs
import pandas as pd
from os import listdir
from os.path import isfile
import shlex, subprocess
import time
from subprocess import *
import sys, getopt
import shutil


inFolder = ""
outFolder = ""

opts, args = getopt.getopt(sys.argv[1:], 'i:o:')
for opt, arg, in opts:
     if opt in ('-i'):
         inFolder = arg
     elif opt in ('-o'):
         outFolder = arg

if inFolder == "" or outFolder == "":
     print("Please specify input and output using -i and -o.")
     sys.exit(-1)



originalTextDocsPath = [inFolder]

#### users provides input for where they want their data to land
#print('Please Enter The Path Where You Want Your Data To Be Output')
pathForInputFoldersForChronos = outFolder

#### users provides input for the location of Chronos 
#print('Please Provide the Path for the Chronos Tool')
chronosLocation = './Chrono-master/Chrono.py'


#### this line is needed to make the code below work 
pathForOutputFoldersForChronos = pathForInputFoldersForChronos

#### this returns a path listing for the original txt documents being used. All docs must be in one folder with no sub folders
originalTextDocsList = []

for originalTextDocsLocations in originalTextDocsPath:
    for originalTextFile in os.listdir(originalTextDocsLocations):
        if fnmatch.fnmatch(originalTextFile, '*.txt'):
            originalTextDocsList.append(''.join((originalTextDocsLocations+'/', originalTextFile)))

#### list the orignal file names which will include .txt
orginalFileNames = os.listdir(originalTextDocsPath[0])

#### remove the .txt from the list of file names leaving a listing of just the file names and append to a list
cleanedFileNameList = []
for txtFiles in orginalFileNames:
    removeTxt = re.sub(r'.txt','',txtFiles)
    cleanedFileNameList.append(removeTxt)
         
#### create new directories (folders) in our path listed above for pathForOutputFoldersForChronos for the Chronos tools
newDataOutputPath = pathForOutputFoldersForChronos+'/'+'results/my_output/' 
if not os.path.exists(newDataOutputPath):
    os.makedirs(newDataOutputPath)
    
#### create new directories (folders) in our path listed above for pathForInputFoldersForChronos for the Chronos tools
newDataInputPath = pathForInputFoldersForChronos+'/'+'data/my_input' 
if not os.path.exists(newDataInputPath):
    os.makedirs(newDataInputPath)
    
#### create new directory to store the results from using Chronos to clean our input data
chronosCleaned = pathForOutputFoldersForChronos+'/'+'chronosCleaned'
if not os.path.exists(chronosCleaned):
    os.makedirs(chronosCleaned)

#### the block below creates a listing of the input folders feeding into Chronos     
folderPathsForInputFilesToChronos = []    

for newInputFolderNames in cleanedFileNameList:
    newInputFolders = ''.join((newDataInputPath+'/', newInputFolderNames))
    newpathInputForChronos = newInputFolders 
    if not os.path.exists(newpathInputForChronos):
        os.makedirs(newpathInputForChronos)
        folderPathsForInputFilesToChronos.append(newpathInputForChronos)
   
##### copy the original text files to the Chronos folder structure and create .dct files per Chronos requirement
documentCounter=0
for thoseInputFolder in folderPathsForInputFilesToChronos:
    thoseOrginalDocsOpen = open(originalTextDocsList[documentCounter]).read()
    nameTheTextFiles = open(os.path.join(thoseInputFolder+'/',orginalFileNames[documentCounter]),'w')
    nameTheTextFiles.write(thoseOrginalDocsOpen)
    nameTheTextFiles.close()
    nameTheDCTFiles = open(os.path.join(thoseInputFolder+'/',cleanedFileNameList[documentCounter]+'.dct'),'w')
    nameTheDCTFiles.write('09/01/2018')
    nameTheDCTFiles.close()
    documentCounter = documentCounter+1
    


# In[4]:


#### the block below creates a listing of the folders that will be input into Chronos 
my_inputPath = ''.join((pathForInputFoldersForChronos, '/data/my_input/'))

foldersForInput = os.listdir(my_inputPath)

foldersForInput

inputFolderList =[]

for folder in foldersForInput:
     inputFolderList.append(''.join((my_inputPath, folder)))


# In[5]:



#### the block below creates a listing of the files that will be input into Chronos
inputTextFilePathList = []

for filePath in inputFolderList:
    for file in os.listdir(filePath):
        if fnmatch.fnmatch(file, '*.txt'):
            inputTextFilePathList.append(''.join((filePath+'/', file)))


# In[6]:



#### the block below takes the user's input to provide Chronos' requirements, runs Chronos then returns to this program 
myDataInput = newDataInputPath
myDataOutput = newDataOutputPath
chronosPath = chronosLocation
noChronoPY = re.sub(r'Chrono\.py','',chronosLocation)
sampleFilesData = 'sample_files/official_train_MLmatrix_Win5_012618_data.csv'
sampleFilesClass = 'sample_files/official_train_MLmatrix_Win5_012618_class.csv'
joinFilesData = ''.join((noChronoPY, sampleFilesData))
joinFilesClass = ''.join((noChronoPY, sampleFilesClass))
##formatting the way below was needed to input into the subprocess.Popen while the .wait() provides being able to return the this program
#command = "python3 %s -i %s -x "'.txt'" -o %s -m SVM -d %s -c %s" % (chronosPath,myDataInput,myDataOutput,joinFilesData,joinFilesClass)
command = ["python3", chronosPath, "-i", myDataInput, "-x", ".txt", "-o", myDataOutput, "-m", "SVM", "-d", joinFilesData, "-c", joinFilesClass]

p = subprocess.Popen(command).wait()


# In[7]:



#### the following block checks to see if Chronos has completed then returns a listing of the output folders 
my_OutputPath = ''.join((pathForOutputFoldersForChronos, '/results/my_output/'))

foldersForOutput = os.listdir(my_OutputPath)
outputFolderList =[]
while len(foldersForOutput) == 0:
    foldersForOutput = os.listdir(my_OutputPath)
    print('processing')
    time.sleep(2)
    for outputFolder in foldersForOutput:
        outputFolderList.append(''.join((my_OutputPath, outputFolder)))
            
for outputFolder in foldersForOutput:
    outputFolderList.append(''.join((my_OutputPath, outputFolder)))

            


# In[8]:



#### the block below creates a listing of the completed files
outputXMLFilePathList = []

for outputXMLFilePath in outputFolderList:
    for outputXMLFile in os.listdir(outputXMLFilePath):
        if fnmatch.fnmatch(outputXMLFile, '*.xml') or fnmatch.fnmatch(outputXMLFile, '*.XML'):
            outputXMLFilePathList.append(''.join((outputXMLFilePath+'/', outputXMLFile)))


# In[10]:


#### the block below uses the XML files to clean the txt files 
counter = 0

for inputFile1 in inputTextFilePathList: 
    #### open the listing of XML files and iterates using a counter
    xmlFile1 = open(outputXMLFilePathList[counter], 'r')
    
    #### read the XML file 
    readxml = xmlFile1.read()

    #### creates a copy of the text file so we can use
    clean = readxml

    #### removes the new line and tabs from the doc leaving us with tags joining each other
    clean1 = re.sub(r'\n|\t','',clean)

    textFile1 = open(inputFile1, 'r')

    readIt = textFile1.read()

    def dateCleanFunk(textFile, xmlFile, tagType):
        #### this finds the tag and the data within and returns a list of needed data and tage type
        monthOYear = r'<span>\d+,\d+</span><type>'+tagType+'</type>'
        monthoYearCompile = re.compile(monthOYear, re.IGNORECASE)
        monthOYearFind = monthoYearCompile.findall(clean1)

        #### create an empty list to hold the results removing the tag location data
        monthOYearPositionList = []

        #### iterate through the monthOYearFind list and remove the data from the span tag we need and add to the list above
        for monthOYearPositions in monthOYearFind:
            monthOYearPosition = r'\d+,\d+'
            monthOYearPositionCompile = re.compile(monthOYearPosition, re.IGNORECASE)
            monthOYearPositionFind = monthOYearPositionCompile.findall(monthOYearPositions)
            monthOYearPositionList.append(monthOYearPositionFind)

        #### this is holding the listing for the locations that will be used to remove/change our day of month items
        monthOYearLocationList = []

        #### this takes the listing above and converts the contents from stings to int so we can use the numbers for location
        for monthOYearNumbers in monthOYearPositionList:
            for monthOYearSplitting in monthOYearNumbers:
                monthOYearNumbersSplit = monthOYearSplitting.split(',')
                monthOYearFinalNumbers = list(map(int, monthOYearNumbersSplit))
                monthOYearLocationList.append(monthOYearFinalNumbers)

        def dateReplace(text, startPosition, endPosition, placeHolder):
            return (text[:startPosition]+placeHolder+text[endPosition:])

        holdOutput =[textFile]

        for thoseLocations in monthOYearLocationList:
            lenghtOfHoldOutput = len(holdOutput)
            lengthOfReplacement = len(textFile[thoseLocations[0]:thoseLocations[1]])
            block = "\u00a9"
            blockFill = block*lengthOfReplacement
            less1 = lenghtOfHoldOutput-1
            lastItemInList = holdOutput[less1]  
            textHold = dateReplace(lastItemInList, thoseLocations[0], thoseLocations[1],blockFill)
            holdOutput.append(textHold)

        finalItem = len(holdOutput)
        finalItemReturn = holdOutput[finalItem-1]


        return(finalItemReturn)
 
    #### this funcation calls the time methods from Chronos we use for cleaning 
    testingList = dateCleanFunk(readIt, clean1,'Day-Of-Month')
    testingMonth = dateCleanFunk(testingList, clean1,'Month-Of-Year')
    testingYear = dateCleanFunk(testingMonth, clean1, 'Year')
    #print(testingYear)
    #replaceDay = dateCleanFunk(testingYear, clean1, 'Day')
    #replaceMonth = dateCleanFunk(replaceDay, clean1, 'Month')
    #replaceNumber = dateCleanFunk(replaceMonth, clean1, 'Number')
    #the listing of what the output files names will be

    #### this function replaces the copyright sign with one DATE token
    replaceThisText = testingYear
    copyRight = "\u00a9"
    replace10 = re.sub(copyRight*11,'DATE',replaceThisText)
    replace9 = re.sub(copyRight*10,'DATE',replace10)
    replace8 = re.sub(copyRight*9,'DATE',replace9)
    replace7 = re.sub(copyRight*8,'DATE',replace8)
    replace6 = re.sub(copyRight*7,'DATE',replace7)
    replace5 = re.sub(copyRight*6,'DATE',replace6)
    replace4 = re.sub(copyRight*5,'DATE',replace5)
    replace3 = re.sub(copyRight*4,'DATE',replace4)
    replace2 = re.sub(copyRight*3,'DATE',replace3)
    replace1 = re.sub(copyRight*2,'DATE',replace2)
    replace0 = re.sub(copyRight*1,'DATE',replace1)
    
    replaceLastYear = re.sub(r'DATE\/DATE\/\d+','DATE', replace0)
    replaceDate3 = re.sub(r'DATE\/DATE\/DATE','DATE', replaceLastYear)
    replaceDateNumAtEnd = re.sub(r'DATE\d+','DATE', replaceDate3)
    replaceNumThenDate = re.sub(r'\d+\/DATE\/DATE','DATE', replaceDateNumAtEnd)
    replaceNumThenDateWithDash = re.sub(r'\d+\-DATE\-DATE','DATE', replaceNumThenDate)
    replaceDateWordDateWithDash = re.sub(r'DATE\-\w+\-DATE','DATE', replaceNumThenDateWithDash)
    replaceDateSlashData = re.sub(r'DATE\/\w+\/DATE','DATE', replaceDateWordDateWithDash)
    replaceDateDashDashDate = re.sub(r'DATE\-DATE\-\w+','DATE', replaceDateSlashData)
    replaceDateDashDash = re.sub(r'DATE\-\w+\-\w+','DATE', replaceDateDashDashDate)
    replaceDatesandLotsofDashes = re.sub(r'DATE\-DATE\-DATE','DATE', replaceDateDashDash)     
    
    replaceJan = re.sub(r'Jan\-\w+\-\w+','DATE', replaceDatesandLotsofDashes)
    replaceJan1 = re.sub(r'JAN\-\w+\-\w+','DATE', replaceJan)
    replaceFeb = re.sub(r'Feb\-\w+\-\w+','DATE', replaceJan1)
    replaceFeb1 = re.sub(r'FEB\-\w+\-\w+','DATE', replaceFeb)
    replaceMar = re.sub(r'Mar\-\w+\-\w+','DATE', replaceFeb1)
    replaceMar1 = re.sub(r'MAR\-\w+\-\w+','DATE', replaceMar)
    replaceMar2 = re.sub(r'March\-\w+\-\w+','DATE', replaceMar1)
    replaceMar3 = re.sub(r'MARCH\-\w+\-\w+','DATE', replaceMar2)
    replaceApr = re.sub(r'Apr\-\w+\-\w+','DATE', replaceMar3)
    replaceApr1 = re.sub(r'APR\-\w+\-\w+','DATE', replaceApr)
    replaceApr2 = re.sub(r'April\-\w+\-\w+','DATE', replaceApr1)
    replaceApr3 = re.sub(r'APRIL\-\w+\-\w+','DATE', replaceApr2)
    replaceMay = re.sub(r'May\-\w+\-\w+','DATE', replaceApr3)
    replaceMay1 = re.sub(r'MAY\-\w+\-\w+','DATE', replaceMay)
    replaceJune = re.sub(r'Jun\-\w+\-\w+','DATE', replaceMay1)
    replaceJune1 = re.sub(r'JUN\-\w+\-\w+','DATE', replaceJune)
    replaceJune2 = re.sub(r'June\-\w+\-\w+','DATE', replaceJune1)
    replaceJune3 = re.sub(r'JUNE\-\w+\-\w+','DATE', replaceJune2)
    replaceJuly = re.sub(r'July\-\w+\-\w+','DATE', replaceJune3)
    replaceJuly1 = re.sub(r'JULY\-\w+\-\w+','DATE', replaceJuly)
    replaceAug = re.sub(r'Aug\-\w+\-\w+','DATE', replaceJuly1)
    replaceAug1 = re.sub(r'AUG\-\w+\-\w+','DATE', replaceAug)
    replaceSept = re.sub(r'Sept\-\w+\-\w+','DATE', replaceAug1)
    replaceSept1 = re.sub(r'SEPT\-\w+\-\w+','DATE', replaceSept)
    replaceOct = re.sub(r'Oct\-\w+\-\w+','DATE', replaceSept1)
    replaceOct1 = re.sub(r'OCT\-\w+\-\w+','DATE', replaceOct)
    replaceNov = re.sub(r'Nov\-\w+\-\w+','DATE', replaceOct1)
    replaceNov1 = re.sub(r'NOV\-\w+\-\w+','DATE', replaceNov)
    replaceDec = re.sub(r'Dec\-\w+\-\w+','DATE', replaceNov1)
    replaceDec1 = re.sub(r'DEC\-\w+\-\w+','DATE', replaceDec)
    
    RreplaceJan = re.sub(r'\d+\-Jan\-\d+','DATE', replaceDec1)
    RreplaceJan1 = re.sub(r'\d+\-JAN\-\d+','DATE', RreplaceJan)
    RreplaceFeb = re.sub(r'\d+\-Feb\-\d+','DATE', RreplaceJan1)
    RreplaceFeb1 = re.sub(r'\d+\-FEB\-\d+','DATE', RreplaceFeb)
    RreplaceMar = re.sub(r'\d+\-Mar\-\d+','DATE', RreplaceFeb1)
    RreplaceMar1 = re.sub(r'\d+\-MAR\-\d+','DATE', RreplaceMar)
    RreplaceMar2 = re.sub(r'\d+\-March\-\d+','DATE', RreplaceMar1)
    RreplaceMar3 = re.sub(r'\d+\-MARCH\-\d+','DATE', RreplaceMar2)
    RreplaceApr = re.sub(r'\d+\-Apr\-\d+','DATE', RreplaceMar3)
    RreplaceApr1 = re.sub(r'\d+\-APR\-\d+','DATE', RreplaceApr)
    RreplaceApr2 = re.sub(r'\d+\-April\-\d+','DATE', RreplaceApr1)
    RreplaceApr3 = re.sub(r'\d+\-APRIL\-\d+','DATE', RreplaceApr2)
    RreplaceMay = re.sub(r'\d+\-May\-\d+','DATE', RreplaceApr3)
    RreplaceMay1 = re.sub(r'\d+\-MAY\-\d+','DATE', RreplaceMay)
    RreplaceJune = re.sub(r'\d+\-Jun\-\d+','DATE', RreplaceMay1)
    RreplaceJune1 = re.sub(r'\d+\-JUN\-\d+','DATE', RreplaceJune)
    RreplaceJune2 = re.sub(r'\d+\-June\-\d+','DATE', RreplaceJune1)
    RreplaceJune3 = re.sub(r'\d+\-JUNE\-\d+','DATE', RreplaceJune2)
    RreplaceJuly = re.sub(r'\d+\-July\-\d+','DATE', RreplaceJune3)
    RreplaceJuly1 = re.sub(r'\d+\-JULY\-\d+','DATE', RreplaceJuly)
    RreplaceAug = re.sub(r'\d+\-Aug\-\d+','DATE', RreplaceJuly1)
    RreplaceAug1 = re.sub(r'\d+\-AUG\-\d+','DATE', RreplaceAug)
    RreplaceSept = re.sub(r'\d+\-Sept\-\d+','DATE', RreplaceAug1)
    RreplaceSept1 = re.sub(r'\d+\-SEPT\-\d+','DATE', RreplaceSept)
    RreplaceOct = re.sub(r'\d+\-Oct\-\d+','DATE', RreplaceSept1)
    RreplaceOct1 = re.sub(r'\d+\-OCT\-\d+','DATE', RreplaceOct)
    RreplaceNov = re.sub(r'\d+\-Nov\-\d+','DATE', RreplaceOct1)
    RreplaceNov1 = re.sub(r'\d+\-NOV\-\d+','DATE', RreplaceNov)
    RreplaceDec = re.sub(r'\d+\-Dec\-\d+','DATE', RreplaceNov1)
    RreplaceDec1 = re.sub(r'\d+\-DEC\-\d+','DATE', RreplaceDec)
    
    RreplaceJanR = re.sub(r'\d\-Jan\-\d+','DATE', RreplaceDec1)
    RreplaceJan1R = re.sub(r'\d\-JAN\-\d+','DATE', RreplaceJanR)
    RreplaceFebR = re.sub(r'\d\-Feb\-\d+','DATE', RreplaceJan1R)
    RreplaceFeb1R = re.sub(r'\d\-FEB\-\d+','DATE', RreplaceFebR)
    RreplaceMarR = re.sub(r'\d\-Mar\-\d+','DATE', RreplaceFeb1R)
    RreplaceMar1R = re.sub(r'\d\-MAR\-\d+','DATE', RreplaceMarR)
    RreplaceMar2R = re.sub(r'\d\-March\-\d+','DATE', RreplaceMar1R)
    RreplaceMar3R = re.sub(r'\d\-MARCH\-\d+','DATE', RreplaceMar2R)
    RreplaceAprR = re.sub(r'\d\-Apr\-\d+','DATE', RreplaceMar3R)
    RreplaceApr1R = re.sub(r'\d\-APR\-\d+','DATE', RreplaceAprR)
    RreplaceApr2R = re.sub(r'\d\-April\-\d+','DATE', RreplaceApr1R)
    RreplaceApr3R = re.sub(r'\d\-APRIL\-\d+','DATE', RreplaceApr2R)
    RreplaceMayR = re.sub(r'\d\-May\-\d+','DATE', RreplaceApr3R)
    RreplaceMay1R = re.sub(r'\d\-MAY\-\d+','DATE', RreplaceMayR)
    RreplaceJuneR = re.sub(r'\d\-Jun\-\d+','DATE', RreplaceMay1R)
    RreplaceJune1R = re.sub(r'\d\-JUN\-\d+','DATE', RreplaceJuneR)
    RreplaceJune2R = re.sub(r'\d\-June\-\d+','DATE', RreplaceJune1R)
    RreplaceJune3R = re.sub(r'\d\-JUNE\-\d+','DATE', RreplaceJune2R)
    RreplaceJulyR = re.sub(r'\d\-July\-\d+','DATE', RreplaceJune3R)
    RreplaceJuly1R = re.sub(r'\d\-JULY\-\d+','DATE', RreplaceJulyR)
    RreplaceAugR = re.sub(r'\d\-Aug\-\d+','DATE', RreplaceJuly1R)
    RreplaceAug1R = re.sub(r'\d\-AUG\-\d+','DATE', RreplaceAugR)
    RreplaceSeptR = re.sub(r'\d\-Sept\-\d+','DATE', RreplaceAug1R)
    RreplaceSept1R = re.sub(r'\d\-SEPT\-\d+','DATE', RreplaceSeptR)
    RreplaceOctR = re.sub(r'\d\-Oct\-\d+','DATE', RreplaceSept1R)
    RreplaceOct1R = re.sub(r'\d\-OCT\-\d+','DATE', RreplaceOctR)
    RreplaceNovR = re.sub(r'\d\-Nov\-\d+','DATE', RreplaceOct1R)
    RreplaceNov1R = re.sub(r'\d\-NOV\-\d+','DATE', RreplaceNovR)
    RreplaceDecR = re.sub(r'\d\-Dec\-\d+','DATE', RreplaceNov1R)
    RreplaceDec1R = re.sub(r'\d\-DEC\-\d+','DATE', RreplaceDecR)
    
    
    ######
    RreplaceJanA = re.sub(r'\d+\-January\-\d+','DATE', RreplaceDec1R)
    RreplaceJan1A = re.sub(r'\d+\-JANUARY\-\d+','DATE', RreplaceJanA)
    RreplaceFebA = re.sub(r'\d+\-February\-\d+','DATE', RreplaceJan1A)
    RreplaceFeb1A = re.sub(r'\d+\-FEBRUARY\-\d+','DATE', RreplaceFebA)
    RreplaceMarA = re.sub(r'\d+\-March\-\d+','DATE', RreplaceFeb1A)
    RreplaceMar1A = re.sub(r'\d+\-MARCH\-\d+','DATE', RreplaceMarA)
    RreplaceMar2A = re.sub(r'\d+\-March\-\d+','DATE', RreplaceMar1A)
    RreplaceMar3A = re.sub(r'\d+\-MARCH\-\d+','DATE', RreplaceMar2A)
    RreplaceAprA = re.sub(r'\d+\-April\-\d+','DATE', RreplaceMar3A)
    RreplaceApr1A = re.sub(r'\d+\-APRIL\-\d+','DATE', RreplaceAprA)
    RreplaceApr2A = re.sub(r'\d+\-April\-\d+','DATE', RreplaceApr1A)
    RreplaceApr3A = re.sub(r'\d+\-APRIL\-\d+','DATE', RreplaceApr2A)
    RreplaceMayA = re.sub(r'\d+\-May\-\d+','DATE', RreplaceApr3A)
    RreplaceMay1A = re.sub(r'\d+\-MAY\-\d+','DATE', RreplaceMayA)
    RreplaceJuneA = re.sub(r'\d+\-June\-\d+','DATE', RreplaceMay1A)
    RreplaceJune1A = re.sub(r'\d+\-JUNE\-\d+','DATE', RreplaceJuneA)
    RreplaceJune2A = re.sub(r'\d+\-June\-\d+','DATE', RreplaceJune1A)
    RreplaceJune3A = re.sub(r'\d+\-JUNE\-\d+','DATE', RreplaceJune2A)
    RreplaceJulyA = re.sub(r'\d+\-July\-\d+','DATE', RreplaceJune3A)
    RreplaceJuly1A = re.sub(r'\d+\-JULY\-\d+','DATE', RreplaceJulyA)
    RreplaceAugA = re.sub(r'\d+\-August\-\d+','DATE', RreplaceJuly1A)
    RreplaceAug1A = re.sub(r'\d+\-AUGUST\-\d+','DATE', RreplaceAugA)
    RreplaceSeptA = re.sub(r'\d+\-September\-\d+','DATE', RreplaceAug1A)
    RreplaceSept1A = re.sub(r'\d+\-SEPTEMBER\-\d+','DATE', RreplaceSeptA)
    RreplaceOctA = re.sub(r'\d+\-October\-\d+','DATE', RreplaceSept1A)
    RreplaceOct1A = re.sub(r'\d+\-OCTOBER\-\d+','DATE', RreplaceOctA)
    RreplaceNovA = re.sub(r'\d+\-November\-\d+','DATE', RreplaceOct1A)
    RreplaceNov1A = re.sub(r'\d+\-NOVEMBER\-\d+','DATE', RreplaceNovA)
    RreplaceDecA = re.sub(r'\d+\-December\-\d+','DATE', RreplaceNov1A)
    RreplaceDec1A = re.sub(r'\d+\-DECEMBER\-\d+','DATE', RreplaceDecA)
    
    RreplaceJanRB = re.sub(r'\d\-January\-\d+','DATE', RreplaceDec1A)
    RreplaceJan1RB = re.sub(r'\d\-JANUARY\-\d+','DATE', RreplaceJanRB)
    RreplaceFebRB = re.sub(r'\d\-February\-\d+','DATE', RreplaceJan1RB)
    RreplaceFeb1RB = re.sub(r'\d\-FEBRUARY\-\d+','DATE', RreplaceFebRB)
    RreplaceMarRB = re.sub(r'\d\-March\-\d+','DATE', RreplaceFeb1RB)
    RreplaceMar1RB = re.sub(r'\d\-MARCH\-\d+','DATE', RreplaceMarRB)
    RreplaceMar2RB = re.sub(r'\d\-March\-\d+','DATE', RreplaceMar1RB)
    RreplaceMar3RB = re.sub(r'\d\-MARCH\-\d+','DATE', RreplaceMar2RB)
    RreplaceAprRB = re.sub(r'\d\-April\-\d+','DATE', RreplaceMar3RB)
    RreplaceApr1RB = re.sub(r'\d\-APR\-\d+','DATE', RreplaceAprRB)
    RreplaceApr2RB = re.sub(r'\d\-April\-\d+','DATE', RreplaceApr1RB)
    RreplaceApr3RB = re.sub(r'\d\-APRIL\-\d+','DATE', RreplaceApr2RB)
    RreplaceMayRB = re.sub(r'\d\-May\-\d+','DATE', RreplaceApr3RB)
    RreplaceMay1RB = re.sub(r'\d\-MAY\-\d+','DATE', RreplaceMayRB)
    RreplaceJuneRB = re.sub(r'\d\-June\-\d+','DATE', RreplaceMay1RB)
    RreplaceJune1RB = re.sub(r'\d\-JUNE\-\d+','DATE', RreplaceJuneRB)
    RreplaceJune2RB = re.sub(r'\d\-June\-\d+','DATE', RreplaceJune1RB)
    RreplaceJune3RB = re.sub(r'\d\-JUNE\-\d+','DATE', RreplaceJune2RB)
    RreplaceJulyRB = re.sub(r'\d\-July\-\d+','DATE', RreplaceJune3RB)
    RreplaceJuly1RB = re.sub(r'\d\-JULY\-\d+','DATE', RreplaceJulyRB)
    RreplaceAugRB = re.sub(r'\d\-August\-\d+','DATE', RreplaceJuly1RB)
    RreplaceAug1RB = re.sub(r'\d\-AUGUST\-\d+','DATE', RreplaceAugRB)
    RreplaceSeptRB = re.sub(r'\d\-September\-\d+','DATE', RreplaceAug1RB)
    RreplaceSept1RB = re.sub(r'\d\-SEPTEMBER\-\d+','DATE', RreplaceSeptRB)
    RreplaceOctRB = re.sub(r'\d\-October\-\d+','DATE', RreplaceSept1RB)
    RreplaceOct1RB = re.sub(r'\d\-OCTOBER\-\d+','DATE', RreplaceOctRB)
    RreplaceNovRB = re.sub(r'\d\-November\-\d+','DATE', RreplaceOct1RB)
    RreplaceNov1RB = re.sub(r'\d\-NOVEMBER\-\d+','DATE', RreplaceNovRB)
    RreplaceDecRB = re.sub(r'\d\-December\-\d+','DATE', RreplaceNov1RB)
    RreplaceDec1RB = re.sub(r'\d\-DECEMBER\-\d+','DATE', RreplaceDecRB)
    
    
    ####  ####  ####
    
    RreplaceJanRP = re.sub(r'\d+Jan\d+','DATE', RreplaceDec1RB)
    RreplaceJan1RP = re.sub(r'\d+JAN\d+','DATE', RreplaceJanRP)
    RreplaceFebRP = re.sub(r'\d+Feb\d+','DATE', RreplaceJan1RP)
    RreplaceFeb1RP = re.sub(r'\d+FEB\d+','DATE', RreplaceFebRP)
    RreplaceMarRP = re.sub(r'\d+Mar\d+','DATE', RreplaceFeb1RP)
    RreplaceMar1RP = re.sub(r'\d+MAR\d+','DATE', RreplaceMarRP)
    RreplaceMar2RP = re.sub(r'\d+March\d+','DATE', RreplaceMar1RP)
    RreplaceMar3RP = re.sub(r'\d+MARCH\d+','DATE', RreplaceMar2RP)
    RreplaceAprRP = re.sub(r'\d+Apr\d+','DATE', RreplaceMar3RP)
    RreplaceApr1RP = re.sub(r'\d+APR\d+','DATE', RreplaceAprRP)
    RreplaceApr2RP = re.sub(r'\d+April\d+','DATE', RreplaceApr1RP)
    RreplaceApr3RP = re.sub(r'\d+APRIL\d+','DATE', RreplaceApr2RP)
    RreplaceMayRP = re.sub(r'\d+May\d+','DATE', RreplaceApr3RP)
    RreplaceMay1RP = re.sub(r'\d+MAY\d+','DATE', RreplaceMayRP)
    RreplaceJuneRP = re.sub(r'\d+Jun\d+','DATE', RreplaceMay1RP)
    RreplaceJune1RP = re.sub(r'\d+JUN\d+','DATE', RreplaceJuneRP)
    RreplaceJune2RP = re.sub(r'\d+June\d+','DATE', RreplaceJune1RP)
    RreplaceJune3RP = re.sub(r'\d+JUNE\d+','DATE', RreplaceJune2RP)
    RreplaceJulyRP = re.sub(r'\d+July\d+','DATE', RreplaceJune3RP)
    RreplaceJuly1RP = re.sub(r'\d+JULY\d+','DATE', RreplaceJulyRP)
    RreplaceAugRP = re.sub(r'\d+Aug\d+','DATE', RreplaceJuly1RP)
    RreplaceAug1RP = re.sub(r'\d+AUG\d+','DATE', RreplaceAugRP)
    RreplaceSeptRP = re.sub(r'\d+Sept\d+','DATE', RreplaceAug1RP)
    RreplaceSept1RP = re.sub(r'\d+SEPT\d+','DATE', RreplaceSeptRP)
    RreplaceOctRP = re.sub(r'\d+Oct\d+','DATE', RreplaceSept1RP)
    RreplaceOct1RP = re.sub(r'\d+OCT\d+','DATE', RreplaceOctRP)
    RreplaceNovRP = re.sub(r'\d+Nov\d+','DATE', RreplaceOct1RP)
    RreplaceNov1RP = re.sub(r'\d+NOV\d+','DATE', RreplaceNovRP)
    RreplaceDecRP = re.sub(r'\d+Dec\d+','DATE', RreplaceNov1RP)
    RreplaceDec1RP = re.sub(r'\d+DEC\d+','DATE', RreplaceDecRP)
    
    RreplaceJanAS = re.sub(r'\d+January\d+','DATE', RreplaceDec1RP)
    RreplaceJan1AS = re.sub(r'\d+JANUARY\d+','DATE', RreplaceJanAS)
    RreplaceFebAS = re.sub(r'\d+February\d+','DATE', RreplaceJan1AS)
    RreplaceFeb1AS = re.sub(r'\d+FEBRUARY\d+','DATE', RreplaceFebAS)
    RreplaceMarAS = re.sub(r'\d+March\d+','DATE', RreplaceFeb1AS)
    RreplaceMar1AS = re.sub(r'\d+MARCH\d+','DATE', RreplaceMarAS)
    RreplaceMar2AS = re.sub(r'\d+March\d+','DATE', RreplaceMar1AS)
    RreplaceMar3AS = re.sub(r'\d+MARCH\d+','DATE', RreplaceMar2AS)
    RreplaceAprAS = re.sub(r'\d+April\d+','DATE', RreplaceMar3AS)
    RreplaceApr1AS = re.sub(r'\d+APRIL\d+','DATE', RreplaceAprAS)
    RreplaceApr2AS = re.sub(r'\d+April\d+','DATE', RreplaceApr1AS)
    RreplaceApr3AS = re.sub(r'\d+APRIL\d+','DATE', RreplaceApr2AS)
    RreplaceMayAS = re.sub(r'\d+May\d+','DATE', RreplaceApr3AS)
    RreplaceMay1AS = re.sub(r'\d+MAY\d+','DATE', RreplaceMayAS)
    RreplaceJuneAS = re.sub(r'\d+June\d+','DATE', RreplaceMay1AS)
    RreplaceJune1AS = re.sub(r'\d+JUNE\d+','DATE', RreplaceJuneAS)
    RreplaceJune2AS = re.sub(r'\d+June\d+','DATE', RreplaceJune1AS)
    RreplaceJune3AS = re.sub(r'\d+JUNE\d+','DATE', RreplaceJune2AS)
    RreplaceJulyAS = re.sub(r'\d+July\d+','DATE', RreplaceJune3AS)
    RreplaceJuly1AS = re.sub(r'\d+JULY\d+','DATE', RreplaceJulyAS)
    RreplaceAugAS = re.sub(r'\d+August\d+','DATE', RreplaceJuly1AS)
    RreplaceAug1AS = re.sub(r'\d+AUGUST\d+','DATE', RreplaceAugAS)
    RreplaceSeptAS = re.sub(r'\d+September\d+','DATE', RreplaceAug1AS)
    RreplaceSept1AS = re.sub(r'\d+SEPTEMBER\d+','DATE', RreplaceSeptAS)
    RreplaceOctAS = re.sub(r'\d+October\d+','DATE', RreplaceSept1AS)
    RreplaceOct1AS = re.sub(r'\d+OCTOBER\d+','DATE', RreplaceOctAS)
    RreplaceNovAS = re.sub(r'\d+November\d+','DATE', RreplaceOct1AS)
    RreplaceNov1AS = re.sub(r'\d+NOVEMBER\d+','DATE', RreplaceNovAS)
    RreplaceDecAS = re.sub(r'\d+December\d+','DATE', RreplaceNov1AS)
    RreplaceDec1AS = re.sub(r'\d+DECEMBER\d+','DATE', RreplaceDecAS)
    
    
    ###  ### - 
    
    RreplaceJanRQ = re.sub(r'Jan\-\d+','DATE', RreplaceDec1AS)
    RreplaceJan1RQ = re.sub(r'JAN\-\d+','DATE', RreplaceJanRQ)
    RreplaceFebRQ = re.sub(r'Feb\-\d+','DATE', RreplaceJan1RQ)
    RreplaceFeb1RQ = re.sub(r'FEB\-\d+','DATE', RreplaceFebRQ)
    RreplaceMarRQ = re.sub(r'Mar\-\d+','DATE', RreplaceFeb1RQ)
    RreplaceMar1RQ = re.sub(r'MAR\-\d+','DATE', RreplaceMarRQ)
    RreplaceMar2RQ = re.sub(r'March\-\d+','DATE', RreplaceMar1RQ)
    RreplaceMar3RQ = re.sub(r'MARCH\-\d+','DATE', RreplaceMar2RQ)
    RreplaceAprRQ = re.sub(r'Apr\-\d+','DATE', RreplaceMar3RQ)
    RreplaceApr1RQ = re.sub(r'APR\-\d+','DATE', RreplaceAprRQ)
    RreplaceApr2RQ = re.sub(r'April\-\d+','DATE', RreplaceApr1RQ)
    RreplaceApr3RQ = re.sub(r'APRIL\-\d+','DATE', RreplaceApr2RQ)
    RreplaceMayRQ = re.sub(r'May\-\d+','DATE', RreplaceApr3RQ)
    RreplaceMay1RQ = re.sub(r'MAY\-\d+','DATE', RreplaceMayRQ)
    RreplaceJuneRQ = re.sub(r'Jun\-\d+','DATE', RreplaceMay1RQ)
    RreplaceJune1RQ = re.sub(r'JUN\-\d+','DATE', RreplaceJuneRQ)
    RreplaceJune2RQ = re.sub(r'June\-\d+','DATE', RreplaceJune1RQ)
    RreplaceJune3RQ = re.sub(r'JUNE\-\d+','DATE', RreplaceJune2RQ)
    RreplaceJulyRQ = re.sub(r'July\-\d+','DATE', RreplaceJune3RQ)
    RreplaceJuly1RQ = re.sub(r'JULY\-\d+','DATE', RreplaceJulyRQ)
    RreplaceAugRQ = re.sub(r'Aug\-\d+','DATE', RreplaceJuly1RQ)
    RreplaceAug1RQ = re.sub(r'AUG\-\d+','DATE', RreplaceAugRQ)
    RreplaceSeptRQ = re.sub(r'Sept\-\d+','DATE', RreplaceAug1RQ)
    RreplaceSept1RQ = re.sub(r'SEPT\-\d+','DATE', RreplaceSeptRQ)
    RreplaceOctRQ = re.sub(r'Oct\-\d+','DATE', RreplaceSept1RQ)
    RreplaceOct1RQ = re.sub(r'OCT\-\d+','DATE', RreplaceOctRQ)
    RreplaceNovRQ = re.sub(r'Nov\-\d+','DATE', RreplaceOct1RQ)
    RreplaceNov1RQ = re.sub(r'NOV\-\d+','DATE', RreplaceNovRQ)
    RreplaceDecRQ = re.sub(r'Dec\-\d+','DATE', RreplaceNov1RQ)
    RreplaceDec1RQ = re.sub(r'DEC\-\d+','DATE', RreplaceDecRQ)
    
    RreplaceJanAK = re.sub(r'January\-\d+','DATE', RreplaceDec1RQ)
    RreplaceJan1AK = re.sub(r'JANUARY\-\d+','DATE', RreplaceJanAK)
    RreplaceFebAK = re.sub(r'February\-\d+','DATE', RreplaceJan1AK)
    RreplaceFeb1AK = re.sub(r'FEBRUARY\-\d+','DATE', RreplaceFebAK)
    RreplaceMarAK = re.sub(r'March\-\d+','DATE', RreplaceFeb1AK)
    RreplaceMar1AK = re.sub(r'MARCH\-\d+','DATE', RreplaceMarAK)
    RreplaceMar2AK = re.sub(r'March\-\d+','DATE', RreplaceMar1AK)
    RreplaceMar3AK = re.sub(r'MARCH\-\d+','DATE', RreplaceMar2AK)
    RreplaceAprAK = re.sub(r'April\-\d+','DATE', RreplaceMar3AK)
    RreplaceApr1AK = re.sub(r'APRIL\-\d+','DATE', RreplaceAprAK)
    RreplaceApr2AK = re.sub(r'April\-\d+','DATE', RreplaceApr1AK)
    RreplaceApr3AK = re.sub(r'APRIL\-\d+','DATE', RreplaceApr2AK)
    RreplaceMayAK = re.sub(r'May\-\d+','DATE', RreplaceApr3AK)
    RreplaceMay1AK = re.sub(r'MAY\-\d+','DATE', RreplaceMayAK)
    RreplaceJuneAK = re.sub(r'June\-\d+','DATE', RreplaceMay1AK)
    RreplaceJune1AK = re.sub(r'JUNE\-\d+','DATE', RreplaceJuneAK)
    RreplaceJune2AK = re.sub(r'June\-\d+','DATE', RreplaceJune1AK)
    RreplaceJune3AK = re.sub(r'JUNE\-\d+','DATE', RreplaceJune2AK)
    RreplaceJulyAK = re.sub(r'July\-\d+','DATE', RreplaceJune3AK)
    RreplaceJuly1AK = re.sub(r'JULY\-\d+','DATE', RreplaceJulyAK)
    RreplaceAugAK = re.sub(r'August\-\d+','DATE', RreplaceJuly1AK)
    RreplaceAug1AK = re.sub(r'AUGUST\-\d+','DATE', RreplaceAugAK)
    RreplaceSeptAK = re.sub(r'September\-\d+','DATE', RreplaceAug1AK)
    RreplaceSept1AK = re.sub(r'SEPTEMBER\-\d+','DATE', RreplaceSeptAK)
    RreplaceOctAK = re.sub(r'October\-\d+','DATE', RreplaceSept1AK)
    RreplaceOct1AK = re.sub(r'OCTOBER\-\d+','DATE', RreplaceOctAK)
    RreplaceNovAK = re.sub(r'November\-\d+','DATE', RreplaceOct1AK)
    RreplaceNov1AK = re.sub(r'NOVEMBER\-\d+','DATE', RreplaceNovAK)
    RreplaceDecAK = re.sub(r'December\-\d+','DATE', RreplaceNov1AK)
    RreplaceDec1AK = re.sub(r'DECEMBER\-\d+','DATE', RreplaceDecAK)
    
    dateWith2Spaces = re.sub(r'DATE\sDATE\sDate','DATE',RreplaceDec1AK)
    dateWith1Space = re.sub(r'DATE\sDATE','DATE',dateWith2Spaces)
    
    

    
    #### the following finds our target list idenifers and converts to unicode characters 

    numberMap1 = {r'\d+\.\)':'NUM',
                  '1.)':u'\u0241',
                  '2.)':u'\u0242',
                  '3.)':u'\u0243',
                  '4.)':u'\u0244',
                  '5.)':u'\u0245',
                  '6.)':u'\u0246',
                  '7.)':u'\u0247',
                  '8.)':u'\u0248',
                  '9.)':u'\u0249',
                  '10.)':u'\u0250',
                  '11.)':u'\u0251',
                  '12.)':u'\u0252',
                  '13.)':u'\u0253',
                  '14.)':u'\u0254',
                  '15.)':u'\u0255',
                  '16.)':u'\u0256',
                  '17.)':u'\u0257',
                  '18.)':u'\u0258',
                  '19.)':u'\u0259',
                  '20.)':u'\u0260'}

    replaceNumberMap1 = re.sub(r'\d+\.\)', lambda x: numberMap1.get(x.group(),x.group(0)),dateWith1Space)

    numberMap2 = {r'\d+\)':'NUM',
                  '1)':u'\u0261',
                  '2)':u'\u0262',
                  '3)':u'\u0263',
                  '4)':u'\u0264',
                  '5)':u'\u0265',
                  '6)':u'\u0266',
                  '7)':u'\u0267',
                  '8)':u'\u0268',
                  '9)':u'\u0269',
                  '10)':u'\u0270',
                  '11)':u'\u0271',
                  '12)':u'\u0272',
                  '13)':u'\u0273',
                  '14)':u'\u0274',
                  '15)':u'\u0275',
                  '16)':u'\u0276',
                  '17)':u'\u0277',
                  '18)':u'\u0278',
                  '19)':u'\u0279',
                  '20)':u'\u0280'}

    replaceNumberMap2 = re.sub(r'\d+\)', lambda x: numberMap2.get(x.group(),x.group(0)),replaceNumberMap1)

    # numberMap3 = { r'\d+\s\)':'NUM',
    #               '1 )':u'\u0281',
    #               '2 )':u'\u0282',
    #               '3 )':u'\u0283',
    #               '4 )':u'\u0284',
    #               '5 )':u'\u0285',
    #               '6 )':u'\u0286',
    #               '7 )':u'\u0287',
    #               '8 )':u'\u0288',
    #               '9 )':u'\u0289',
    #               '10 )':u'\u0290',
    #               '11 )':u'\u0291',
    #               '12 )':u'\u0292',
    #               '13 )':u'\u0293',
    #               '14 )':u'\u0294',
    #               '15 )':u'\u0295',
    #               '16 )':u'\u0296',
    #               '17 )':u'\u0297',
    #               '18 )':u'\u0298',
    #               '19 )':u'\u0299',
    #               '20 )':u'\u029A'}

    # replaceNumberMap3 = re.sub(r'\d+\s\)', lambda x: numberMap3.get(x.group(),x.group(0)),replaceNumberMap2)

    numberMap4 = {r'd+\.\s':'NUM',
                  '1. ':u'\u0200',
                  '2. ':u'\u0201',
                  '3. ':u'\u0202',
                  '4. ':u'\u0203',
                  '5. ':u'\u0204',
                  '6. ':u'\u0205',
                  '7. ':u'\u0206',
                  '8. ':u'\u0207',
                  '9. ':u'\u0208',
                  '10. ':u'\u0209',
                  '11. ':u'\u0210',
                  '12. ':u'\u0211',
                  '13. ':u'\u0212',
                  '14. ':u'\u0213',
                  '15. ':u'\u0214',
                  '16. ':u'\u0215',
                  '17. ':u'\u0216',
                  '18. ':u'\u0217',
                  '19. ':u'\u0218',
                  '20. ':u'\u0219'}

    replaceNumberMap4 = re.sub(r'\d+\.\s', lambda x: numberMap4.get(x.group(),x.group(0)),replaceNumberMap2)


    #### convert all remining numbers to NUM
    numbers2NUM = re.sub(r'\d+\.\d+','NUM',replaceNumberMap4)
    numbers2NUM1 = re.sub(r'\d+','NUM',numbers2NUM)


    numberExtra = re.sub(r'\%NUM\%|\^NUM\^|\*NUM\*|\+NUM\+|\-NUM\-|\=NUM\=|\#NUM\#|\/NUM\/|\~NUM\~|\`NUM\`|\"NUM\"|\'NUM\'','NUM',numbers2NUM1)

    numberExtra1 = re.sub(r'NUM\%|NUM\^|NUM\*|NUM\+|NUM\-|NUM\=|NUM\#|NUM\/|NUM\~|NUM\`|NUM\"|NUM\'','NUM',numberExtra)
    
    numberExtra2 = re.sub(r'\<NUM|\>NUM|NUM\smg|NUMmg|NUML|NUM\sL|NUMml|NUMml\.|NUMC\.|NUMC|NUMF\.|NUMF|NUMmg\.|\%NUM|\^NUM|\*NUM|\+NUM|\-NUM|\=NUM|\#NUM|\/NUM|\~NUM|\`NUM|\"NUM|\'NUM','NUM',numberExtra1)
    
    #numberExtra3 = re.sub(r'NUM\s+\,\s+NUM\s+\,\s+NUM\s+\,\s+NUM|NUM\s+\,\s+NUM\s+\,\s+NUM|NUM\s+\,\s+NUM','NUM',numberExtra2)
    
    numberExtra3A = re.sub(r'NUMPM|NUM\:NUM|NUMAM|NUM\:NUMPM','NUM',numberExtra2)
    
    numberExtra3B = re.sub(r'\w+NUM\w+|\w+NUM|NUM\w+|NUMPM|NUMAM','NUM',numberExtra3A)

    numberExtra3C = re.sub(r'NUM\:NUM', 'NUM', numberExtra3B)
    
    numberExtra4 = re.sub(r'NUMNUMNUM|NUMNUM','NUM', numberExtra3C)

    ### remap the mapping of list identifers back to their original form

    remapNumberMap1 = {u'\u0241':'1.)',
                       u'\u0242':'2.)',
                       u'\u0243':'3.)',
                       u'\u0244':'4.)',
                       u'\u0245':'5.)',
                       u'\u0246':'6.)',
                       u'\u0247':'7.)',
                       u'\u0248':'8.)',
                       u'\u0249':'9.)',
                       u'\u0250':'10.)',
                       u'\u0251':'11.)',
                       u'\u0252':'12.)',
                       u'\u0253':'13.)',
                       u'\u0254':'14.)',
                       u'\u0255':'15.)',
                       u'\u0256':'16.)',
                       u'\u0257':'17.)',
                       u'\u0258':'18.)',
                       u'\u0259':'19.)',
                       u'\u0260':'20.)'}


    remapNumberMap11= u'\u0241'
    remapNumberMap12= u'\u0242'
    remapNumberMap13= u'\u0243'
    remapNumberMap14= u'\u0244'
    remapNumberMap15= u'\u0245'
    remapNumberMap16= u'\u0246'
    remapNumberMap17= u'\u0247'
    remapNumberMap18= u'\u0248'
    remapNumberMap19= u'\u0249'
    remapNumberMap110= u'\u0250'
    remapNumberMap111= u'\u0251'
    remapNumberMap112= u'\u0252'
    remapNumberMap113= u'\u0253'
    remapNumberMap114= u'\u0254'
    remapNumberMap115= u'\u0255'
    remapNumberMap116= u'\u0256'
    remapNumberMap117= u'\u0257'
    remapNumberMap118= u'\u0258'
    remapNumberMap119= u'\u0259'
    remapNumberMap120= u'\u0260'



    replaceRemapNumberMap1 = re.sub(remapNumberMap11, '1.)',numberExtra4)
    replaceRemapNumberMap11 = re.sub(remapNumberMap12, '2.)',replaceRemapNumberMap1)
    replaceRemapNumberMap12 = re.sub(remapNumberMap13, '3.)',replaceRemapNumberMap11)
    replaceRemapNumberMap13 = re.sub(remapNumberMap14, '4.)',replaceRemapNumberMap12)
    replaceRemapNumberMap14 = re.sub(remapNumberMap15, '5.)',replaceRemapNumberMap13)
    replaceRemapNumberMap15 = re.sub(remapNumberMap16, '6.)',replaceRemapNumberMap14)
    replaceRemapNumberMap16 = re.sub(remapNumberMap17, '7.)',replaceRemapNumberMap15)
    replaceRemapNumberMap17 = re.sub(remapNumberMap18, '8.)',replaceRemapNumberMap16)
    replaceRemapNumberMap18 = re.sub(remapNumberMap19,'9.)',replaceRemapNumberMap17)
    replaceRemapNumberMap19= re.sub(remapNumberMap110, '10.)',replaceRemapNumberMap18)
    replaceRemapNumberMap110 = re.sub(remapNumberMap111, '11.)',replaceRemapNumberMap19)
    replaceRemapNumberMap111 = re.sub(remapNumberMap112, '12.)',replaceRemapNumberMap110)
    replaceRemapNumberMap112 = re.sub(remapNumberMap113, '13.)',replaceRemapNumberMap111)
    replaceRemapNumberMap113 = re.sub(remapNumberMap114, '14.)',replaceRemapNumberMap112)
    replaceRemapNumberMap114 = re.sub(remapNumberMap115, '15.)',replaceRemapNumberMap113)
    replaceRemapNumberMap115 = re.sub(remapNumberMap116, '16.)',replaceRemapNumberMap114)
    replaceRemapNumberMap116 = re.sub(remapNumberMap117, '17.)',replaceRemapNumberMap115)
    replaceRemapNumberMap117 = re.sub(remapNumberMap118, '18.)',replaceRemapNumberMap116)
    replaceRemapNumberMap118 = re.sub(remapNumberMap119, '19.)',replaceRemapNumberMap117)
    replaceRemapNumberMap119 = re.sub(remapNumberMap120, '20.)',replaceRemapNumberMap118)



    remapNumberMap2 = {u'\u0261':'1)',
                       u'\u0262':'2)',
                       u'\u0263':'3)',
                       u'\u0264':'4)',
                       u'\u0265':'5)',
                       u'\u0266':'6)',
                       u'\u0267':'7)',
                       u'\u0268':'8)',
                       u'\u0269':'9)',
                       u'\u0270':'10)',
                       u'\u0271':'11)',
                       u'\u0272':'12)',
                       u'\u0273':'13)',
                       u'\u0274':'14)',
                       u'\u0275':'15)',
                       u'\u0276':'16)',
                       u'\u0277':'17)',
                       u'\u0278':'18)',
                       u'\u0279':'19)',
                       u'\u0280':'20)'}

    remapNumberMap21= u'\u0261'
    remapNumberMap22= u'\u0262'
    remapNumberMap23= u'\u0263'
    remapNumberMap24= u'\u0264'
    remapNumberMap25= u'\u0265'
    remapNumberMap26= u'\u0266'
    remapNumberMap27= u'\u0267'
    remapNumberMap28= u'\u0268'
    remapNumberMap29= u'\u0269'
    remapNumberMap210= u'\u0270'
    remapNumberMap211= u'\u0271'
    remapNumberMap212= u'\u0272'
    remapNumberMap213= u'\u0273'
    remapNumberMap214= u'\u0274'
    remapNumberMap215= u'\u0275'
    remapNumberMap216= u'\u0276'
    remapNumberMap217= u'\u0277'
    remapNumberMap218= u'\u0278'
    remapNumberMap219= u'\u0279'
    remapNumberMap220= u'\u0280'



    replaceRemapNumberMap2 = re.sub(remapNumberMap21, '1)',replaceRemapNumberMap119)
    replaceRemapNumberMap21 = re.sub(remapNumberMap22, '2)',replaceRemapNumberMap2)
    replaceRemapNumberMap22 = re.sub(remapNumberMap23, '3)',replaceRemapNumberMap21)
    replaceRemapNumberMap23 = re.sub(remapNumberMap24, '4)',replaceRemapNumberMap22)
    replaceRemapNumberMap24 = re.sub(remapNumberMap25, '5)',replaceRemapNumberMap23)
    replaceRemapNumberMap25 = re.sub(remapNumberMap26, '6)',replaceRemapNumberMap24)
    replaceRemapNumberMap26 = re.sub(remapNumberMap27, '7)',replaceRemapNumberMap25)
    replaceRemapNumberMap27 = re.sub(remapNumberMap28,'8)',replaceRemapNumberMap26)
    replaceRemapNumberMap28 = re.sub(remapNumberMap29, '9)',replaceRemapNumberMap27)
    replaceRemapNumberMap29 = re.sub(remapNumberMap210, '10)',replaceRemapNumberMap28)
    replaceRemapNumberMap210 = re.sub(remapNumberMap211, '11)',replaceRemapNumberMap29)
    replaceRemapNumberMap211 = re.sub(remapNumberMap212, '12)',replaceRemapNumberMap210)
    replaceRemapNumberMap212 = re.sub(remapNumberMap213, '13)',replaceRemapNumberMap211)
    replaceRemapNumberMap213 = re.sub(remapNumberMap214, '14)',replaceRemapNumberMap212)
    replaceRemapNumberMap214 = re.sub(remapNumberMap215, '15)',replaceRemapNumberMap213)
    replaceRemapNumberMap215 = re.sub(remapNumberMap216, '16)',replaceRemapNumberMap214)
    replaceRemapNumberMap216 = re.sub(remapNumberMap217, '17)',replaceRemapNumberMap215)
    replaceRemapNumberMap217 = re.sub(remapNumberMap218, '18)',replaceRemapNumberMap216)
    replaceRemapNumberMap218 = re.sub(remapNumberMap219, '19)',replaceRemapNumberMap217)
    replaceRemapNumberMap219 = re.sub(remapNumberMap220, '20)',replaceRemapNumberMap218)


    # remapNumberMap3 = {u'\u0281':'1 )',
    #                    u'\u0282':'2 )',
    #                    u'\u0283':'3 )',
    #                    u'\u0284':'4 )',
    #                    u'\u0285':'5 )',
    #                    u'\u0286':'6 )',
    #                    u'\u0287':'7 )',
    #                    u'\u0288':'8 )',
    #                    u'\u0289':'9 )',
    #                    u'\u0290':'10 )',
    #                    u'\u0291':'11 )',
    #                    u'\u0292':'12 )',
    #                    u'\u0293':'13 )',
    #                    u'\u0294':'14 )',
    #                    u'\u0295':'15 )',
    #                    u'\u0296':'16 )',
    #                    u'\u0297':'17 )',
    #                    u'\u0298':'18 )',
    #                    u'\u0299':'19 )',
    #                    u'\u029A':'20 )'}

    # remapNumberMap31= u'\u0281'
    # remapNumberMap32= u'\u0282'
    # remapNumberMap33= u'\u0283'
    # remapNumberMap34= u'\u0284'
    # remapNumberMap35= u'\u0285'
    # remapNumberMap36= u'\u0286'
    # remapNumberMap37= u'\u0287'
    # remapNumberMap38= u'\u0288'
    # remapNumberMap39= u'\u0289'
    # remapNumberMap310= u'\u0290'
    # remapNumberMap311= u'\u0291'
    # remapNumberMap312= u'\u0292'
    # remapNumberMap313= u'\u0293'
    # remapNumberMap314= u'\u0294'
    # remapNumberMap315= u'\u0295'
    # remapNumberMap316= u'\u0296'
    # remapNumberMap317= u'\u0297'
    # remapNumberMap318= u'\u0298'
    # remapNumberMap319= u'\u0299'
    # remapNumberMap320= u'\u029A'



    # replaceRemapNumberMap3 = re.sub(remapNumberMap31, '1 )',replaceRemapNumberMap219)
    # replaceRemapNumberMap31 = re.sub(remapNumberMap32, '2 )',replaceRemapNumberMap3)
    # replaceRemapNumberMap32 = re.sub(remapNumberMap33, '3 )',replaceRemapNumberMap31)
    # replaceRemapNumberMap33 = re.sub(remapNumberMap34, '4 )',replaceRemapNumberMap32)
    # replaceRemapNumberMap34 = re.sub(remapNumberMap35, '5 )',replaceRemapNumberMap33)
    # replaceRemapNumberMap35 = re.sub(remapNumberMap36, '6 )',replaceRemapNumberMap34)
    # replaceRemapNumberMap36 = re.sub(remapNumberMap37, '7 )',replaceRemapNumberMap35)
    # replaceRemapNumberMap37 = re.sub(remapNumberMap38, '8 )',replaceRemapNumberMap36)
    # replaceRemapNumberMap38 = re.sub(remapNumberMap39, '9 )',replaceRemapNumberMap37)
    # replaceRemapNumberMap39 = re.sub(remapNumberMap310, '10 )',replaceRemapNumberMap38)
    # replaceRemapNumberMap310 = re.sub(remapNumberMap311, '11 )',replaceRemapNumberMap39)
    # replaceRemapNumberMap311 = re.sub(remapNumberMap312, '12 )',replaceRemapNumberMap310)
    # replaceRemapNumberMap312 = re.sub(remapNumberMap313, '13 )',replaceRemapNumberMap311)
    # replaceRemapNumberMap313 = re.sub(remapNumberMap314, '14 )',replaceRemapNumberMap312)
    # replaceRemapNumberMap314 = re.sub(remapNumberMap315, '15 )',replaceRemapNumberMap313)
    # replaceRemapNumberMap315 = re.sub(remapNumberMap316, '16 )',replaceRemapNumberMap314)
    # replaceRemapNumberMap316 = re.sub(remapNumberMap317, '17 )',replaceRemapNumberMap315)
    # replaceRemapNumberMap317 = re.sub(remapNumberMap318, '18 )',replaceRemapNumberMap316)
    # replaceRemapNumberMap318 = re.sub(remapNumberMap319, '19 )',replaceRemapNumberMap317)
    # replaceRemapNumberMap319 = re.sub(remapNumberMap320, '20 )',replaceRemapNumberMap318)


    remapNumberMap4 = {u'\u0200':'1. ',
                       u'\u0201':'2. ',
                       u'\u0202':'3. ',
                       u'\u0203':'4. ',
                       u'\u0204':'5. ',
                       u'\u0205':'6. ',
                       u'\u0206':'7. ',
                       u'\u0207':'8. ',
                       u'\u0208':'9. ',
                       u'\u0209':'10. ',
                       u'\u0210':'11. ',
                       u'\u0211':'12. ',
                       u'\u0212':'13. ',
                       u'\u0213':'14. ',
                       u'\u0214':'15. ',
                       u'\u0215':'16. ',
                       u'\u0216':'17. ',
                       u'\u0217':'18. ',
                       u'\u0218':'19. ',
                       u'\u0219':'20. '}

    remapNumberMap41= u'\u0200'
    remapNumberMap42= u'\u0201'
    remapNumberMap43= u'\u0202'
    remapNumberMap44= u'\u0203'
    remapNumberMap45= u'\u0204'
    remapNumberMap46= u'\u0205'
    remapNumberMap47= u'\u0206'
    remapNumberMap48= u'\u0207'
    remapNumberMap49= u'\u0208'
    remapNumberMap410= u'\u0209'
    remapNumberMap411= u'\u0210'
    remapNumberMap412= u'\u0211'
    remapNumberMap413= u'\u0212'
    remapNumberMap414= u'\u0213'
    remapNumberMap415= u'\u0214'
    remapNumberMap416= u'\u0215'
    remapNumberMap417= u'\u0216'
    remapNumberMap418= u'\u0217'
    remapNumberMap419= u'\u0218'
    remapNumberMap420= u'\u0219'


    replaceRemapNumberMap4 = re.sub(remapNumberMap41, '1. ',replaceRemapNumberMap219)
    replaceRemapNumberMap41 = re.sub(remapNumberMap42, '2. ',replaceRemapNumberMap4)
    replaceRemapNumberMap42 = re.sub(remapNumberMap43, '3. ',replaceRemapNumberMap41)
    replaceRemapNumberMap43 = re.sub(remapNumberMap44, '4. ',replaceRemapNumberMap42)
    replaceRemapNumberMap44 = re.sub(remapNumberMap45, '5. ',replaceRemapNumberMap43)
    replaceRemapNumberMap45 = re.sub(remapNumberMap46, '6. ',replaceRemapNumberMap44)
    replaceRemapNumberMap46 = re.sub(remapNumberMap47, '7. ',replaceRemapNumberMap45)
    replaceRemapNumberMap47 = re.sub(remapNumberMap48, '8. ',replaceRemapNumberMap46)
    replaceRemapNumberMap48 = re.sub(remapNumberMap49, '9. ',replaceRemapNumberMap47)
    replaceRemapNumberMap49 = re.sub(remapNumberMap410, '10. ',replaceRemapNumberMap48)
    replaceRemapNumberMap410 = re.sub(remapNumberMap411, '11. ',replaceRemapNumberMap49)
    replaceRemapNumberMap411 = re.sub(remapNumberMap412, '12. ',replaceRemapNumberMap410)
    replaceRemapNumberMap412 = re.sub(remapNumberMap413, '13. ',replaceRemapNumberMap411)
    replaceRemapNumberMap413 = re.sub(remapNumberMap414, '14. ',replaceRemapNumberMap412)
    replaceRemapNumberMap414 = re.sub(remapNumberMap415, '15. ',replaceRemapNumberMap413)
    replaceRemapNumberMap415 = re.sub(remapNumberMap416, '16. ',replaceRemapNumberMap414)
    replaceRemapNumberMap416 = re.sub(remapNumberMap417, '17. ',replaceRemapNumberMap415)
    replaceRemapNumberMap417 = re.sub(remapNumberMap418, '18. ',replaceRemapNumberMap416)
    replaceRemapNumberMap418 = re.sub(remapNumberMap419, '19. ',replaceRemapNumberMap417)
    replaceRemapNumberMap419 = re.sub(remapNumberMap420, '20. ',replaceRemapNumberMap418)

    low = replaceRemapNumberMap419.lower()
    #print(replaceRemapNumberMap419)

    # outputTextFile = open('C:/Users/bat/Desktop/0002.txt','w')
    # outputTextFile.write(replaceRemapNumberMap419)
    # outputTextFile.close()

    # openMe = open('C:/Users/wccramer/Desktop/0002.txt','r').read()
    # print(OpenMe)


    #### store the output file from all the cleaning 
    mergeOutputName = os.path.join(outFolder+'/',foldersForInput[counter]+'.txt')    
    finialOutputFileName = open(mergeOutputName,'w')
    finialOutputFileName.write(low)
    finialOutputFileName.close()
    #counter = counter+1
    
    #os.remove(mergeOutputName)
newDataOutputPath1 = outFolder+'/results'
newDataOutputPath2 = outFolder+'/data'
newDataOutputPath3 = outFolder+'/chronosCleaned'
shutil.rmtree(newDataOutputPath1)
shutil.rmtree(newDataOutputPath2)
shutil.rmtree(newDataOutputPath3)
# os.rmdir(newDataOutputPath)
# os.rmdir(newDataInputPath)
#os.rmdir(chronosCleaned)
            
#print("Ya Done!")
#print(numberReplace)

