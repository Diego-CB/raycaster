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
    txmin = (self.minBounding.x - origin.x) / direction.x
    txmax = (self.maxBounding.x - origin.x) / direction.x
    
    if txmin > txmax:
      txmin, txmax = txmax, txmin
    
    tymin = (self.minBounding.y - origin.y) / direction.y
    tymax = (self.maxBounding.y - origin.y) / direction.y

    if tymin > tymax:
      tymin, tymax = tymax, tymin

    if ((txmin > tymax) or (tymin > txmax)): return False 

    if (tymin > txmin):
      txmin = tymin
 
    if (tymax < txmax):
        txmax = tymax

    tzmin = (self.minBounding.z - origin.z) / direction.z
    tzmax = (self.maxBounding.z - origin.z) / direction.z

    if (tzmin > tzmax):
      tzmin, tzmax = tzmax, tzmin
 
    if ((txmin > tzmax) or (tzmin > txmax)):
      return False
 
    if (tzmin > txmin):
      txmin = tzmin
 
    if (tzmax < txmax):
      txmax = tzmax

    d = V3(
      (self.center.x - origin.x) / direction.x,
      (self.center.y - origin.y) / direction.y,
      (self.center.z - origin.z) / direction.z
    )

    d = self.center - origin
    impact = V3(
      direction.x * d.x / direction.x,
      direction.y * d.y / direction.y,
      direction.z * d.z / direction.z
    ) - origin

    impact_layer = (
      self.center.x - origin.x,
      self.center.y - origin.y,
      self.center.z - origin.z
    )
    min_index = impact_layer.index(min(impact_layer))

    impact_layer:V3 = V3(
      -1 if min_index == 0 else 1,
      -1 if min_index == 1 else 1,
      -1 if min_index == 2 else 1,
    )

    normal = V3(
      direction.x * impact_layer.x,
      direction.y * impact_layer.y,
      direction.z * impact_layer.z,
    ).normalize()

    return Intersect(
      distance=d.size(),
      point=impact,
      normal=normal
    )

  