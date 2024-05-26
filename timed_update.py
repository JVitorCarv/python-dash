# Import necessary libraries
import pandas as pd
import numpy as np
import random
import string
from dash import (
    Dash,
    html,
    dash_table,
    dcc,
    callback,
    Output,
    Input,
    clientside_callback,
)
import plotly.express as px
import dash_bootstrap_components as dbc

# Set the number of rows and columns for the DataFrame
num_rows = 100
num_cols = 5

# Global variable to store the DataFrame
global_df = None


# Function to generate random data
def generate_random_data():
    data = {
        "Column1": np.random.randint(0, 100, size=num_rows),
        "Column2": np.random.rand(num_rows),
        "Column3": np.random.choice([True, False], size=num_rows),
        "Column4": np.random.choice(list(string.ascii_uppercase), size=num_rows),
        "Column5": [random.choice(["A", "B", "C"]) for _ in range(num_rows)],
    }
    return pd.DataFrame(data)


# Initialize the Dash app
external_stylesheets = [dbc.themes.ZEPHYR, dbc.icons.FONT_AWESOME]
app = Dash(__name__, external_stylesheets=external_stylesheets)

# Define the layout
app.layout = dbc.Container(
    [
        html.Div(id="random-data-table"),
        dcc.Graph(id="histogram"),
        dcc.Interval(
            id="interval-component-table",
            interval=4 * 1000,
            n_intervals=0,  # in milliseconds
        ),
        dcc.Interval(
            id="interval-component-histogram",
            interval=4 * 1000,
            n_intervals=0,  # in milliseconds
        ),
    ],
    fluid=True,
)


# Callback to update the random data every 4 seconds
@app.callback(
    Output("random-data-table", "children"),
    Input("interval-component-table", "n_intervals"),
)
def update_random_data_table(n_intervals):
    global global_df
    global_df = generate_random_data()  # Update global DataFrame
    return dash_table.DataTable(
        data=global_df.to_dict("records"),
        columns=[{"name": col, "id": col} for col in global_df.columns],
        page_size=12,
        style_table={"overflowX": "auto"},
    )


# Callback to update the histogram every 10 seconds
@app.callback(
    Output("histogram", "figure"), Input("interval-component-histogram", "n_intervals")
)
def update_histogram(n_intervals):
    global global_df
    if global_df is None:
        global_df = generate_random_data()  # Generate data if not already generated
    fig = px.histogram(global_df, x="Column1", title="Histogram of Column1")
    return fig


if __name__ == "__main__":
    app.run_server(debug=True)
