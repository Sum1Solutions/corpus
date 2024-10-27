# Simulation Adjuster App

FIRST OFF - This is totally not working yet...

This is a web-based interactive application that allows users to adjust key variables in a simulation and visualize the results in real-time. The app is built using **Dash**, a Python framework for building web applications, and includes a dynamic UI where users can control parameters such as the number of individuals, timesteps, theory understanding, and application.

## Background Concept

The purpose of the simulation is to compare the behavior and performance of two groups: **theory-aware individuals** and a **control group**. The theory-aware group benefits from understanding and applying a certain "theory" to their decision-making, emotional management, and peer learning, while the control group does not.

### Key Concepts:
- **Theory Understanding**: Controls how well theory-aware individuals understand the theory. A higher value leads to better decision-making.
- **Theory Application**: Determines how effectively theory-aware individuals apply their understanding. A higher value means they apply the theory more consistently.
- **Teaching Probability**: Represents the likelihood of peer learning. A higher value increases the chances of theory-aware individuals teaching others.
- **Number of Individuals**: The number of people participating in the simulation. A higher number may lead to more reliable results but will increase computational time.
- **Number of Timesteps**: The duration of the simulation, where more timesteps allow for longer interactions and decision-making processes.

## Features

- Interactive **sliders** allow users to dynamically adjust the simulation parameters.
- **Real-time visualization** of the simulation's results using interactive graphs.
- A responsive user interface that runs entirely in the web browser.

## How to Run the App

1. **Clone the repository** from GitHub:
   ```bash
   git clone https://github.com/Sum1Solutions/n-equals-1.git
   ```

2. **Set up a virtual environment** to manage dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install the necessary dependencies** listed in the `requirements.txt` file. Run the following command in your terminal:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the app** by executing the `app.py` script:
   ```bash
   python app.py
   ```

5. **Open your browser** and navigate to `http://127.0.0.1:8050/` to interact with the app.

## How to Use the App

1. Adjust the sliders for the following parameters:
   - **Number of Individuals**: Choose how many people will participate in the simulation.
   - **Number of Timesteps**: Set the duration of the simulation.
   - **Theory Understanding**: Select how well the theory-aware individuals comprehend the theory.
   - **Theory Application**: Control how well individuals apply their understanding to their decisions.
   - **Teaching Probability**: Adjust the likelihood of peer learning happening between individuals.

2. Once you've adjusted the parameters, click the **"Run Simulation"** button to start the simulation.

3. The graph below will update to show the **mean performance** of the theory-aware group and the control group over time.

## Technologies Used

- **Dash**: For building the web interface and managing interactive components.
- **Plotly**: For generating dynamic and interactive visualizations.
- **Flask**: For serving the web application.
- **NumPy**: For running simulations and handling numerical calculations.

## Customization

Feel free to modify the simulation logic in the `simulation.py` file or the layout and styling in the `app.py` file. You can also add additional parameters or UI components to the Dash app if needed.

## License

This project is licensed under the MIT License.

