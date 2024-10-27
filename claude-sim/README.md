# Conservative Simulation App

This is a Python-based application that simulates the behavior and interactions of individuals in a controlled environment using conservative parameters. The purpose of the simulation is to explore how different factors, such as emotional states, peer learning, and theory application, affect the cumulative performance of individuals over time.

## Background Concept

The simulation models the behavior of two groups of individuals: **theory-aware individuals** and a **control group**. The **theory-aware individuals** benefit from understanding and applying a specific theory, which helps them manage emotional states, gain perspective, and learn from others. The **control group** does not have this knowledge and relies more heavily on randomness and emotional influence.

The conservative settings used in this simulation represent individuals with limited understanding and application of the theory, making the results more subtle and indicative of slight improvements over time.

### Key Concepts:
- **Theory Understanding**: Represents how well theory-aware individuals understand the theory. A higher value leads to better decision-making.
- **Theory Application**: Indicates how effectively individuals apply their understanding of the theory. A higher value means they consistently use their knowledge to make better choices.
- **Teaching Probability**: The likelihood that a theory-aware individual will successfully educate a non-aware individual, depending on their emotional state.
- **Emotional State and Perspective**: Each individual has an emotional state that affects their decision-making, and theory-aware individuals are better at managing these states and gaining perspective over time.

## Features

- **Simulated Interactions**: Models the choices and interactions of individuals over a series of timesteps.
- **Visualization**: Uses **matplotlib** to plot the results, including individual trajectories and final value distributions.
- **Conservative Parameters**: Simulates conservative settings where individuals have limited knowledge and learning capabilities.

## How to Run the App

1. **Set up a virtual environment** to manage dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

2. **Install the necessary dependencies** using `pip`. Run the following command:
   ```bash
   pip install numpy matplotlib tqdm
   ```

3. **Run the script** to execute the simulation:
   ```bash
   python conservative_simulation.py
   ```

4. **View the results**: The script will generate plots that show the value trajectories of theory-aware individuals vs. the control group, as well as the final value distributions.

## How to Interpret the Results

- **Value Trajectories Plot**: Shows the cumulative value for each individual over time. The blue lines represent the **theory-aware group**, and the red lines represent the **control group**. The solid lines show the mean performance of each group.
- **Final Value Distribution Plot**: Displays the distribution of final cumulative values for both groups, highlighting differences in performance.
- **Simulation Metrics**: At the end of the simulation, metrics such as the average final value, standard deviation, and the ratio of positive outcomes for each group are printed to the console.

## Technologies Used

- **Python**: The core programming language for the simulation.
- **NumPy**: For numerical operations and data handling.
- **Matplotlib**: For visualizing the results of the simulation.
- **tqdm**: For displaying progress bars during the simulation.

## Customization

You can modify the parameters of the simulation, such as the number of individuals, timesteps, and learning rates, by adjusting the values in the `ConservativeSimulationParams` class. This allows you to explore different scenarios and understand how changes affect individual and group behavior.

## License

This project is licensed under the MIT License.

