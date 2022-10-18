from math import dist
from Intersect import Intersect

class Sphere:
  def __init__(self, center, radius, material) -> None:
    self.center = center
    self.radius = radius
    self.material = material

  def ray_intersect(self, origin, direction):
    L = self.center - origin
    tca = L * direction
    l = L.size()
    d2 = l**2  - tca**2

    if d2 > self.radius**2:
      return False

    thc = (self.radius**2 - d2)**0.5
    t0 = tca - thc
    t1 = tca + thc
    
    t = t0
    if t < 0:
      t = t1
    if t < 0:
      return False
    impact = direction * t0 + origin
    normal = (impact - self.center).normalize()

    return Intersect(
      distance=t0,
      point=impact,
      normal=normal
    )
  