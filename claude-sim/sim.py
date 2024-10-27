from dataclasses import dataclass
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm

# Redefining necessary components due to the environment reset
@dataclass
class ConservativeSimulationParams:
    n_individuals: int = 1000          # 1000 individuals
    n_timesteps: int = 500             # 500 timesteps
    baseline_choice_std: float = 0.05  # Very conservative randomness
    emotional_impact: float = 0.1      # Lower emotional impact
    perspective_strength: float = 0.1  # Lower perspective effect
    network_strength: float = 0.05     # Lower network influence
    learning_rate: float = 0.0005      # Slow learning rate
    spin_frequency: float = 0.05       # Less frequent emotional spins
    spin_duration: int = 3             # Shorter emotional spin duration
    perspective_probability: float = 0.02 # Less frequent perspective shifts
    # Theory awareness parameters - Conservative (lower understanding and application)
    theory_understanding: float = 0.3  # Low understanding of theory for aware individuals
    theory_application: float = 0.2    # Low application of theory for aware individuals
    receptiveness_threshold: float = 0.3  # Conservative mood threshold for learning from others
    teaching_probability: float = 0.1     # Very slow peer learning rate

class Individual:
    def __init__(self, params: ConservativeSimulationParams, has_theory_knowledge: bool = False):
        self.params = params
        self.value = 0.0
        self.emotional_state = 0.0
        self.perspective_level = 0.0
        self.choice_history = []
        self.value_history = []
        self.emotional_history = []
        self.in_spin = False
        self.spin_countdown = 0
        self.has_theory_knowledge = has_theory_knowledge
        self.theory_understanding = params.theory_understanding if has_theory_knowledge else 0.0
        self.theory_application = params.theory_application if has_theory_knowledge else 0.0
        
    def make_choice(self, network_influence: float = 0.0) -> float:
        base_choice = np.random.normal(0, self.params.baseline_choice_std)
        
        # Theory-aware individuals are better at:
        if self.has_theory_knowledge:
            # 1. Recognizing emotional states (reduced negative impact)
            emotional_effect = -self.emotional_state * self.params.emotional_impact * (1 - self.theory_understanding)
            
            # 2. Taking perspective (increased positive impact)
            perspective_effect = self.perspective_level * self.params.perspective_strength * (1 + self.theory_understanding)
            
            # 3. Learning from others (enhanced network effect)
            network_effect = network_influence * self.params.network_strength * (1 + self.theory_application)
            
            # 4. Faster learning
            learning_effect = len(self.choice_history) * self.params.learning_rate * (1 + self.theory_application)
        else:
            emotional_effect = -self.emotional_state * self.params.emotional_impact
            perspective_effect = self.perspective_level * self.params.perspective_strength
            network_effect = network_influence * self.params.network_strength
            learning_effect = len(self.choice_history) * self.params.learning_rate
        
        choice = base_choice + emotional_effect + perspective_effect + network_effect + learning_effect
        choice = np.clip(choice, -1, 1)
        
        self.choice_history.append(choice)
        self.value += choice
        self.value_history.append(self.value)
        self.emotional_history.append(self.emotional_state)
        
        return choice
    
    def update_state(self):
        # Theory-aware individuals:
        if self.has_theory_knowledge:
            # 1. Have shorter emotional spins
            if not self.in_spin:
                if np.random.random() < self.params.spin_frequency * (1 - self.theory_understanding):
                    self.in_spin = True
                    self.spin_countdown = int(self.params.spin_duration * (1 - self.theory_understanding))
                    self.emotional_state = np.random.uniform(0.5, 1.0) * (1 - self.theory_understanding)
            else:
                self.spin_countdown -= 1
                if self.spin_countdown <= 0:
                    self.in_spin = False
                    self.emotional_state = 0.0
            
            # 2. Have more frequent perspective shifts
            if np.random.random() < self.params.perspective_probability * (1 + self.theory_application):
                self.perspective_level = min(1.0, self.perspective_level + 0.1 * (1 + self.theory_understanding))
        else:
            # Non-theory-aware individuals' state updates
            if not self.in_spin:
                if np.random.random() < self.params.spin_frequency:
                    self.in_spin = True
                    self.spin_countdown = self.params.spin_duration
                    self.emotional_state = np.random.uniform(0.5, 1.0)
            else:
                self.spin_countdown -= 1
                if self.spin_countdown <= 0:
                    self.in_spin = False
                    self.emotional_state = 0.0
            
            if np.random.random() < self.params.perspective_probability:
                self.perspective_level = min(1.0, self.perspective_level + 0.1)

    def try_to_educate(self, others):
        if self.has_theory_knowledge:
            for other in others:
                if not other.has_theory_knowledge:  # Only educate those without theory knowledge
                    if other.emotional_state < self.params.receptiveness_threshold:
                        if np.random.random() < self.params.teaching_probability:
                            other.theory_understanding += 0.05
                            other.theory_application += 0.03
                            other.has_theory_knowledge = True  # They gain theory knowledge
                            other.theory_understanding = min(1.0, other.theory_understanding)
                            other.theory_application = min(1.0, other.theory_application)

