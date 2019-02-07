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
        #print(codedChar[1])
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
        #print(i, bitStr[i], bitStr[windowStart:i])
        while(bitStr[i] != bitStr[windowStart]): #Find the first matching character in window
            windowStart += 1
        d = i - windowStart
        l += 1
        if(i == len(bitStr)-1): #Last character reached
            return i, (d, l, "-")
        while(bitStr[i + l] == bitStr[windowStart + l] and i + l < bufferEnd): #Continue matching characters between window and buffer
            print(bitStr[i + l])
            l += 1
            print(bitStr[i + l])
        i = i + l + 1
        char = bitStr[i]
        print(i, (d, l, char))
        return i, (d, l, char)
    else: #Have not encountered character before
        i = i + 1
        return i, (0, 0, char)
    
def decode(codeArr):
    i = 0
    bitStr = ""
    while(codeArr[i][-1] != "-"):
        #print(codeArr[i])
        code = codeArr[i]
        d = code[0]
        lookBack = 0
        it = 0
        while(d > 0):
            it = it + 1
            d = d - codeArr[i - it][1] - 1
            lookBack = lookBack + 1
        it = 1
        j = i - lookBack
        #print(code)
        #print(j, i, code[0], lookBack)
        if(code[1] == 0):
            #print(j, code)
            bitStr += code[-1]
        elif(code[1] == 1):
            #print(-code[0], -code[0] + code[1])
            #print(code, bitStr, bitStr[-code[0]:-code[0] + code[1]])
            bitStr += bitStr[-1]
            bitStr += code[-1]
        else:
            subStr = bitStr[-code[0]:-code[0] + code[1]]
            #print(-code[0], -code[0] + code[1])
            #print(code, bitStr, bitStr[-code[0]:-code[0] + code[1]])
            bitStr += subStr
        i = i + 1
        if(codeArr[i][-1] == "-"):
            code = codeArr[i]
            #print(code)
            j = i - lookBack
            for k in range(code[1]):
                prevCode = codeArr[j]
                bitStr += prevCode[-1]
                j = j + 1
    
    print(bitStr)
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