# -*- coding: utf-8 -*-
"""
Created on Mon Feb  4 19:19:47 2019

@author: Erdal Guclu
"""
from bitarray import bitarray


#params:
#   content: full content of file to be compressed
#   W: window size
#   L: lookahead buffer size
#The main encode function that turns content into a binary bitarray
def encode(content, W, L):
    i = 0
    encoded = bitarray()
    while(i < len(content)):
        codedChar = codeChar(content, i, W, L)
        #.zfill(8) makes sure each value/character is encoded into a single byte
        encoded += bin(int(codedChar[1][0]))[2:].zfill(8) #distance d
        encoded += bin(int(codedChar[1][1]))[2:].zfill(8) #length l
        try:
            encoded += bin(ord(codedChar[-1][-1]))[2:].zfill(8)
        except(TypeError): #Have reached the last empty string character
            encoded += bin(0)[2:].zfill(8) #Add utf-8 "NULL" end marker
        if(i == len(content)):
            break
        else:
            i = codedChar[0] #set i to current position in input
    return encoded

#params:
#   content: full content of file to be compressed
#   i: pointer to character currently being encoded
#   W: window size
#   L: lookahead buffer size
#This is a function that encodes character i in content
def codeChar(content, i, W, L):
    char = content[i]
    if(i == 0):
        i = i + 1
        return i, (0, 0, char)
    elif(i <= W): #We are near the start of the bitStr so window starts at index 0
        windowStart = 0
    else: #We can use the full window size W 
        windowStart = i - W
    if(len(content)-i <= L): #We are near the end of bitStr so buffer has to end at final index 
        bufferEnd = len(content)
    else: #We can use the fill buffer size L
        bufferEnd = i + L
    if(content[i] in content[windowStart:i]): #The current character was seen in the window
        match = getLongestPrefix(content[windowStart:i], content[i:bufferEnd])
        i = i + match[1]
        if(i > len(content)-1): #We are encoding the ending character
            return i, (match[0], match[1], "") #Empty string will get turned into a marker
        char = content[i]
        i = i + 1
        return i, (match[0], match[1], char)
    else: #Have not encountered character before
        i = i + 1
        return i, (0, 0, char)
#params:
#   window: substring preceding the character being encoded
#   buffer: substring including the character being encoded as characters after it
#This function finds the longest substring in the window that matches with the first l characters of the buffer
def getLongestPrefix(window, buffer):
    curPrefix = ""
    longestPrefix = (-1, -1)
    d = len(window) #distance
    i = 0 #pointer for buffer
    j = 0 #pointer for window
    mark = -1
    while(j < len(window)):
        isNext = False #If we break into the while loop below j will already point to the next character so we only increment j if this is false
        while(i < len(buffer) and buffer[i] == window[j]):
            if(curPrefix == ""): #We mark the index at which the prefix starts
                mark = j  
            curPrefix += window[j]
            j = j + 1
            i = i + 1
            isNext = True
            if(j == len(window)):
                break
        if(len(curPrefix) >= longestPrefix[-1]): #We check if the current prefix is longer than the last
            d = len(window) - mark
            longestPrefix = (d, len(curPrefix))
            curPrefix = "" #Reset the current prefix so we can move on to the next
            i = 0
        if(not isNext): #Only executes if we did not break into the inner while loop
            curPrefix = ""
            i = 0
            j = j + 1
    return longestPrefix

#params:
#   codeArr: array of 3-tuples storing (distance, length, character)
#Takes and encoded array and recreates the orginal content
def decode(codeArr):
    i = 0
    content = ""
    while(codeArr[i][-1] != ""):
        code = codeArr[i]
        if(code[1] == 0):
            content += code[-1]
        else:
            j = len(content) - code[0]
            for k in range(code[1]):
                content += content[j]
                j = j + 1
            content += code[-1]
        i = i + 1
        try:
            if(codeArr[i][-1] == ""): #Check if we have reached the "NULL" end marker
                code = codeArr[i]
                j = len(content) - code[0]
                for k in range(code[1]):
                    content += content[j]
                    j = j + 1
        except(IndexError): #This means that we have reached the end
            break
    return content

#params:
#   fileName: name of the file to be compressed including the extension
#   W: window size
#   L: lookahead buffer size
#   infWindow: bool that if true overrides W and L and uses "infinite" buffer and window size
#This is mainly a wrapper function for encode that reads the content of a file and passes it through
def compressFile(fileName, W, L, infWindow):
    with open(fileName, encoding="utf8") as file:
        content = file.read()
    if(infWindow):
        W = len(content)
        L = len(content)
    encoded = encode(content, W, L)
    binaryName = fileName.split(".")[0] + ".bin"
    with open(binaryName, "wb") as file:
        encoded.tofile(file)
        file.flush()
    print("File " + fileName + " compressed.")

#params:
#   fileName: name of the binary file to be compressed excluding the extension
#This is mainly a wrapper function for decode that reads the content of the correspinding binary and passes it through  
def decompressFile(fileName):
    decoded = []
    binary = bitarray()
    with open(fileName + '.bin', 'rb') as file: #Read binary
        binary.fromfile(file)
    binary = binary.to01() #Turn bitarray into string of binary
    for j in range(0, len(binary), 24): #Reads the string 3 bytes at a time
        triBytes = binary[j:j + 24]
        decoded.append((int(triBytes[0:8], 2), int(triBytes[8:16], 2), chr(int(triBytes[16:24], 2)))) #Creates an array of triplets to pass into decode
    decompressed = decode(decoded)
    decompressed = decompressed[0:-1] #Remove the ending marker
    with open("decompressed.txt", "w+") as file: #Write decompressed content to file
        file.write(decompressed)
        file.flush()
    print("File " + fileName + " decompressed.")
    
compressFile("Lempel-Ziv_Compressor.py", 128, 128, False)
decompressFile("Lempel-Ziv_Compressor")




















