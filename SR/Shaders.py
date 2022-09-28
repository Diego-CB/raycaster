''' 
--------------------------------------
  Universidad del Valle de Guatemala
  Author: Diego Cordova - 20212

  Shaders.py
  - implementation of shaders

  Last modified (yy-mm-dd): 2022-09-17
--------------------------------------
'''

from .MStructs.Vector import V3
from .util import color
from .Render import Render
from math import sqrt

def __getIntensity(L:V3, baricentric:tuple, normals:tuple):
  '''Intensity of light (for gouraud algorithm)'''
  w, u, v = baricentric
  nA, nB, nC = normals
  L = L.normalize()

  iA = nA.normalize() * L
  iB = nB.normalize() * L
  iC = nC.normalize() * L
  return iA * w + iB * u + iC * v

def gouraud(render:Render, **kwargs):
  '''Implementation of gouraud algorithm (shader)'''
  w, u, v = kwargs['bari']
  i = __getIntensity(kwargs['light'], (w, u, v), kwargs['normals'])

  try:
    tA, tB, tC = kwargs['texture_coords']
    if render.texture:
      tx = tA.x * w + tB.x * u + tC.x * v
      ty = tA.y * w + tB.y * u + tC.y * v

      return render.texture.get_color(tx, ty, i)

  except:
    return color(
      round(255 * i),
      round(255 * i),
      round(255 * i),
      normalized=False
    )

def jupiter_shader(render:Render, **kwargs):
  '''Jupiter like texture via shader'''
  i = __getIntensity(kwargs['light'], kwargs['bari'], kwargs['normals'])
  x, y = kwargs['coords']
  w, h = kwargs['size']

  RED = (255, 180, 120)
  DARK = (250, 210, 180)
  CLEAR = (250, 245, 240)

  lines = [
    h * 8/10,
    h * 7.8/10,
    h * 7.65/10,
    h * 7.2/10,
    h * 5.8/10,
    h * 4/10,
    h * 2.5/10,
    h * 2/10
  ]
  a = (w * ((7.2/10) - (5.3/10))) / 2
  b = (lines[6] - lines[7]) / 1.6

  # Lineas
  if y > lines[0]:
    r, g, b = DARK
  
  elif lines[1] < y <= lines[0]:
    r, g, b = CLEAR
  
  elif lines[2] < y <= lines[1]:
    r, g, b = DARK

  elif lines[3] < y <= lines[2]:
    r, g, b = CLEAR
  
  elif lines[4] < y <= lines[3]:
    r, g, b = RED
  
  elif lines[5] < y <= lines[4]:
    r, g, b = CLEAR
 
  elif lines[6] < y <= lines[5]:
    # Mancha: parte alta
    circle:bool = False

    if w * 5.3/10 < x < w * 7.2/10:
      if y <= lines[6] + b:
        offset_x = (w * (5.3/10)) + a
        offset_y = (h * (7.2/10)) + b

        if __checkCoords(a, b, offset_x, offset_y, w, h, x, y):
          circle = True
    
    r, g, b = RED if circle else DARK

  elif lines[7] < y <= lines[6]:
    # Mancha: parte baja
    circle:bool = False
    
    if w * 5.3/10 < x < w * 7.2/10:
      if y >= lines[6] - b:
        offset_x = (w * (5.3/10)) + a
        offset_y = (h * (7.2/10)) + b

        if __checkCoords(a, b, offset_x, offset_y, w, h, x, y):
          circle = True

    r, g, b = RED if circle else CLEAR

  elif y <= lines[7]:
    r, g, b = DARK

  return color(
    max(min(round(r * i), 255), 0),
    max(min(round(g * i), 255), 0),
    max(min(round(b * i), 255), 0),
    normalized=False
  )

def __checkCoords(a, b, offset_x, offset_y, w, h, x, y):
  ''' Checks if a certain coordinate is in a certain elipse '''
  a = a**2
  b = b**2

  # Check X coordinate
  func_y = (a*b - b * (x-offset_x)**2)
  if func_y < 0: return False
  
  func_y = sqrt(func_y / a)
  y_up = func_y + h - offset_y
  y_down = -func_y + h - offset_y
  if not (y_down < y < y_up): return False

  # Check Y coordinate
  func_x = (a*b - a * (y - w + offset_y)**2)
  if func_x < 0: return False
  
  func_x = sqrt(func_x / b)
  x_up = func_x + offset_x
  x_down = -func_x + offset_x
  if not (x_down < x < x_up): return False

  return True
  