# Running the conservative simulation
def run_conservative_simulation():
    print("Running conservative simulation with peer learning...")
    params = ConservativeSimulationParams()
    
    # Create two groups: with and without theory knowledge
    aware_group = [Individual(params, has_theory_knowledge=True) for _ in range(params.n_individuals // 2)]
    control_group = [Individual(params, has_theory_knowledge=False) for _ in range(params.n_individuals // 2)]
    
    all_individuals = aware_group + control_group  # Both groups combined
    
    # Track results
    values = np.zeros((params.n_individuals, params.n_timesteps))
    
    # Run simulation
    for t in tqdm(range(params.n_timesteps)):
        # Each individual makes a choice and updates their state
        for i, ind in enumerate(all_individuals):
            choice = ind.make_choice()
            values[i, t] = ind.value
            ind.update_state()
        
        # Theory-aware individuals try to educate others
        for ind in aware_group:
            ind.try_to_educate(all_individuals)
    
    # Plot results and analyze metrics
    plt.figure(figsize=(15, 10))
    
    # Plot individual trajectories
    plt.subplot(2, 1, 1)
    for i in range(params.n_individuals):
        plt.plot(values[i, :], 'b-', alpha=0.05)
    
    # Plot means
    plt.plot(np.mean(values[:len(aware_group)], axis=0), 'b-', linewidth=2, label='Theory-Aware Group')
    plt.plot(np.mean(values[len(aware_group):], axis=0), 'r-', linewidth=2, label='Control Group')
    
    plt.title('Value Trajectories: Theory-Aware vs Control Groups (Conservative Settings)')
    plt.xlabel('Time')
    plt.ylabel('Cumulative Value')
    plt.legend()
    
    # Plot final distributions
    plt.subplot(2, 1, 2)
    plt.hist(values[:len(aware_group), -1], bins=20, alpha=0.5, color='b', label='Theory-Aware Final Values')
    plt.hist(values[len(aware_group):, -1], bins=20, alpha=0.5, color='r', label='Control Final Values')
    plt.title('Distribution of Final Values (Conservative Settings)')
    plt.xlabel('Final Value')
    plt.ylabel('Count')
    plt.legend()
    
    plt.tight_layout()

    # Save the plot as an image file
    plt.savefig('conservative_simulation_results.png')  # Save the figure as a PNG file
    plt.show()
    
    # Calculate and print metrics
    metrics = {
        'aware_mean_final': np.mean(values[:len(aware_group), -1]),
        'control_mean_final': np.mean(values[len(aware_group):, -1]),
        'aware_std_final': np.std(values[:len(aware_group), -1]),
        'control_std_final': np.std(values[len(aware_group):, -1]),
        'aware_positive_ratio': np.mean(values[:len(aware_group), -1] > 0),
        'control_positive_ratio': np.mean(values[len(aware_group):, -1] > 0),
    }
    
    print("\nSimulation Metrics (Conservative Settings):")
    for key, value in metrics.items():
        print(f"{key}: {value:.3f}")
    
    return

if __name__ == "__main__":
    metrics = run_comparative_simulation()
