import numpy as np
from Optimizer import ABC
from config import objective_function
from Pendulum import InvertedPendulum
from Simulation import Simulation

# @title <p> Find optimal value for Q and R

# Define bounds for optimization (example: Q diagonal entries and R value)
bounds = [(0.1, 100)] * 4 + [(0.1, 10)]  # Diagonal of Q (4 values) and scalar R (1 value)

# Initialize and run ABC optimization
abc = ABC(objective_function=objective_function, num_bees=30, max_iter=5, limit=10)
best_solution, best_fitness = abc.optimize(dim=5, bounds=bounds, verbose=True)

print("Best Q and R parameters found:", best_solution)
print("Best fitness (LQR cost):", best_fitness)

# @title <p> Simulate without best solution
pendulum = InvertedPendulum()
pendulum_solution = pendulum.solve(t=20, t_sampling=100)

simulation = Simulation(pendulum_solution)
simulation.plot(f"Simulasi Inverted Pendulum Without Optimization")
simulation.simulate(pendulum.L, title=f"Simulasi Inverted Pendulum Without Optimization")

# @title <p> Simulate using best solution
Q = np.diag(best_solution[:-1])
R = np.array([[best_solution[-1]]])

optimized_pendulum = InvertedPendulum(Q=Q, R=R)
pendulum_solution = optimized_pendulum.solve(t=20, t_sampling=100)

simulation = Simulation(pendulum_solution)
simulation.plot(title=f"Simulasi Inverted Pendulum With ABC Optimization")
simulation.simulate(optimized_pendulum.L, title=f"Simulasi Inverted Pendulum With ABC Optimization")