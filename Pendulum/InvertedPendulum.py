import numpy as np
from scipy.integrate import solve_ivp
from LQR import LQR

# @title <p> Initialize Pendulum Class
class InvertedPendulum:
  def __init__(self,
                m: float = 0.1,
                M: float = 1.0,
                L: float = 1.0,
                g: float = 9.81,
                d: float = 0.1,
                x_0: float = 0,
                theta_0: float = 0.1,
                force_0: float = 0,
                Q: np.ndarray = None,
                R: np.ndarray = None):

      self.m = m
      self.M = M
      self.L = L
      self.g = g
      self.d = d

      self.force_0 = force_0
      self.initial = np.array([x_0, 0, theta_0, 0])

      self.A, self.B = self._system_matrices(m, M, L, g, d)

      # Matriks cost untuk LQR
      self.Q = np.diag([10, 1, 10, 1]) if Q is None else Q
      self.R = np.array([[0.1]]) if R is None else R

  def _system_matrices(self, m, M, L, g, d ):

    A = np.array([
        [0, 1, 0, 0],
        [0, -d/m, -m*g/m, 0],
        [0, 0, 0, 1],
        [0, d/(m*L), (m+M)*g/(m*L), 0]
    ])
    B = np.array([[0], [-1/m], [0], [1/(m*L)]])

    return A, B

  def solve(
      self,
      t:float,
      t_sampling:float,
    ):

    lqr = LQR()
    K = lqr.solve(self.A, self.B, self.Q, self.R)
    del(lqr)

    def pendulum_dynamics(t, x):
      u = self._control_input(K, x, self.force_0)
      dxdt = self._time_derivative(self.A, self.B, x, u)
      return dxdt

    # Simulasi sistem
    t_span = (0, t)  # Rentang waktu simulasi
    t_eval = np.linspace(t_span[0], t_span[1], t_sampling)  # Titik waktu evaluasi
    solution = solve_ivp(pendulum_dynamics, t_span, self.initial, t_eval=t_eval)
    return solution

  def _control_input(self, K, x, force_0):
    u = -K @ x + force_0
    return u

  def _time_derivative(self, A, B, x, u):
    dxdt = A @ x + B.flatten() * u
    return dxdt