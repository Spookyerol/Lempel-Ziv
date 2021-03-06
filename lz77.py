# -*- coding: utf-8 -*-
"""
Created on Mon Feb 4 19:19:47 2019

@author: Erdal Guclu
"""
from bitarray import bitarray

dBits = 8 #This global variable allows one to determine the amount of bytes to be used to encode distance
lBits = 8 #This global variable allows one to determine the amount of bytes to be used to encode length

#params:
#   fileName: name of file being encoded including extension
#   content: All bytes of file to be compressed
#   W: window size in bytes
#   L: lookahead buffer size in bytes
#The main encode function that turns content into a binary bitarray and writes it to a .bin file
def encode(fileName, content, W, L):
    global dBits
    global lBits
    i = 0
    encoded = bitarray()
    while(i < len(content)):
        codedChar = codeChar(content, i, W, L)
        #.zfill(n*8) makes sure each value is encoded into n bytes
        encoded += bin(codedChar[1][0])[2:].zfill(dBits) #distance d
        encoded += bin(codedChar[1][1])[2:].zfill(lBits) #length l
        try:
            encoded += bin(codedChar[-1][-1])[2:].zfill(8)
        except(TypeError): #Have reached the last empty string character
            encoded += bin(0)[2:].zfill(8) #Add utf-8 "NULL" end marker
        if(i == len(content)):
            break
        else:
            i = codedChar[0] #set i to current position in input
    binaryName = fileName.split(".")[0] + ".bin"
    with open("binaries/" + binaryName, "wb") as file:
        encoded.tofile(file)
    return encoded

#params:
#   content: All bytes of file to be compressed
#   i: pointer to byte currently being encoded
#   W: window size
#   L: lookahead buffer size
#This is a function that encodes byte i in content
def codeChar(content, i, W, L):
    char = content[i]
    if(i <= W): #We are near the start of the bitStr so window starts at index 0
        windowStart = 0
    else: #We can use the full window size W 
        windowStart = i - W
    if(len(content)-i <= L): #We are near the end of bitStr so buffer has to end at final index 
        bufferEnd = len(content)
    else: #We can use the full buffer size L
        bufferEnd = i + L
    match = getLongestPrefix(content[windowStart:i], content[i:bufferEnd])
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
#   buffer: bytes including the byte being encoded and bytes after it
#This function finds the longest substring in the window and buffer that matches with the first l characters of the buffer
def getLongestPrefix(window, buffer):
    l = len(buffer)
    longestPrefix = window.rfind(buffer[0:l])
    while(l > 0):
        if(len(window) == 5):
            pass
        if(longestPrefix != -1): #If there has been a match we no longer have to keep searching
            i = 0
            sl = l #the self-referential match length
            if(longestPrefix+sl == len(window)): #Checks if there has been a self-referential match
                try:
                    while(buffer[i] == buffer[sl + i]):
                        l = l + 1
                        i = i + 1
                except(IndexError): #This means that we have reached the end of the input so it is safe to ignore
                    pass
            break
        l = l - 1
        longestPrefix = window.rfind(buffer[0:l])
    return longestPrefix, l

#params:
#   fileName: name of the binary file to be compressed including the extension
#Takes and encoded array and recreates the orginal content
def decode(fileName):
    global dBits
    global lBits
    decodeContent = bitarray()
    with open("binaries/" + fileName.split(".")[0] + '.bin', 'rb') as file: #Read binary
        byteCount = (dBits / 8) + (lBits / 8) + 1
        binContent = file.read(int(byteCount))
        while(binContent):
            code = (binContent[0:int(dBits / 8)], binContent[int(dBits / 8):int(dBits / 8) + int(lBits / 8)], binContent[-1])
            if(code[1] == 0):
                decodeContent += bin(code[-1])[2:].zfill(8)
            else:
                j = len(decodeContent) - (int.from_bytes(code[0], byteorder='big') * 8) #points to the first bit that needs to be copied
                for k in range((int.from_bytes(code[1], byteorder='big'))): #Copy the bytes that need to be copied
                    decodeContent += decodeContent[j:j + 8]
                    j = j + 8 #next byte to copy
                decodeContent += bin(code[-1])[2:].zfill(8)
            binContent = file.read(int(byteCount))
    decodeContent = decodeContent[0:len(decodeContent)-8] #Remove end marker 
    return decodeContent