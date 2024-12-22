import numpy as np

def system_matrices(
    m: float = 0.1,
    M: float = 1.0,
    L: float = 1.0,
    g: float = 9.81,
    d: float = 0.1,
  ):

  A = np.array([
      [0, 1, 0, 0],
      [0, -d/m, -m*g/m, 0],
      [0, 0, 0, 1],
      [0, d/(m*L), (m+M)*g/(m*L), 0]
  ])
  B = np.array([[0], [-1/m], [0], [1/(m*L)]])

  return A, B