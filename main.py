''' 
--------------------------------------
  Universidad del Valle de Guatemala
  Author: Diego Cordova - 20212

  main.py
  - main program to write files
  
  Last modified (yy-mm-dd): 2022-09-17
--------------------------------------
'''

if __name__ == '__main__':
  from Drivers import *
  from src.Shaders import *

  print('---- Rendering Jupiter with shaders ----')
  LIGHT = (-15, 15, 50)
  W = 800
  SIZE = 1.8

  transform = rotate = center = (0, 0, 0)
  scale = (SIZE, SIZE, SIZE)
  eye = (0, 0, 1)
  up = (0, 1, 0)
  coeff = 0.0001

  paintModel(
    './models/NoText/Sphere.obj', None, W, transform, scale, 
    rotate, eye, center, up, coeff, LIGHT, 'Renders/Jupiter', jupiter_shader
  )

