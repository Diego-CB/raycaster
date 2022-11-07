from cmath import pi
from math import tan
from .Light import Light
from .util import *

MAX_RECURSION_DEPTH = 3

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

  def cast_ray(self, origin, direction, recursion = 0):
    if recursion >= MAX_RECURSION_DEPTH:
      return self.bg_color

    material, intersect = self.scene_intersect(origin, direction)

    if material is None:
      return self.bg_color


    # Refraccion

    if material.albedo[3] > 0:
      refract_direction = refract(direction, intersect.normal, material.refractive_index)
      refract_bias = -3 if (refract_direction * intersect.normal) < 0 else 3
      refract_origin = intersect.point + (intersect.normal * refract_bias)
      refract_color = self.cast_ray(refract_origin, refract_direction, recursion + 1)
    else:
      refract_color = color(0, 0, 0)

    refraction = color(
      int(refract_color[2] * material.albedo[3]),
      int(refract_color[1] * material.albedo[3]),
      int(refract_color[0] * material.albedo[3]),
      normalized=False
    )

    # Reflexion
    offset_normal = intersect.normal * 0.001

    if material.albedo[2] > 0:
      reflect_dir = reflect(direction, intersect.normal)
      reflect_orig = (
        offset_normal - intersect.point \
          if reflect_dir * intersect.normal < 0 \
          else intersect.point + offset_normal
      )
      reflect_color = self.cast_ray(reflect_orig, reflect_dir, recursion + 1)
    else:
      reflect_color = color(0, 0, 0)

    reflection = (
      int(float(reflect_color[0]) * material.albedo[2]),
      int(float(reflect_color[1]) * material.albedo[2]),
      int(float(reflect_color[2]) * material.albedo[2]),
    )

    light_dir = (self.light.position - intersect.point).normalize()
    light_distance = (self.light.position - intersect.point).size()

    # Shadows

    shadow_orig = (intersect.point - offset_normal) if (light_dir * intersect.normal) < 0 else (intersect.point + offset_normal)
    shadow_material, shadow_intersect = self.scene_intersect(shadow_orig, light_dir)
    shadow_intensity = 0

    if shadow_material and (shadow_intersect.point - shadow_orig).size() < light_distance:
      shadow_intensity = 0.4

    intensity = self.light.intensity * max(0, light_dir * intersect.normal) * (1 - shadow_intensity)
    
    
    # Difusse component

    diffuse = (
      int(material.diffuse[2] * intensity * material.albedo[0]),
      int(material.diffuse[1] * intensity * material.albedo[0]),
      int(material.diffuse[0] * intensity * material.albedo[0])
    )

    # Specular intensity
    light_reflection = reflect(light_dir, intersect.normal)
    reflection_intensity = max(0, light_reflection * direction)
    specular_intensity = self.light.intensity * reflection_intensity**material.spec
    specular = (
      int(self.light.color[2] * specular_intensity * material.albedo[1]),
      int(self.light.color[0] * specular_intensity * material.albedo[1]),
      int(self.light.color[1] * specular_intensity * material.albedo[1])
    )

    spec_color = (
      max(0, min(255, diffuse[0] + specular[2] + reflection[2] + refraction[2])),
      max(0, min(255, diffuse[1] + specular[1] + reflection[1] + refraction[1])),
      max(0, min(255, diffuse[2] + specular[0] + reflection[0] + refraction[0])),
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

  def get_bg(self, direction):
    if self.envmap:
      return self.envmap.get_color(direction)

    return self.bg_color

