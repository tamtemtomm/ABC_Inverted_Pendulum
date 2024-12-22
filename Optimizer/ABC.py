import numpy as np
from Simulation import Simulation
from Pendulum import InvertedPendulum


class ABC:
    def __init__(self, objective_function, num_bees=30, max_iter=100, limit=10):

        self.objective_function = objective_function
        self.num_bees = num_bees
        self.max_iter = max_iter
        self.limit = limit
        self.solution = None  # Best solution found
        self.best_fitness = float('inf')  # Best fitness value

    def _initialize_population(self, dim, bounds):

        low = np.array([b[0] for b in bounds])
        high = np.array([b[1] for b in bounds])

        # Ensure low and high arrays have the same length as `dim`
        if len(low) != dim or len(high) != dim:
            raise ValueError("Bounds dimensionality must match `dim`.")

        # Generate random values within bounds for the entire population
        population = np.random.uniform(
            low=low, high=high, size=(self.num_bees, dim))
        return population

    def optimize(self, dim, bounds, verbose=False, simulate=False):

        print(f'dim={dim}, bounds={bounds}')

        if simulate : 
            verbose=True
        
        population = self._initialize_population(dim, bounds)
        fitness = np.array([self.objective_function(ind)
                           for ind in population])
        # Tracks the number of unsuccessful trials
        trial = np.zeros(self.num_bees)

        for iteration in range(self.max_iter):

            population, fitness, trial = self._employed_bees(
                population, self.objective_function, fitness, self.num_bees, bounds, trial)

            population, fitness, trial = self._onlooker_bees(
                population, self.objective_function, fitness, self.num_bees, bounds, trial)

            population, fitness, trial = self._scout_bees(
                population, self.objective_function, fitness, self.num_bees, bounds, trial, self.limit)

            # Update best solution
            best_idx = np.argmin(fitness)
            if fitness[best_idx] < self.best_fitness:
                self.solution = population[best_idx]
                self.best_fitness = fitness[best_idx]

            if verbose:
                print('----------------------------------------------')
                print(f'Iteration {iteration + 1}')
                print(f'Best solution : {self.solution}')
                print(f'Best fitness : {self.best_fitness}')

            if simulate : 
                Q = np.diag(self.solution[:-1])
                R = np.array([[self.solution[-1]]])

                pendulum = InvertedPendulum(Q=Q, R=R)
                pendulum_solution = pendulum.solve(t=10, t_sampling=100)

                simulation = Simulation(pendulum_solution)
                simulation.plot(title=f'Simulasi Iterasi {iteration}')

                del(pendulum)
                del(simulation)

        return self.solution, self.best_fitness

    def _mutate_solution(self, solution, population, bounds):

        phi = np.random.uniform(-1, 1, size=solution.shape)
        partner = population[np.random.randint(len(population))]
        candidate = solution + phi * (solution - partner)
        # Clip to bounds
        candidate = np.clip(candidate, [b[0]
                            for b in bounds], [b[1] for b in bounds])
        return candidate

    def _employed_bees(self, population, objective_function, fitness, num_bees, bounds, trial):

        for i in range(num_bees):
            candidate = self._mutate_solution(
                population[i], population, bounds)
            candidate_fitness = objective_function(candidate)
            if candidate_fitness < fitness[i]:
                population[i] = candidate
                fitness[i] = candidate_fitness
                trial[i] = 0
            else:
                trial[i] += 1

        return population, fitness, trial

    def _onlooker_bees(self, population, objective_function, fitness, num_bees, bounds, trial):

        prob = fitness / fitness.sum()  # Probability selection based on fitness
        for i in range(num_bees):
            if np.random.rand() < prob[i]:
                candidate = self._mutate_solution(
                    population[i], population, bounds)
                candidate_fitness = objective_function(candidate)
                if candidate_fitness < fitness[i]:
                    population[i] = candidate
                    fitness[i] = candidate_fitness
                    trial[i] = 0
                else:
                    trial[i] += 1

        return population, fitness, trial

    def _scout_bees(self, population, objective_function, fitness, num_bees, bounds, trial, limit):

        for i in range(num_bees):
            if trial[i] >= limit:
                population[i] = self._initialize_population(1, bounds)[0]
                fitness[i] = objective_function(population[i])
                trial[i] = 0

        return population, fitness, trial
