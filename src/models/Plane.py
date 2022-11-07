from math import dist
from ..Intersect import Intersect
from ..Lib.Vector import V3
from ..material import Material

class Plane:
  def __init__(self, center, w, h, material) -> None:
    self.center:V3 = center
    self.material:Material = material
    self.w = w
    self.h = h

  def ray_intersect(self, origin:V3, direction:V3) -> Intersect:
    if direction.y == 0: return False
    d = (self.center.y - origin.y) / direction.y
    impact = direction * d - origin
    normal = V3(0, -1, 0)

    if d <= 0 or \
      (self.center.x - self.w/2) > impact.x or impact.x > (self.center.x + self.w/2) \
      or (self.center.z - self.h/2) > impact.z or impact.z > (self.center.z + self.h/2) \
    :
      return False

    return Intersect(
      distance=d,
      point=impact,
      normal=normal
    )

  