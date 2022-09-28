''' 
--------------------------------------
  Universidad del Valle de Guatemala
  Author: Diego Cordova - 20212

  gl.py
  - Uses de Renderer Object to
    write bmp files

  Last modified (yy-mm-dd): 2022-09-12
--------------------------------------
'''

from .Render import Render
from .util import color as color_b
from .MStructs.Vector import V3
from .IO_bmp import *
from .Texture import Texture
from .Shaders import gouraud

def glInit(shader=gouraud):
  ''' Initialized Internal Render Object '''
  global SR
  SR = Render()
  SR.current_shader = shader

def sr_isInit():
  '''
    Checks if Internal Object is Initialized
    If not, reaises exception
  '''
  try:
    SR.current_color

  except NameError:
    raise Exception('ERROR: Software Renderer not initialized\n\
       execute glInit before any action\n\
    ')

def glCreateWindow(width: int, height: int):
  ''' Initialize Window of image '''
  sr_isInit()
  SR.initWindow(width=width, height=height)

def glClear():
  ''' Fills image with one plain color (clear_color)'''
  sr_isInit()
  SR.clear()

def glCLearColor(r, g, b):
  ''' changes clear_color'''
  sr_isInit()
  SR.set_clear_color(color_b(r, g, b))

def glColor(r, g, b):
  ''' changes the color for writting pixels '''
  sr_isInit()
  SR.set_current_color(color_b(r, g, b))

# ------------ Carga de modelos ------------

def lookAt(eye, center, up, coeff):
  sr_isInit()
  SR.lookAt(V3(*eye), V3(*center), V3(*up), coeff)

def load_model(
  model_path, 
  L,
  translate=(0, 0, 0),
  scale    =(1, 1, 1),
  rotate   =(0, 0, 0),
  texture_path = None
):
  sr_isInit()
  SR.load_model(
    model_path,
    L=L,
    translate=translate,
    scale=scale,
    rotate=rotate,
    texture_path=texture_path
  )

# ------------ Escritura de Archivos ------------

def gl_zBuffer(fileName, scale):
  ''' Writes the Z-Buffer to a bmp file '''
  sr_isInit()
  z_write(fileName + '.bmp', SR.zBuffer, scale)
  print(f'-> Z-Buffer written succesfully to: {fileName}.bmp')

def glFinish(fileName):
  ''' Writes the FrameBuffer to a bmp file '''
  sr_isInit()
  write_bmp(fileName + '.bmp', SR.framebuffer)
  print(f'-> FrameBuffer written succesfully to: {fileName}.bmp')

def setBG(img_path):
  sr_isInit()
  img = Texture(img_path)
  SR.framebuffer = img.pixels