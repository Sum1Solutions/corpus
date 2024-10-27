import numpy as np
from tqdm import tqdm

class ConservativeSimulationParams:
    def __init__(self, n_individuals, n_timesteps, theory_understanding, theory_application, teaching_probability):
        self.n_individuals = n_individuals
        self.n_timesteps = n_timesteps
        self.theory_understanding = theory_understanding
        self.theory_application = theory_application
        self.teaching_probability = teaching_probability

# Simulate with parameters from the UI
def run_simulation_with_params(params):
    aware_values = np.zeros((params.n_individuals // 2, params.n_timesteps))
    control_values = np.zeros((params.n_individuals // 2, params.n_timesteps))

    # Simulate both groups (theory-aware vs control)
    for t in range(params.n_timesteps):
        for i in range(params.n_individuals // 2):
            # Simulate choices for theory-aware individuals
            aware_values[i, t] = aware_values[i, t - 1] + np.random.normal(0, 1)
            # Simulate choices for control individuals
            control_values[i, t] = control_values[i, t - 1] + np.random.normal(0, 1)

    return aware_values, control_values
