from Lib.Vector import V3

def reflect(I:V3, N:V3) -> V3:
  return (I - N * 2 * (N * I)).normalize()