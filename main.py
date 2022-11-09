from src.util import *
from src.models import *
from src import *

if __name__ == '__main__':
  r = Raytracer(500, 500)
  r.light = Light(V3(-1, -1, 1), 1.2)
  r.bg_color = color(0, 0, 0, normalized=False)
  r.bg_color = color(50, 50, 140, normalized=False)

  rubber = Material(color(180, 0, 0, normalized=False), [0.9, 0.1, 0, 0], 10)
  ivory = Material(color(200, 200, 180, normalized=False), [0.6, 0.3, 0.1, 0], 50)
  mirror = Material(color(0, 0, 0), [0, 10, 0.8, 0], 1425)
  glass = Material(color(0, 0, 0), [0, 0, 0, 1], 125, 1.5)

  cc = Material(color(1, 1, 1), [1, 0, 0, 0], 0, 0)

  r.scene = [
    Cube(V3(-0.05, 0.2, -10), 5, rubber),
    Sphere(V3(0, 0.2, -8), 2, glass),
    Plane(V3(0, 1.5, -3), 1, 1, ivory)
  ]

  r.render()

else:
  r = Raytracer(500, 500)
  r.light = Light(V3(-1, -1, 1), 1.2)
  r.bg_color = color(0, 0, 0, normalized=False)
  r.bg_color = color(0, 0, 140, normalized=False)

  rubber = Material(color(180, 0, 0, normalized=False), [0.9, 0.1, 0, 0], 10)
  ivory = Material(color(200, 200, 180, normalized=False), [0.6, 0.3, 0.1, 0], 50)
  mirror = Material(color(0, 0, 0), [0, 10, 0.8, 0], 1425)
  glass = Material(color(0, 0, 0), [0, 0, 0, 1], 125, 1.5)

  r.scene = [
    Sphere(V3(0, -2, -11.5), 2, ivory),
    Sphere(V3(1, 1, -8.5), 1.7, rubber),
    Sphere(V3(-2, 1, -10), 2.5, mirror),
    Sphere(V3(0, 0, -5), 1, glass),
    Plane(V3(0, 2.8, -5), 10, 10, ivory)
  ]

  r.render()
