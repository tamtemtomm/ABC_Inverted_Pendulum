# Inverted Pendulum Simulation and Optimization

This repository contains a Python implementation of an **Inverted Pendulum** system with Linear Quadratic Regulator (LQR) control. It also integrates an Artificial Bee Colony (ABC) optimization algorithm for fine-tuning the LQR parameters to achieve optimal system performance.

## Features
- **Inverted Pendulum Simulation**: Simulates the dynamics of an inverted pendulum on a cart.
- **LQR Control**: Provides state-space-based optimal control for the system.
- **ABC Optimization**: Optimizes the LQR cost matrices to minimize system error.
- **Visualization**: Includes both static and animated plots of the simulation.

---

## Repository Structure

```plaintext
├── Pendulum
│   └── InvertedPendulum.py       # Inverted Pendulum dynamics and control
├── LQR
│   └── LQR.py                    # Linear Quadratic Regulator implementation
├── Optimizer
│   └── ABC.py                    # Artificial Bee Colony optimization algorithm
├── Simulation
│   └── Simulator.py              # Simulation visualization (static and animated)
├── config
│   └── ObjectiveFunction.py      # Defines the optimization objective function
```

## Requirements
Install the required Python packages using:

Here is a structured README.md file for your repository:

markdown
Copy code
# Inverted Pendulum Simulation and Optimization

This repository contains a Python implementation of an **Inverted Pendulum** system with Linear Quadratic Regulator (LQR) control. It also integrates an Artificial Bee Colony (ABC) optimization algorithm for fine-tuning the LQR parameters to achieve optimal system performance.

## Features
- **Inverted Pendulum Simulation**: Simulates the dynamics of an inverted pendulum on a cart.
- **LQR Control**: Provides state-space-based optimal control for the system.
- **ABC Optimization**: Optimizes the LQR cost matrices to minimize system error.
- **Visualization**: Includes both static and animated plots of the simulation.

---

## Repository Structure

```plaintext
├── Pendulum
│   └── InvertedPendulum.py       # Inverted Pendulum dynamics and control
├── LQR
│   └── LQR.py                    # Linear Quadratic Regulator implementation
├── Optimizer
│   └── ABC.py                    # Artificial Bee Colony optimization algorithm
├── Simulation
│   └── Simulator.py              # Simulation visualization (static and animated)
├── config
│   └── ObjectiveFunction.py      # Defines the optimization objective function
```

## Requirements
Install the required Python packages using:

``
pip install -r requirements.txt
``
## How to Use
1. Simulating the Inverted Pendulum
You can directly simulate the pendulum with the default LQR settings:

```
from Pendulum import InvertedPendulum
from Simulation import Simulation

# Initialize and solve the system
pendulum = InvertedPendulum()
solution = pendulum.solve(t=10, t_sampling=100)

# Visualize the results
simulation = Simulation(solution)
simulation.plot()
simulation.simulate(L=pendulum.L)
```
2. Optimizing LQR Parameters
Optimize the $Q$ and $R$ matrices using the ABC algorithm:
```
from Optimizer.ABC import ABC
from config.ObjectiveFunction import objective_function

# Define parameter bounds ([min, max] for each element)
bounds = [(1, 20), (1, 5), (1, 20), (1, 5), (0.01, 1)]

# Initialize ABC optimizer
optimizer = ABC(objective_function, num_bees=30, max_iter=50)

# Run optimization
solution, best_fitness = optimizer.optimize(dim=5, bounds=bounds, simulate=True)

print(f"Optimized Parameters: {solution}")
print(f"Best Fitness Value: {best_fitness}")
```
3. Simulating Optimized Results
Visualize the system's performance with optimized parameters:
```
from Pendulum import InvertedPendulum
from Simulation import Simulation

# Use optimized Q and R
Q = np.diag(solution[:-1])
R = np.array([[solution[-1]]])

pendulum = InvertedPendulum(Q=Q, R=R)
optimized_solution = pendulum.solve(t=10, t_sampling=100)

simulation = Simulation(optimized_solution)
simulation.plot()
```

## Examples
1. Example Plot <br></br>
   ![Figure_1_1](https://github.com/user-attachments/assets/103c8991-0edd-4569-b4c6-4ff71a5b4a78)

2. Example Simulation <br></br>
  ![Figure_2_1](https://github.com/user-attachments/assets/04aa3bfe-bf39-4315-8d8e-9042d3360ad1)

## Future Work
1. Implement additional optimization algorithms for comparison.
2. Extend the system to include external disturbances.
3. Integrate real-time control on hardware.
