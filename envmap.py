from cmath import pi
from mmap import mmap
import numpy
import mmap
import struct
import math
from Lib.util import *
from Lib.Vector import *


class Envmap:
  def __init__(self, path) -> None:
    self.path = path
    self.read()

  def read(self):
    with open(self.path) as img:
      m = mmap.mmap(img.fileno(), 0, access=mmap.ACCESS_READ)
      ba = bytearray(m)
      header_size = struct.unpack('=l', ba[10:14])[0]
      self.width = struct.unpack('=l', ba[18:22])[0]
      self.height = struct.unpack('=l', ba[22:26])[0]
      all_bytes = ba[header_size::]
      self.pixels = numpy.frombuffer(all_bytes, dtype='uint8')

    print('done')
    print(self.width)
    print(self.height)
    assert False, 1

  def get_color(self, direction):
    girection = direction.normalize()
    x = int(math.atan2(direction.z, direction.x) / (2 * pi) * 0.5) * self.width
    y = int(math.acos(-direction.y) / pi) * self.height

    index = ((y * self.width +x) * 3) % len(self.pixels)

    
    c = self.pixels[index:index+3].astype(numpy.uint8)
    return color(
      c[2],
      c[1],
      c[0],
      normalized=False
    )

