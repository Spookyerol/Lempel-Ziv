# -*- coding: utf-8 -*-
"""
Created on Mon Feb  4 19:19:47 2019

@author: Erdal Guclu
"""
from bitarray import bitarray

def encode(msg, W, L):
    bitStr = ""
    for char in msg:
        bitStr += bin(ord(char))[2:].zfill(8)
    print(bitStr)
    i = 0
    encoded = []
    while(i <= len(bitStr)-1):
        codedChar = codeChar(bitStr, i, W, L)
        encoded.append(codedChar[1])
        if(i == len(bitStr)-1):
            break
        else:
            i = codedChar[0]
    print(encoded)
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
        bufferEnd = len(bitStr) - 1
    else:
        bufferEnd = i + L
    d = 0
    l = 0
    if(bitStr[i] in bitStr[windowStart:i]): 
        while(bitStr[i] != bitStr[windowStart]):
            windowStart += 1
        d = i - windowStart
        l += 1
        if(i == len(bitStr)-1):
            return i, (d, l, "-")
        while(bitStr[i + l] == bitStr[windowStart + l] and i + l < bufferEnd):
            l += 1
        i = i + l
        char = bitStr[i]
        return i, (d, l, char)
    else:
        i = i + 1
        return i, (0, 0, char)
    
def decode(codeArr):
    i = 0
    j = i
    bitStr = ""
    while(codeArr[i][-1] != "-"):
        #print(codeArr[i])
        code = codeArr[i]
        j = i - code[0]
        #print(j)
        if(code[1] == 0):
            bitStr += code[-1]
        else:
            for k in range(code[1]):
                prevCode = codeArr[j]
                bitStr += prevCode[-1]
                j = j + 1
            bitStr += code[-1]
        i = i + 1
        if(codeArr[i][-1] == "-"):
            code = codeArr[i]
            j = i - code[0]
            for k in range(code[1]):
                prevCode = codeArr[j]
                bitStr += prevCode[-1]
                j = j + 1
    
    #print(bitStr)
    #bits.tobytes().decode('utf-8')
        
decode(encode("abracadabra", 8, 8))

"""
while input is not empty do
    prefix := longest prefix of input that begins in window
    
    if prefix exists then
        i := distance to start of prefix
        l := length of prefix
        c := char following prefix in input
    else
        i := 0
        l := 0
        c := first char of input
    end if
    
    output (i, l, c)
    
    s := pop l+1 chars from front of input
    discard l+1 chars from front of window
    append s to back of window
"""