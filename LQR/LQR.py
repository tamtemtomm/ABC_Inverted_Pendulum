import numpy as np
import scipy

# @title <p> Make it into class module
class LQR :
  def __init__(self):
    pass

  def _gain(self, R, B, P):

    # K = R^(-1).B.P
    K = np.linalg.inv(R) @ B.T @ P
    return K

  def _solve_riccati(self, A, B, Q, R):

    # A.P + P.A - P.B.R^(-1).B.P + Q = 0
    P = scipy.linalg.solve_continuous_are(A, B, Q, R)
    return P

  def solve_manual(
      self,
      A:np.ndarray,
      B:np.ndarray,
      Q:np.ndarray,
      R:np.ndarray,
      max_iter:int=1000,
      tol:float=1e-8
  ):
      # Initialize P with Q
      P = np.copy(Q)

      for iteration in range(max_iter):
          # Compute the intermediate term: B.T @ P @ B
          BT_P_B = B.T @ P @ B

          # Compute the gain: (R + B.T @ P @ B)^(-1)
          gain = np.linalg.inv(R + BT_P_B)

          # Update P
          P_next = A.T @ P @ A - A.T @ P @ B @ gain @ B.T @ P @ A + Q

          # Check for convergence
          if np.linalg.norm(P_next - P, ord='fro') < tol:
              print(f"Converged after {iteration + 1} iterations")
              return P_next

          # Update P for the next iteration
          P = P_next

      print("Maximum iterations reached without convergence")
      return P

  def solve(self, A, B, Q, R):
    P = self._solve_riccati(A, B, Q, R)
    K = self._gain(R, B, P)
    return K

  def cost(self, x, u, Q, R):
    cost = x.T @ Q @ x + u.T @ R @ u
    return cost