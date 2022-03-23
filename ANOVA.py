import csv,tkinter,math,numpy
import pandas as pd
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfilename
from tabulate import tabulate

def main():
    endAct = 1
    while endAct != 0:
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
        endAct = endProgram()

def title():
    print("ANOVA")
    input("Press <Enter> to select CSV data file... ")

def openFile():
    # open file with tkinter GUI
    inFile = open(askopenfilename(), "r")
    return inFile

def readFile(inFile):
    numCols = int(input("Enter the number of samples then press <Enter>: "))
    colList = []
    for i in range(numCols):
        colNum = input("Specify the sample number then press <Enter>: ")
        colList.append(colNum)
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
    input("Press <Enter> to create ANOVA file... ")

def writeFile(SSB,SSBDF,SSBMS,SSW, TSS,TSSDF,SSWDF,SSWMS,FTest,sampSizeList,meanList,varList,grandMean):
    outFileName = asksaveasfilename()
    outFile = open(outFileName, "w")

    headerList = []
    for i in range(len(meanList)):
        headerVal = str(i+1)
        headerList.append(headerVal)
    headerList.insert(0, "Statistics")
    meanList.insert(0, "Sample Mean")
    varList.insert(0, "Sample Variance")
    sampSizeList.insert(0, "Sample Size")
    statTable = [meanList,varList,sampSizeList]

    print("Summary of Data",file=outFile)
    print(tabulate(statTable,headers=headerList,tablefmt='grid',floatfmt='0.2f'),file=outFile)

    print("ANOVA Table",file=outFile)
    print(tabulate([
        ["Between Samples",round(SSB,2),round(SSBDF,2),round(SSBMS,2),round(FTest,2)],
        ["Within Samples", round(SSW, 2), round(SSWDF, 2), round(SSWMS, 2)],
        ["Total", round(TSS, 2), round(TSSDF, 2)]
    ],
        headers=["Source","SS","df","MS","F Test"], tablefmt='grid',floatfmt='0.2f'),file=outFile)

    outFile.close()

def endProgram():
    endAct = int(input("\nSuccessfully created ANOVA file\n<1> Restart <0> Exit "))
    return endAct
main()
