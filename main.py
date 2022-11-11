from src import *

if __name__ == '__main__':
  r = Raytracer(500, 500)
  r.light = Light(V3(1, -1, 1), 1.1, color(250, 191, 30, normalized=False))
  r.bg_color = color(135, 206, 255, normalized=False)

  grass = Material(color(0, 1, 0), [0.9, 0.1, 0, 0], 40)
  white_wood = Material(color(230, 230, 230, normalized=False), [0.75, 0.1, 0.15, 0], 50)
  leaf = Material(color(24, 94, 28, normalized=False), [0.4, 0.2, 0.1, 0.2], 40, 5)
  dirt = Material(color(122, 68, 11, normalized=False), [0.9, 0.1, 0, 0], 40)
  light_wood = Material(color(237, 185, 88, normalized=False), [0.5, 0.1, 0.4, 0], 80)
  fire = Material(color(255, 130, 30, normalized=False), [0.8, 0.15, 0, 0.05], 10, 1)

  Tree1 = [
    # Wood
    Cube(V3(1, 0.5, -4), 0.6, white_wood),
    Cube(V3(1, 0, -4), 0.6, white_wood),
    Cube(V3(1, -0.5, -4), 0.6, white_wood),

    # Leafs
    Cube(V3(1, -1, -4), 0.6, leaf),
    Cube(V3(0.6, -0.8, -3.96), 0.6, leaf),
    Cube(V3(1, -0.8, -3.94), 0.6, leaf),
    Cube(V3(1.5, -0.8, -3.94), 0.6, leaf),
  ]
  
  Tree2 = [
    # Wood
    Cube(V3(-1, 0.5, -4), 0.6, white_wood),
    Cube(V3(-1, 0, -4), 0.6, white_wood),
    Cube(V3(-1, -0.5, -4), 0.6, white_wood),

    # Leafs
    Cube(V3(-1, -1, -4), 0.6, leaf),
    Cube(V3(-0.6, -0.8, -3.96), 0.6, leaf),
    Cube(V3(-1, -0.8, -3.94), 0.6, leaf),
    Cube(V3(-1.5, -0.8, -3.94), 0.6, leaf),
  ]

  stairs = [
    Cube(V3(0, 1.4, -4), 0.4, light_wood),
    Cube(V3(-0.4, 1.4, -4), 0.4, light_wood),
    Cube(V3(0.4, 1.4, -4), 0.4, light_wood),
    
    Cube(V3(0, 1.45, -3.5), 0.4, light_wood),
    Cube(V3(-0.4, 1.45, -3.5), 0.4, light_wood),
    Cube(V3(0.4, 1.45, -3.5), 0.4, light_wood),
    
    Cube(V3(0, 1.55, -3), 0.4, light_wood),
    Cube(V3(-0.4, 1.55, -3), 0.4, light_wood),
    Cube(V3(0.4, 1.55, -3), 0.4, light_wood),
  ]

  torchs = [
    Cube(V3(0.3, 0.5, -2.5), 0.08, light_wood),
    Cube(V3(0.3, 0.5 - 0.08, -2.5), 0.08, light_wood),
    Cube(V3(0.3, 0.5 - (0.08 *2), -2.5), 0.08, light_wood),
    Sphere(V3(0.3, 0.5 - (0.08 *3), -2.55), 0.08, fire),
   
    Cube(V3(-0.3, 0.5, -2.5), 0.08, light_wood),
    Cube(V3(-0.3, 0.5 - 0.08, -2.5), 0.08, light_wood),
    Cube(V3(-0.3, 0.5 - (0.08 *2), -2.5), 0.08, light_wood),
    Sphere(V3(-0.3, 0.5 - (0.08 *3), -2.55), 0.08, fire),
  ]

  r.scene = [
    Plane(V3(0, 2, -3), 100, 80, grass),
    Plane(V3(0, 1.625, -4), 100, 3, dirt),
    *stairs,
    *Tree1,
    *Tree2,
    *torchs,
  ]

  r.render()