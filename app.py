from flask import Flask, render_template
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import numpy as np
import plotly.graph_objs as go

# Import the simulation classes and logic
from simulation import run_simulation_with_params, ConservativeSimulationParams

# Initialize Flask
server = Flask(__name__)

# Initialize Dash app on top of Flask
app = Dash(__name__, server=server, url_base_pathname='/dash/')

# Layout for the Dash app (UI components with explanations)
app.layout = html.Div(children=[
    html.H1("Simulation Parameter Adjuster"),
    
    html.Div([
        html.H2("Adjust the Parameters Below:"),
        
        # Number of Individuals
        html.Label("Number of Individuals"),
        dcc.Slider(id='n-individuals', min=100, max=1000, step=100, value=500,
                   marks={i: str(i) for i in range(100, 1100, 100)}),
        dcc.Markdown('''**Explanation**: This controls the number of individuals in the simulation. 
        A higher number of individuals may give more reliable results, but will also take longer to compute.'''),
        
        # Number of Timesteps
        html.Label("Number of Timesteps"),
        dcc.Slider(id='n-timesteps', min=100, max=1000, step=100, value=500,
                   marks={i: str(i) for i in range(100, 1100, 100)}),
        dcc.Markdown('''**Explanation**: The number of timesteps controls how long the simulation runs. 
        More timesteps allow individuals to interact and improve over a longer period.'''),

        # Theory Understanding
        html.Label("Theory Understanding (0 = No understanding, 1 = Full understanding)"),
        dcc.Slider(id='theory-understanding', min=0.0, max=1.0, step=0.1, value=0.5,
                   marks={i/10: str(i/10) for i in range(0, 11)}),
        dcc.Markdown('''**Explanation**: This controls how well the theory-aware individuals understand the theory. 
        A value of **0** means they have **no understanding** (similar to control individuals), while a value of **1** indicates they have **full comprehension**.'''),

        # Theory Application
        html.Label("Theory Application (0 = Not applied, 1 = Fully applied)"),
        dcc.Slider(id='theory-application', min=0.0, max=1.0, step=0.1, value=0.5,
                   marks={i/10: str(i/10) for i in range(0, 11)}),
        dcc.Markdown('''**Explanation**: This affects how well individuals apply their understanding of the theory. 
        A value of **0** means they are not applying the theory at all, while **1** means they are applying it **perfectly**.'''),

        # Teaching Probability
        html.Label("Teaching Probability (0 = Never teaches, 1 = Always teaches)"),
        dcc.Slider(id='teaching-probability', min=0.0, max=1.0, step=0.1, value=0.2,
                   marks={i/10: str(i/10) for i in range(0, 11)}),
        dcc.Markdown('''**Explanation**: This controls the probability that a theory-aware individual will successfully teach another individual. 
        A value of **0** means peer learning does not occur, while a value of **1** means it happens every time a receptive individual is present.'''),

        html.Button("Run Simulation", id='run-simulation', n_clicks=0),
    ], style={'width': '50%', 'margin': 'auto'}),

    # Output container for the simulation results
    html.Div(id='output-container', children=[
        html.H2("Simulation Results"),
        dcc.Graph(id='simulation-graph')
    ])
])

# Callback to run the simulation and update the output graph based on user input
@app.callback(
    Output('simulation-graph', 'figure'),
    [Input('n-individuals', 'value'),
     Input('n-timesteps', 'value'),
     Input('theory-understanding', 'value'),
     Input('theory-application', 'value'),
     Input('teaching-probability', 'value'),
     Input('run-simulation', 'n_clicks')]
)
def update_simulation(n_individuals, n_timesteps, theory_understanding, theory_application, teaching_probability, n_clicks):
    if n_clicks > 0:
        # Run the simulation with adjusted parameters
        params = ConservativeSimulationParams(
            n_individuals=n_individuals,
            n_timesteps=n_timesteps,
            theory_understanding=theory_understanding,
            theory_application=theory_application,
            teaching_probability=teaching_probability
        )
        
        results = run_simulation_with_params(params)
        aware_values, control_values = results

        # Create plotly figure
        figure = go.Figure()

        # Plot mean trajectories
        figure.add_trace(go.Scatter(
            y=np.mean(aware_values, axis=0),
            mode='lines',
            name='Theory-Aware Group',
            line=dict(color='blue')
        ))
        
        figure.add_trace(go.Scatter(
            y=np.mean(control_values, axis=0),
            mode='lines',
            name='Control Group',
            line=dict(color='red')
        ))

        figure.update_layout(
            title="Value Trajectories: Theory-Aware vs Control",
            xaxis_title="Time",
            yaxis_title="Cumulative Value",
            legend_title="Groups"
        )
        return figure
    return go.Figure()

# Flask route for homepage
@server.route('/')
def index():
    return render_template('index.html')

# Start the Flask app with Dash embedded
if __name__ == '__main__':
    app.run_server(debug=True)
