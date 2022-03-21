import csv,tkinter,math,numpy
import pandas as pd
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfilename
from tabulate import tabulate

def main():
    title()
    inFile = openFile()
    df,numCols,colList = readFile(inFile)
    meanList = getMean(df,colList)
    varList = getVar(df,colList)
    sampSizeList = getSampSize(df,colList)
    grandMean = getGrandMean(meanList)
    SSB,SSBDF,SSBMS = calcSSB(grandMean,meanList,varList,sampSizeList,numCols)
    SSW = calcSSW(varList,sampSizeList)
    TSS,TSSDF,SSWDF,SSWMS = calcTSS(SSB,SSW,SSBDF,SSBMS,sampSizeList)
    FTest = calcFTest(SSBMS,SSWMS)
    outFileInstructions()
    writeFile(SSB,SSBDF,SSBMS,SSW, TSS,TSSDF,SSWDF,SSWMS,FTest,sampSizeList,meanList,varList,grandMean)
    endProgram()

def title():
    title = " ANOVA "
    print(title.center(50))
    input("Please press <Enter> to select CSV data file: ")

def openFile():
    # open file with tkinter GUI
    inFile = open(askopenfilename(), "r")
    return inFile

def readFile(inFile):
    numCols = int(input("Please enter the total number of columns to be analyzed then press <Enter>: "))
    colList = []
    for i in range(numCols):
        colNum = input("Please enter the column number then press <Enter>: ")
        colList.append(colNum)
    print(colList)
    # read csv cols
    df = pd.read_csv(inFile)
    inFile.close

    return df,numCols,colList

def getMean(df,colList):
    meanList = []
    for i in range(len(colList)):
        meanVal = df[colList[i]].mean()
        meanList.append(meanVal)
    return meanList

def getVar(df,colList):
    varList = []
    for i in range(len(colList)):
        varVal = df[colList[i]].var()
        varList.append(varVal)
    return varList

def getSampSize(df,colList):
    sampSizeList = []
    for i in range(len(colList)):
        sampSizeList.append(len(df[colList[i]]))
    return  sampSizeList

def getGrandMean(meanList):
    grandMean = numpy.mean(meanList)
    return grandMean

def calcSSB(grandMean,meanList,varList,sampSizeList,numCols):
    totSSB = 0
    for i in range(len(meanList)):
        SSB = sampSizeList[i]*pow((meanList[i]*grandMean),2)
        totSSB = SSB+totSSB
    SSBDF = numCols - 1
    SSBMS = totSSB/SSBDF

    return totSSB,SSBDF,SSBMS

def calcSSW(varList,sampSizeList):
    totSSW = 0
    for i in range(len(varList)):
        SSW = varList[i]*(sampSizeList[i]-1)
        totSSW = SSW+totSSW
    return totSSW

def calcTSS(SSB,SSW,SSBDF,SSBMS,sampSizeList):
    TSS = SSB+SSW
    TSSDF = numpy.sum(sampSizeList) -1
    SSWDF = TSSDF - SSBDF
    SSWMS = SSW/SSWDF
    return TSS, TSSDF,SSWDF,SSWMS

def calcFTest(SSBMS,SSWMS):
    FTest = SSBMS/SSWMS
    return FTest

def outFileInstructions():
    input("Please press <Enter> to create your ANOVA file: ")

def writeFile(SSB,SSBDF,SSBMS,SSW, TSS,TSSDF,SSWDF,SSWMS,FTest,sampSizeList,meanList,varList,grandMean):
    outFileName = asksaveasfilename()
    outFile = open(outFileName, "w")

    title = " ANOVA "
    print(title.center(75),file=outFile)

    print(tabulate([
        ["Sample Mean", meanList],
        ["Sample Variance", varList],
        ["Sample Size", sampSizeList]
    ],
        headers=["Statistic"],
        tablefmt='grid'), file=outFile)

    print(tabulate([
        ["Between Samples",round(SSB,2),round(SSBDF,2),round(SSBMS,2),round(FTest,2)],
        ["Within Samples", round(SSW, 2), round(SSWDF, 2), round(SSWMS, 2)],
        ["Total", round(TSS, 2), round(TSSDF, 2)]
    ],
        headers=["Source","Sum of Squares","df","Mean Square","F Test"],
        tablefmt='grid'),file=outFile)

    outFile.close()

def endProgram():
    input("\nPress <Enter> to exit the program")

main()
