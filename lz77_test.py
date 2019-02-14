# -*- coding: utf-8 -*-
"""
Created on Wed Feb 13 23:38:03 2019

@author: Erdal Guclu
"""
import lz77 as lz77 #Imports the source code
from bitarray import bitarray
from sys import argv
import time
import os

fileName = argv[1]
W = int(argv[2]) - 1
L = int(argv[3]) - 1

dBits = 8 #This global variable allows one to determine the amount of bytes to be used to encode distance
lBits = 8 #This global variable allows one to determine the amount of bytes to be used to encode length

#params
#   n: number of repeats per experiment
#   fileName: name of the input file including extension
#   W: window size in bytes
#   L: lookahead buffer size in bytes
#   willPrint: If true prints results to console, else will return test values instead.
#Performs a single experiment on a file with given parameters.
def experiment(n, fileName, W, L, willPrint):
    global dBits
    global lBits
    compTimes = []
    decompTimes = []
    sizeComp = -1
    sizeUncomp = -1     
    if(W > 2**dBits - 1 or L > 2**lBits): #Checks if the window and buffer size fit into the encoding format.  
        W = 2**dBits - 1
        L = 2**lBits - 1
        print("The window and buffer sizes were above the maximum for the no. of bytes used to encode distance and length so have been adjusted to: " + str(2**dBits - 1) + " and " + str(2**lBits - 1) + " respectively.")  
    with open("originals/" + fileName, "rb") as file:
        content = file.read()
    decodeContent = bitarray()
    for i in range(n):
        start  = time.time()
        lz77.encode(fileName, content, W, L)
        endComp = time.time()
        compTimes.append(endComp - start)
        start = time.time()
        decodeContent = lz77.decode(fileName)
        endDecomp = time.time()
        decompTimes.append(endDecomp - start)   
    with open("decompressed/" + fileName.split(".")[0] + "Decomp" + "." + fileName.split(".")[1], "wb") as file: #Write decompressed content to file
        decodeContent.tofile(file) 
    sizeComp = os.path.getsize("./binaries/" + fileName.split(".")[0] + ".bin") #Get the sizes of files
    sizeUncomp = os.path.getsize("./originals/" + fileName)
    timeCompress = sum(compTimes) / len(compTimes) #Find average times
    timeDecompress = sum(decompTimes) / len(decompTimes)
    if(not willPrint): #Will return instead of printing
        encodeData = "Across " + str(n) +  " tests it took " + str(timeCompress) + " seconds to compress " + fileName + " from " + str(sizeUncomp) + " to " + str(sizeComp) + " bytes\n"
        decodeData = "Across " + str(n) +  " tests it took " + str(timeDecompress) + " seconds to decompress " + fileName.split(".")[0] + ".bin\n"
        compData = "The compression ratio is: " + str(sizeUncomp / sizeComp) + "\n"
        return (encodeData, decodeData, compData)
    else:
        print("Window size: " + str(W) + "Buffer size: " + str(L) + "\n")
        print("Across " + str(n) +  " tests it took " + str(timeCompress) + " seconds to compress " + fileName + " from " + str(sizeUncomp) + " to " + str(sizeComp) + " bytes\n")
        print("Across " + str(n) +  " tests it took " + str(timeDecompress) + " seconds to decompress " + fileName.split(".")[0] + ".bin\n")
        print("The compression ratio is: " + str(sizeUncomp / sizeComp) + "\n")

#params
#   n: number of repeats per experiment
#   fileName: name of the input file including extension
#   W: window size in bytes
#   L: lookahead buffer size in bytes
#Performs a set of experiments on a given file and writes the results to a text file.
def testFile(n, fileName, W, L):
    global dBits
    global lBits
    file = open("TestData.txt", "a+", encoding = "utf-8")
    file.write(fileName + "\n")
    while(W <= 8191 and L <= 255):
        print("next", W, L)
        dBits = 8
        lBits = 8
        if(W > 255): #The testing algorithm supports upto 5 bytes large tuples however this can be changed to higher values since the lz77 source can handle it
            dBits = 16
        if(L > 255):
            lBits = 16
        data = experiment(n, fileName, W, L, False)
        file.write("Window size: " + str(W) + "Buffer size: " + str(L) + "\n")
        file.write("Bytes used to encode a tuple: " + str((dBits / 8) + (lBits / 8) + 1) + "\n")
        file.write(data[0])
        file.write(data[1])
        file.write(data[2] + "\n")
        W = W + 768 #The expression here can be modified in many ways to create varying sequences of data
        file.flush()
    file.close()
    
experiment(5, fileName, W, L, True) #You can comment and uncomment these lines to choose which testing method to use
#testFile(5, fileName, W, L)