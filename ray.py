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
  rubber = Material(diffuse=color(80, 0, 0, False), albedo=[0.9, 0.1], spec=10)
  ivory = Material(diffuse=color(100, 100, 80, False), albedo=[0.6, 0.3], spec=50)

  r = Raytracer(800, 800)
  r.light = Light(V3(0, 0, 0).normalize(), 1, color(1, 1, 1))

  r.scene = [
    Sphere(V3(4, 0, -16), 3, rubber),
    Sphere(V3(-1.5, 0, -10), 3, ivory),
  ]

  r.render()
