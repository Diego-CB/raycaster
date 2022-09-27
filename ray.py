from Lib.IO_bmp import *
from Lib.Vector import V3
from Lib.util import *
from Lib.Sphere import Sphere
from cmath import pi
from math import tan

class Raytracer:
  def __init__(self, width, height):
    self.width = width
    self.height = height
    self.bg_color = color(0, 0, 0)
    self.current_color = color(1, 1, 1)
    self.clear()

  def clear(self):
    ''' Fills framebuffer with the actual clear_color'''
    self.framebuffer = [
      [self.bg_color for x in range(self.width)]
        for y in range(self.height)
    ]

  def point(self, x, y, c=None):
    if y < 0 or x < 0: return
    if y > self.height - 1 or x > self.width - 1: return
    self.framebuffer[y][x] = c or self.current_color

  def write(self, filename):
    write_bmp(filename, self.framebuffer)

  def render(self):
    FOV = int(pi * 1/2)
    AR = self.width / self.height
    tana = tan(FOV/2)

    for y in range(self.height):
      for x in range(self.width):
        i = ((2 * (x + 0.5) / self.width) - 1) * tana * AR
        j = (1 - (2 * (y + 0.5) / self.width)) * tana

        origin = V3(0, 0, 0)
        direction = V3(i, j, -1).normalize()
        c = self.cast_ray(origin, direction)

        self.point(x, y, c)

    filename = 'ray.bmp'
    self.write('./Renders/' + filename)
  
  def cast_ray(self, origin, direction):
    check = [ s.ray_intersect(origin, direction) 
      for s in [
        Sphere(V3(0, 3.8, -16), 4),
        Sphere(V3(0, -1.2, -16), 3),
        Sphere(V3(0, -5.5, -16), 2),
      ]
    ]

    if True in check:
      return color(0.8, 0.8, 0.8)
    else:
      return self.bg_color


# -- main --
SIZE = 400
r = Raytracer(SIZE, SIZE)
r.render()
