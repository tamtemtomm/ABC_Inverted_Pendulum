import numpy as np
from LQR import LQR
from Pendulum import InvertedPendulum

def objective_function(params):

  # print(f'Params : {params}')

  # Initialize Q and R
  Q = np.diag(params[:-1])
  R = np.array([[params[-1]]])

  # Initialize the pendulum
  pendulum = InvertedPendulum(Q=Q, R=R)

  # Solve for 10 seconds with 100 sampling points
  solution = pendulum.solve(t=10, t_sampling=100)

  # Calculate LQR cost J
  lqr = LQR()
  lqr_cost = 0
  for i in range(len(solution.t)):
      x_t = solution.y[:, i]
      u_t = -pendulum._control_input(lqr.solve(pendulum.A, pendulum.B, pendulum.Q, pendulum.R), x_t, pendulum.force_0)
      lqr_cost = lqr.cost(x_t, u_t, pendulum.Q, pendulum.R)
      # lqr_cost += x_t.T @ pendulum.Q @ x_t + u_t.T @ pendulum.R @ u_t

  del(pendulum)
  del(lqr)

  return lqr_cost