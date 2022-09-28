from Intersect import Intersect
from Lib.IO_bmp import *
from Lib.Vector import V3
from Lib.util import *
from Sphere import Sphere
from Light import Light
from material import Material
from cmath import pi
from math import tan

class Raytracer:
  def __init__(self, width, height):
    self.width = width
    self.height = height
    self.bg_color = color(0, 0, 0)
    self.current_color = color(1, 1, 1)
    self.scene = []
    self.light = Light(V3(0, 0, 0), 1)
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
    material, intersect = self.scene_intersect(origin, direction)
    if material is None: return self.bg_color

    light_dir = (self.light.position - intersect.point).normalize()
    intensity = light_dir * intersect.normal
    print(material.diffuse)
    print(intensity)

    diffuse = (
      int(material.diffuse[2] * intensity),
      int(material.diffuse[1] * intensity),
      int(material.diffuse[0] * intensity)
    )
    print(diffuse)
    
    diffuse = color(*diffuse, normalized=False)

    return diffuse


  def scene_intersect(self, origin, direction):
    zBuffer = 9999
    material = None
    intersect = None

    for o in self.scene:
      obj_intersect = o.ray_intersect(origin, direction)

      if obj_intersect:
        if obj_intersect.distance < zBuffer:
          zBuffer = obj_intersect.distance
          material = o.material
          intersect = obj_intersect

    return material, intersect

# -- main --

red = Material(color(1, 0, 0))
white = Material(color(1, 1, 1))
SIZE = 800
r = Raytracer(SIZE, SIZE)
r.light = Light(V3(-3, -2, 0).normalize(), 1)
r.scene = [
  Sphere(V3(-3, 0, -16), 2, red),
  Sphere(V3(-2.8, 0, -10), 2, white),
]

r.point(100, 100)
r.render()
