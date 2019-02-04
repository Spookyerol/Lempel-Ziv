# -*- coding: utf-8 -*-
"""
Created on Mon Feb  4 19:19:47 2019

@author: Erdal Guclu
"""
from bitarray import bitarray



def encode(msg, W, L):
    bits = bitarray()
    msg = msg.zfill(8)
    print(msg)
    for char in msg:
        bits += bin(ord(char))[2:]
    bits = bits
    print(bits)
    i = 0
    while(len(bits) < 0):
        for j in range(W):
            for k in range(L):
                i = i
        
    
encode("abracadabra", 8, 4);

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