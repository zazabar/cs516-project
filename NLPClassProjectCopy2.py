
# coding: utf-8

# In[24]:


import re
import os
import fnmatch
import bs4 as bs
import pandas as pd
from os import listdir
from os.path import isfile
import sys
import shlex, subprocess
import time
from subprocess import *


# In[133]:


#### users provides input for their text data
print('Please Enter The Path Where Your Raw Input Text Data is Located')
originalTextDocsPath = [input()]

#### users provides input for where they want their data to land
print('Please Enter The Path Where You Want Your Data To Be Output')
pathForInputFoldersForChronos = input()

#### users provides input for the location of Chronos 
print('Please Provide the Path for the Chronos Tool')
chronosLocation = input()

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
newDataOutputPath = pathForOutputFoldersForChronos+'/'+'/results/my_output/' 
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
    


# In[134]:


#### the block below creates a listing of the folders that will be input into Chronos 
my_inputPath = ''.join((pathForInputFoldersForChronos, '/data/my_input/'))

foldersForInput = os.listdir(my_inputPath)

foldersForInput

inputFolderList =[]

for folder in foldersForInput:
     inputFolderList.append(''.join((my_inputPath, folder)))


# In[135]:



#### the block below creates a listing of the files that will be input into Chronos
inputTextFilePathList = []

for filePath in inputFolderList:
    for file in os.listdir(filePath):
        if fnmatch.fnmatch(file, '*.txt'):
            inputTextFilePathList.append(''.join((filePath+'/', file)))


# In[136]:



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
command = "python %s -i %s -x "'.txt'" -o %s -m SVM -d %s -c %s" % (chronosPath,myDataInput,myDataOutput,joinFilesData,joinFilesClass)

p = subprocess.Popen(command).wait()


# In[137]:



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

            


# In[138]:



#### the block below creates a listing of the completed files
outputXMLFilePathList = []

for outputXMLFilePath in outputFolderList:
    for outputXMLFile in os.listdir(outputXMLFilePath):
        if fnmatch.fnmatch(outputXMLFile, '*.XML'):
            outputXMLFilePathList.append(''.join((outputXMLFilePath+'/', outputXMLFile)))


# In[148]:


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
    
    
    #numberReplace = re.sub(r'\d+','NUM', dateWith1Space)

    
    #### store the output file from all the cleaning 
    mergeOutputName = os.path.join(chronosCleaned+'/',foldersForInput[counter]+'.txt')    
    finialOutputFileName = open(mergeOutputName,'w')
    finialOutputFileName.write(dateWith1Space)
    finialOutputFileName.close()
    counter = counter+1
    
print("Ya Done!")
#print(numberReplace)

