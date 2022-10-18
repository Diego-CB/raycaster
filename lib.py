from Lib.Vector import V3

def reflect(I:V3, N:V3) -> V3:
  return (I - N * 2 * (N * I)).normalize()

def refract(I:V3,  N:V3, roi):
  etai = 1
  etat = roi
  cosi = (I * N) * -1

  if cosi < 0:
    cosi *= -1
    etai *= -1
    etat *= -1
    N *= -1

  eta = etai / etat
  k = 1 - eta**2 * (1 - cosi**2)

  if k < 0:
    return V3(1, 0, 0)
  
  cost = k ** 0.5

  return ((I * eta) + (N * (eta * cosi - cost))).normalize()

'''
def refract(I:V3,  N:V3, roi):
    cosi = -max(-1, min(1, I * N))
    etai = 1
    etat = roi

    if cosi < 0:  # if the ray is inside the object, swap the indices and invert the normal to get the correct result
      cosi = -cosi
      etai, etat = etat, etai
      N = N * -1

    eta = etai/etat
    k = 1 - eta**2 * (1 - cosi**2)
    if k < 0:
      return V3(1, 0, 0)
    cost = k ** 0.5

    return ((
      (I * eta) +
      (N * (eta * cosi - cost))
    )).normalize()
'''