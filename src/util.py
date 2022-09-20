''' 
--------------------------------------
  Universidad del Valle de Guatemala
  Author: Diego Cordova - 20212

  util.py
  - auxiliar functions used in 
    implementation of bmp writter
  
  Last modified (yy-mm-dd): 2022-07-17
--------------------------------------
'''

import struct

def char(c):
  '''Package information into char (1 byte)'''
  return struct.pack('=c', c.encode('ascii'))

def word(w):
  '''Package information into word (2 bytes)'''
  return struct.pack('=h', w)

def dword(d):
  '''Package information into doubble word (4 bytes)'''
  return struct.pack('=l', d)

def color(r, g, b, normalized=True):
  '''Package rgb color information into bytes for bmp immages'''
  if normalized:
    if r < 0 or r > 1: raise Exception('invalid color:', [r, g, b])
    if g < 0 or b > 1: raise Exception('invalid color:', [r, g, b])
    if g < 0 or b > 1: raise Exception('invalid color:', [r, g, b])

    r = int(255 * r)
    g = int(255 * g)
    b = int(255 * b)
    
  return bytes([b, g, r])
