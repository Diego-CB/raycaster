from Intersect import Intersect
from Lib.IO_bmp import *
from Lib.Vector import V3
from Lib.util import *
from Sphere import Sphere
from Light import Light
from lib import *
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
    
    # Difusse component
    intensity = light_dir * intersect.normal
    intensity = 0 if intensity < 0 else intensity

    diffuse = (
      int(material.diffuse[2] * intensity * material.albedo[0]),
      int(material.diffuse[1] * intensity * material.albedo[0]),
      int(material.diffuse[0] * intensity * material.albedo[0])
    )
    

    # Specular intensity
    light_reflection = reflect(light_dir, intersect.normal)
    reflection_intensity = max(0, light_reflection * direction)
    specular_intensity = self.light.intensity * reflection_intensity ** material.spec
    specular = (
      int(self.light.color[2] * specular_intensity * material.albedo[1]),
      int(self.light.color[0] * specular_intensity * material.albedo[1]),
      int(self.light.color[1] * specular_intensity * material.albedo[1])
    )

    spec_color = (
      diffuse[0] + specular[0],
      diffuse[1] + specular[2],
      diffuse[2] + specular[1]
    )
    return color(*spec_color, normalized=False)


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

if __name__ == '__main__':
  polar_skin = Material(color(1, 1, 1), [0.9, 0.1], 5)
  polar_body = Material(color(1, 1, 1), [0.7, 0.3], 50)
  pardo_skin = Material(color(150, 75, 0, normalized=False), [0.9, 0.1], 5)
  pardo_body = Material(color(170, 95, 0, normalized=False), [0.7, 0.3], 5)
  eyes = Material(color(0, 0, 0), [1, 0], 0)

  r = Raytracer(600, 600)
  r.light = Light(V3(0, 0, 0).normalize(), 1, color(1, 1, 1))
  r.bg_color = color(0.6, 0.6, 0.6)

  polar_bear = [
    Sphere(V3(-2.5, -2.5 + 2.2, -9), 1.1, polar_body),
    
    Sphere(V3(-3.2, -2.8 + 2, -8), 0.5, polar_skin),
    Sphere(V3(-1.3, -2.9 + 2, -8.4), 0.55, polar_skin),
    
    Sphere(V3(-3, -2.8 + 3.5, -8), 0.5, polar_skin),
    Sphere(V3(-1.5, -2.8 + 3.5, -8), 0.5, polar_skin),
    
    Sphere(V3(-2.28, -1.7, -8), 0.7, polar_skin),
    Sphere(V3(-2.65, -2.05, -7.5), 0.35, polar_skin),
    Sphere(V3(-1.65, -2.15, -7.8), 0.38, polar_skin),

    Sphere(V3(-2.3, -1.65, -7.2), 0.1, eyes),
    Sphere(V3(-2.3 + 0.45, -1.65, -7.2), 0.1, eyes),

    Sphere(V3(-2.17, -1.35, -7.55), 0.25, polar_skin),
    Sphere(V3(-2.08, -1.3, -7.2), 0.08, eyes),
  ]

  offset = 4

  brown_bear = [
    Sphere(V3(offset + -2.1, -2.5 + 2.2, -9), 1.1, pardo_body),
  
    Sphere(V3(offset + -3.2, -2.8 + 2, -8), 0.5, pardo_skin),
    Sphere(V3(offset + -1.3, -2.9 + 2, -8.4), 0.55, pardo_skin),
    
    Sphere(V3(offset + -3, -2.8 + 3.5, -8), 0.5, pardo_skin),
    Sphere(V3(offset + -1.5, -2.8 + 3.5, -8), 0.5, pardo_skin),
    
    Sphere(V3(offset + -2.28, -1.7, -8), 0.7, pardo_skin),
    Sphere(V3(offset + -2.85, -2.05, -7.6), 0.35, pardo_skin),
    Sphere(V3(offset + -1.85, -2.15, -7.5), 0.38, pardo_skin),

    Sphere(V3(offset + -2.6, -1.65, -7.2), 0.1, eyes),
    Sphere(V3(offset + -2.6 + 0.45, -1.65, -7.2), 0.1, eyes),

    Sphere(V3(offset + -2.3, -1.35, -7.55), 0.25, pardo_skin),
    Sphere(V3(offset + -2.35, -1.3, -7.2), 0.08, eyes),
  ]

  r.scene = [*polar_bear, *brown_bear]

  r.render()

