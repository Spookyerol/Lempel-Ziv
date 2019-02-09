# -*- coding: utf-8 -*-
"""
Created on Mon Feb  4 19:19:47 2019

@author: Erdal Guclu
"""
from bitarray import bitarray

def encode(msg, W, L):
    bitStr = msg
    i = 0
    encoded = bitarray()
    encodedStr = []
    while(i < len(bitStr)):
        codedChar = codeChar(bitStr, i, W, L)
        encodedStr.append(codedChar[1])
        for j in range(len(codedChar)-1):
            encoded += bin(int(codedChar[1][j]))[2:].zfill(8)
        encoded += bin(ord(codedChar[-1][-1]))[2:].zfill(8)
        if(i == len(bitStr)):
            break
        else:
            i = codedChar[0]
    print(encodedStr)
    return encoded

def codeChar(bitStr, i, W, L):
    char = bitStr[i]
    if(i == 0):
        i = i + 1
        return i, (0, 0, char)
    elif(i <= W):
        windowStart = 0
    else: 
        windowStart = i - W
    if(len(bitStr)-i <= L):
        bufferEnd = len(bitStr)
    else:
        bufferEnd = i + L
    if(bitStr[i] in bitStr[windowStart:i]):
        match = getLongestPrefix(bitStr[windowStart:i], bitStr[i:bufferEnd])
        i = i + match[1]
        if(i > len(bitStr)-1):
            return i, (match[0], match[1], "-")
        char = bitStr[i]
        i = i + 1
        return i, (match[0], match[1], char)
    else: #Have not encountered character before
        i = i + 1
        return i, (0, 0, char)
    
def getLongestPrefix(window, buffer):
    curPrefix = ""
    longestPrefix = (-1, -1)
    d = len(window)
    i = 0
    j = 0
    mark = -1
    while(j < len(window)):
        isNext = False
        while(i < len(buffer) and buffer[i] == window[j]):
            if(curPrefix == ""):
                mark = j  
            curPrefix += window[j]
            j = j + 1
            i = i + 1
            isNext = True
            if(j == len(window)):
                break
        if(len(curPrefix) >= longestPrefix[-1]):
            d = len(window) - mark
            longestPrefix = (d, len(curPrefix))
            curPrefix = ""
            i = 0
        if(not isNext):
            curPrefix = ""
            i = 0
            j = j + 1
    return longestPrefix

def decode(codeArr):
#    with open('somefile.bin', 'rb') as fh:
#    a.fromfile(fh)
    i = 0
    bitStr = ""
    while(codeArr[i][-1] != "-"):
        code = codeArr[i]
        if(code[1] == 0):
            bitStr += code[-1]
        else:
            j = len(bitStr) - code[0]
            for k in range(code[1]):
                bitStr += bitStr[j]
                j = j + 1
            bitStr += code[-1]
        i = i + 1
        try:
            if(codeArr[i][-1] == "-"):
                code = codeArr[i]
                j = len(bitStr) - code[0]
                for k in range(code[1]):
                    bitStr += bitStr[j]
                    j = j + 1
        except(IndexError):
            break
    bitStr = bitarray(bitStr)
    decoded = bitStr.tobytes().decode("utf-8")
    print(decoded)
    return decoded

def compressFile(fileName, W, L, infWindow):
    with open(fileName, encoding="utf8") as file:
        content = file.read()
    print(content)
    if(infWindow):
        W = len(content)
        L = len(content)
    encoded = encode(content, W, L)
    binaryName = fileName.split(".")[0] + ".bin"
    with open(binaryName, "wb") as file:
        encoded.tofile(file)
        file.flush()
    print("File " + fileName + " compressed.")
    
compressFile("text1.txt", 16, 8, True)





















