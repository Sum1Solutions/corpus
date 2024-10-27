from flask import Flask, render_template
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import numpy as np
import plotly.graph_objs as go
import scipy.stats as stats

# Import the simulation classes and logic
from simulation import run_simulation_with_params, ConservativeSimulationParams

# Initialize Flask
server = Flask(__name__)

# Initialize Dash app on top of Flask
app = Dash(__name__, server=server, url_base_pathname='/dash/')

# Layout for the Dash app (UI components with explanations)
app.layout = html.Div(children=[
    html.H1("Simulation Adjuster App", style={'textAlign': 'center', 'margin-bottom': '30px'}),

    html.Div([
        html.Div([
            html.Label("Number of Individuals", style={'font-weight': 'bold'}),
            dcc.Slider(id='n-individuals', min=100, max=1000, step=100, value=500,
                       marks={i: str(i) for i in range(100, 1100, 100)}),
            dcc.Markdown("""**Explanation**: Controls the number of individuals in the simulation.
            A higher number may provide more reliable results, but takes longer to compute.""")
        ], style={'width': '90%', 'margin': 'auto', 'padding': '15px', 'box-shadow': '0 4px 8px 0 rgba(0, 0, 0, 0.2)', 'border-radius': '10px', 'margin-bottom': '20px'}),

        html.Div([
            html.Label("Number of Timesteps", style={'font-weight': 'bold'}),
            dcc.Slider(id='n-timesteps', min=100, max=1000, step=100, value=500,
                       marks={i: str(i) for i in range(100, 1100, 100)}),
            dcc.Markdown("""**Explanation**: Sets the number of timesteps, affecting the duration of the simulation.""")
        ], style={'width': '90%', 'margin': 'auto', 'padding': '15px', 'box-shadow': '0 4px 8px 0 rgba(0, 0, 0, 0.2)', 'border-radius': '10px', 'margin-bottom': '20px'}),

        html.Div([
            html.Label("Theory Understanding (0 = No understanding, 1 = Full understanding)", style={'font-weight': 'bold'}),
            dcc.Slider(id='theory-understanding', min=0.0, max=1.0, step=0.1, value=0.5,
                       marks={i/10: str(i/10) for i in range(0, 11)}),
            dcc.Markdown("""**Explanation**: Controls how well individuals understand the theory.""")
        ], style={'width': '90%', 'margin': 'auto', 'padding': '15px', 'box-shadow': '0 4px 8px 0 rgba(0, 0, 0, 0.2)', 'border-radius': '10px', 'margin-bottom': '20px'}),

        html.Div([
            html.Label("Theory Application (0 = Not applied, 1 = Fully applied)", style={'font-weight': 'bold'}),
            dcc.Slider(id='theory-application', min=0.0, max=1.0, step=0.1, value=0.5,
                       marks={i/10: str(i/10) for i in range(0, 11)}),
            dcc.Markdown("""**Explanation**: Controls how effectively individuals apply their theoretical understanding.""")
        ], style={'width': '90%', 'margin': 'auto', 'padding': '15px', 'box-shadow': '0 4px 8px 0 rgba(0, 0, 0, 0.2)', 'border-radius': '10px', 'margin-bottom': '20px'}),

        html.Div([
            html.Label("Teaching Probability (0 = Never teaches, 1 = Always teaches)", style={'font-weight': 'bold'}),
            dcc.Slider(id='teaching-probability', min=0.0, max=1.0, step=0.1, value=0.2,
                       marks={i/10: str(i/10) for i in range(0, 11)}),
            dcc.Markdown("""**Explanation**: Controls the likelihood of peer learning events.""")
        ], style={'width': '90%', 'margin': 'auto', 'padding': '15px', 'box-shadow': '0 4px 8px 0 rgba(0, 0, 0, 0.2)', 'border-radius': '10px', 'margin-bottom': '20px'}),

        html.Div([
            html.Button("Run Simulation", id='run-simulation', n_clicks=0, style={'margin-top': '20px', 'padding': '10px 20px', 'font-size': '16px', 'border-radius': '10px', 'background-color': '#007bff', 'color': 'white', 'border': 'none', 'cursor': 'pointer'})
        ], style={'width': '100%', 'textAlign': 'center', 'padding': '20px'})
    ], style={'width': '90%', 'margin': 'auto'}),

    html.Div(id='results-section', children=[
        html.H2("Simulation Results", style={'textAlign': 'center', 'margin-top': '40px'}),
        html.Div([
            dcc.Graph(id='simulation-graph', style={'display': 'inline-block', 'width': '48%', 'padding': '10px'}),
            dcc.Graph(id='distribution-graph', style={'display': 'inline-block', 'width': '48%', 'padding': '10px'})
        ], style={'width': '100%', 'margin': 'auto', 'textAlign': 'center'})
    ], style={'padding': '20px'})
])

# Callback to run the simulation and update the output graphs based on user input
@app.callback(
    [Output('simulation-graph', 'figure'), Output('distribution-graph', 'figure')],
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

        # Statistical analysis (p-value)
        t_stat, p_value = stats.ttest_ind(aware_values[:, -1], control_values[:, -1])
        p_value_text = f"P-value: {p_value:.4f}"

        # Create plotly figure for value trajectories
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
            legend_title="Groups",
            annotations=[
                dict(
                    x=0.5,
                    y=1.1,
                    xref='paper',
                    yref='paper',
                    text=p_value_text,
                    showarrow=False,
                    font=dict(size=12)
                )
            ]
        )

        # Create plotly figure for distribution of final values
        distribution_figure = go.Figure()
        distribution_figure.add_trace(go.Histogram(
            x=aware_values[:, -1],
            name='Theory-Aware Group',
            opacity=0.75,
            marker=dict(color='blue')
        ))
        distribution_figure.add_trace(go.Histogram(
            x=control_values[:, -1],
            name='Control Group',
            opacity=0.75,
            marker=dict(color='red')
        ))

        distribution_figure.update_layout(
            title="Distribution of Final Values: Theory-Aware vs Control",
            xaxis_title="Final Value",
            yaxis_title="Frequency",
            legend_title="Groups",
            barmode='overlay',
            annotations=[
                dict(
                    x=0.5,
                    y=1.1,
                    xref='paper',
                    yref='paper',
                    text=p_value_text,
                    showarrow=False,
                    font=dict(size=12)
                )
            ]
        )

        return figure, distribution_figure
    return go.Figure(), go.Figure()

# Flask route for homepage
@server.route('/')
def index():
    return render_template('index.html')

# Start the Flask app with Dash embedded
if __name__ == '__main__':
    app.run_server(debug=True)
