from ..Intersect import Intersect
from ..util import V3
from ..material import Material

class Cube:
  def __init__(self, center:V3, size, material) -> None:
    self.center:V3 = center
    self.material:Material = material
    self.size = size
    b_size = size/2
    self.minBounding = center + V3(b_size, b_size, b_size)
    self.maxBounding = center - V3(b_size, b_size, b_size)

  def ray_intersect(self, origin:V3, direction:V3) -> Intersect:
    txmin = 9999 if direction.x == 0 else (self.minBounding.x - origin.x) / direction.x
    txmax = 9999 if direction.x == 0 else (self.maxBounding.x - origin.x) / direction.x
    
    if txmin > txmax:
      txmin, txmax = txmax, txmin
    
    tymin = 9999 if direction.y == 0 else (self.minBounding.y - origin.y) / direction.y
    tymax = 9999 if direction.y == 0 else (self.maxBounding.y - origin.y) / direction.y

    if tymin > tymax:
      tymin, tymax = tymax, tymin

    if ((txmin > tymax) or (tymin > txmax)): return False 

    if (tymin > txmin):
      txmin = tymin
 
    if (tymax < txmax):
        txmax = tymax

    tzmin = 9999 if direction.z == 0 else (self.minBounding.z - origin.z) / direction.z
    tzmax = 9999 if direction.z == 0 else (self.maxBounding.z - origin.z) / direction.z

    if (tzmin > tzmax):
      tzmin, tzmax = tzmax, tzmin
 
    if ((txmin > tzmax) or (tzmin > txmax)):
      return False
 
    if (tzmin > txmin):
      txmin = tzmin
 
    if (tzmax < txmax):
      txmax = tzmax

    # Distance and impact
    d = self.center - origin

    # Normal
    impact_layer = (
      self.center.x - origin.x,
      self.center.y - origin.y,
      self.center.z - origin.z
    )
    min_index = impact_layer.index(min(impact_layer))

    normal:V3 = V3(
      0 if min_index != 0 else 1 if impact_layer[0] <= 0 else -1,
      0 if min_index != 1 else 1 if impact_layer[1] <= 0 else -1,
      0 if min_index != 2 else 1 if impact_layer[2] <= 0 else -1,
    )

    return Intersect(
      distance=d.size(),
      point=d,
      normal=normal
    )

  