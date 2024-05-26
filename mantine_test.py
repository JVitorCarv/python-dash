# Import packages
from dash import Dash, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px
import dash_mantine_components as dmc

DATA_URL = "https://raw.githubusercontent.com/plotly/datasets/master/gapminder2007.csv"

df = pd.read_csv(DATA_URL)

app = Dash()

app.layout = dmc.MantineProvider(
    [
        dmc.Title(
            "My First App with Data, Graph, and Controls", color="blue", size="h3"
        ),
        dmc.RadioGroup(
            [dmc.Radio(i, value=i) for i in ["pop", "lifeExp", "gdpPercap"]],
            id="my-dmc-radio-item",
            value="lifeExp",
            size="sm",
        ),
        dmc.Grid(
            [
                dmc.Col(
                    [
                        dash_table.DataTable(
                            data=df.to_dict("records"),
                            page_size=12,
                            style_table={"overflowX": "auto"},
                        )
                    ],
                    span=6,
                ),
                dmc.Col([dcc.Graph(figure={}, id="graph-placeholder")], span=6),
            ]
        ),
    ],
    fluid=True,
)


@callback(
    Output(component_id="graph-placeholder", component_property="figure"),
    Input(component_id="my-dmc-radio-item", component_property="value"),
)
def update_graph(col_chosen):
    fig = px.histogram(df, x="continent", y=col_chosen, histfunc="avg")
    return fig


# Run the App
if __name__ == "__main__":
    app.run(debug=True)
