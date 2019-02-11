# -*- coding: utf-8 -*-
"""
Created on Mon Feb 4 19:19:47 2019

@author: Erdal Guclu
"""
from bitarray import bitarray

bitCount = 16 #This global variable allows one to determine the amount of bytes to be used to encode a single number (for d and l)

#params:
#   content: full content of file to be compressed
#   W: window size
#   L: lookahead buffer size
#The main encode function that turns content into a binary bitarray and writes it to a .bin file
def encode(fileName, W, L):
    global bitCount
    with open(fileName, "rb") as file:
        content = file.read()
    i = 0
    encoded = bitarray()
    while(i < len(content)):
        codedChar = codeChar(content, i, W, L)
        #.zfill(n*8) makes sure each value is encoded into n bytes
        encoded += bin(codedChar[1][0])[2:].zfill(bitCount) #distance d
        encoded += bin(codedChar[1][1])[2:].zfill(bitCount) #length l
        try:
            encoded += bin(codedChar[-1][-1])[2:].zfill(8)
        except(TypeError): #Have reached the last empty string character
            encoded += bin(0)[2:].zfill(8) #Add utf-8 "NULL" end marker
        if(i == len(content)):
            break
        else:
            i = codedChar[0] #set i to current position in input
    binaryName = fileName.split(".")[0] + ".bin"
    with open(binaryName, "wb") as file:
        encoded.tofile(file)
        file.flush()
    return encoded

#params:
#   content: full content of file to be compressed
#   i: pointer to byte currently being encoded
#   W: window size
#   L: lookahead buffer size
#This is a function that encodes byte i in content
count = 0

def codeChar(content, i, W, L):
    global count
    char = content[i]
    if(i <= W): #We are near the start of the bitStr so window starts at index 0
        windowStart = 0
    else: #We can use the full window size W 
        windowStart = i - W
    if(len(content)-i <= L): #We are near the end of bitStr so buffer has to end at final index 
        bufferEnd = len(content)
    else: #We can use the full buffer size L
        bufferEnd = i + L
    #print(len(content[windowStart:i]))
    match = getLongestPrefix(content[windowStart:i], content[i:bufferEnd], i)
    if(count < 8):
                print(content[windowStart:i])
                print(content[i:bufferEnd])
                print(content[i:bufferEnd][0:match[1]],  content[i:bufferEnd][0], match[1], len(content[windowStart:i]) - match[0], i)
    count += 1
    if(match[0] != -1): #A match has been found
        d = len(content[windowStart:i]) - match[0]
        i = i + match[1]
        if(i > len(content)-1): #We are encoding the ending character
            return i, (d, match[1], "") #Empty string will get turned into a marker
        char = content[i]
        i = i + 1
        return i, (d, match[1], char)
    else: #A match was not found
        i = i + 1
        return i, (0, 0, char)
    
    
#params:
#   window: substring preceding the character being encoded
#   buffer: substring including the character being encoded as characters after it
#This function finds the longest substring in the window that matches with the first l characters of the buffer
def getLongestPrefix(window, buffer, i):
    global count
    global bitCount
    l = len(buffer)
    search = window + buffer
    #print(window, buffer)
    longestPrefix = window.rfind(buffer[0:l])
    while(l > 0):
        if(longestPrefix != -1):
            break
        l = l - 1
        longestPrefix = window.rfind(buffer[0:l])
#    i = 0
#    if(longestPrefix != -1 and i < len(buffer) - 1 and buffer[i] == buffer[i+1]): #Check for self-referential matches
#        l = l + 1
#        i = i + 1
    return longestPrefix, l

#params:
#   fileName: name of the binary file to be compressed including the extension
#Takes and encoded array and recreates the orginal content
def decode(fileName):
    global bitCount
    global count
    count = 0
    decodeContent = bitarray()
    with open(fileName.split(".")[0] + '.bin', 'rb') as file: #Read binary
        byteCount = (bitCount / 8) * 2 + 1
        binContent = file.read(int(byteCount))
        lengthNums = int(bitCount / 8) #Computes the number of bytes that each int value is encoded as7
        while(binContent):
            code = (binContent[0:lengthNums], binContent[lengthNums:lengthNums*2], binContent[-1])
            if(count <= 7):
                print(int.from_bytes(code[0], byteorder='big'), int.from_bytes(code[1], byteorder='big'), code[-1])
            count += 1
            if(code[1] == 0):
                decodeContent += bin(code[-1])[2:].zfill(8)
            else:
                if(count == 134):
                    print(len(decodeContent), int.from_bytes(code[0], byteorder='big'))
                    pass
                j = len(decodeContent) - (int.from_bytes(code[0], byteorder='big') * 8) #points to the first bit that needs to be copied
                for k in range(code[1][-1]): #Copy the bytes that need to be copied
                    decodeContent += decodeContent[j:j + 8]
                    j = j + 8 #next byte to copy
                decodeContent += bin(code[-1])[2:].zfill(8)
            binContent = file.read(int(byteCount))
    decodeContent = decodeContent[0:len(decodeContent)-8] #Remove end marker 
    print(len(decodeContent) / 8)
    with open(fileName.split(".")[0] + "Decomp" + "." + fileName.split(".")[1], "wb") as file: #Write decompressed content to file
        decodeContent.tofile(file)
        file.flush()
    return decodeContent

def calc_bitCount(W):
    pass

"""
These imports are for the testing/experimentation system
"""
import time
import os

def experiment(n, fileName, W, L):
    global bitCount
    compTimes = []
    decompTimes = []
    sizeComp = -1
    sizeUncomp = -1     
    if(W > 2**bitCount - 1):
        W = 2**bitCount - 1
        L = 2**bitCount - 1
        print("The window and buffer sizes were above the maximum for the no. of bytes used to encode distance and length so have been adjusted to: " + str(2**bitCount - 1))
    for i in range(n):
        print(i)
        start  = time.time()
        encode(fileName, W, L)
        endComp = time.time()
        compTimes.append(endComp - start)
        start = time.time()
        decode(fileName)
        endDecomp = time.time()
        decompTimes.append(endDecomp - start)
    sizeComp = os.path.getsize("./" + fileName.split(".")[0] + ".bin")
    sizeUncomp = os.path.getsize("./" + fileName)
    timeCompress = sum(compTimes) / len(compTimes)
    timeDecompress = sum(decompTimes) / len(decompTimes)
    print("Across " + str(n) +  " tests it took " + str(timeCompress*1000) + " miliseconds to compress " + fileName + " from " + str(sizeUncomp) + " to " + str(sizeComp) + " bytes")
    print("Across " + str(n) +  " tests it took " + str(timeDecompress*1000) + " miliseconds to decompress " + fileName.split(".")[0] + ".bin")
    print("The compression ratio is: " + str(sizeUncomp / sizeComp))


#experiment(5, "htbk26report.pdf", 255, 255)
encode("text1.txt", 300, 300)
decode("text1.txt")