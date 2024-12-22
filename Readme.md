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

## Requirements
Install the required Python packages using:

``
pip install -r requirements.txt
``

