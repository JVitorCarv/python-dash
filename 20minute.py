# Import packages
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
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc

df = pd.read_csv(
    "https://raw.githubusercontent.com/plotly/datasets/master/gapminder2007.csv"
)

external_stylesheets = [dbc.themes.ZEPHYR, dbc.icons.FONT_AWESOME]
app = Dash(__name__, external_stylesheets=external_stylesheets)

color_mode_switch = dbc.Row(
    [
        dbc.Label(className="fa fa-moon inline", html_for="switch"),
        dbc.Switch(
            id="switch", value=True, className="d-inline-block ms-1", persistence=True
        ),
        dbc.Label(className="fa fa-sun inline", html_for="switch"),
    ],
    className="align-items-center",
)

header = dbc.Row(
    [
        html.Div(
            "My First App with Data, Graph, and Controls",
            className="text-primary text-center fs-3",
        )
    ]
)

data_selector = dbc.Row(
    [
        dbc.RadioItems(
            options=[{"label": x, "value": x} for x in ["pop", "lifeExp", "gdpPercap"]],
            value="lifeExp",
            inline=True,
            id="radio-buttons",
        )
    ]
)

data_table = dbc.Row(
    [
        dbc.Col(
            [
                dash_table.DataTable(
                    data=df.to_dict("records"),
                    page_size=12,
                    style_table={"overflowX": "auto"},
                )
            ],
            width=6,
        ),
        dbc.Col([dcc.Graph(figure={}, id="graph-placeholder")], width=6),
    ]
)

app.layout = dbc.Container(
    [
        header,
        data_selector,
        data_table,
        color_mode_switch,
    ],
    fluid=True,
)

clientside_callback(
    """
    (switchOn) => {
       document.documentElement.setAttribute("data-bs-theme", switchOn ? "light" : "dark"); 
       return window.dash_clientside.no_update
    }
    """,
    Output("switch", "id"),
    Input("switch", "value"),
)


@callback(
    Output(component_id="graph-placeholder", component_property="figure"),
    Input(component_id="radio-buttons", component_property="value"),
)
def update_graph(col_chosen):
    fig = px.histogram(df, x="continent", y=col_chosen, histfunc="avg")
    return fig


if __name__ == "__main__":
    app.run(debug=True)
