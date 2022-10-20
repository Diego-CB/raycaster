''' 
--------------------------------------
  Universidad del Valle de Guatemala
  Author: Diego Cordova - 20212

  Op_bmp.py
  - Utilities for reading and writting
    of bmp files

  Last modified (yy-mm-dd): 2022-08-08
--------------------------------------
'''

from .util import *

# Writing of BMP

def pixel_header(file, width, height):
  ''' Writes Pixel Header for the file f'''

  # -------- File header --------
  
  # BM
  file.write(char('B'))
  file.write(char('M'))

  # Tamano del file Header + Tamano del Image Header + tamano de la imagen
  file.write(dword(14 + 40 + width * height * 3))

  file.write(dword(0)) # 4 bytes vacios (dword)
  file.write(dword(14 + 40)) # Tamano del file Header + Tamano del Image Header

  # -------- Image header --------
  
  file.write(dword(40)) # Tamano del Image Header
  file.write(dword(width)) # Ancho de la imagen
  file.write(dword(height)) # Largo de la imagen
  file.write(word(1)) # un word con un 1 (2 bytes)
  file.write(word(24)) # un word con un 24 (2 bytes)
  file.write(dword(0)) # 4 bytes vacios (dword)
  file.write(dword(width * height * 3)) # tamano de la imagen
  
  # 4 dwords vacios: 4*4 bytes
  file.write(dword(0))
  file.write(dword(0))
  file.write(dword(0))
  file.write(dword(0))

def write_bmp(filename, frameBuffer:list[list[bytes]]):
  '''
    Writes a bmp file with the 
    color information contained
    in the framebuffer
  '''

  width = len(frameBuffer[0])
  height = len(frameBuffer)
  file = open(filename, 'bw')
  pixel_header(file, width, height)

  for y in range(height):
    for x in range(width):
      file.write(frameBuffer[y][x])

  file.close()

def z_write(filename, zBuffer, scale):
  '''
    Writes a bmp file with the 
    color information contained
    in the zBuffer
  '''

  width = len(zBuffer[0])
  height = len(zBuffer)
  f = open(filename, 'bw')
  pixel_header(f, width, height)

  for y in range(width):
    for x in range(height):
      z = zBuffer[y][x]
      z = 0 if z < 0 else z
      z = z / (scale * 3)
      z = 1 if z > 1 else z
      z_color = color(z, z, z)
      f.write(z_color)

  f.close
