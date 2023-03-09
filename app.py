import dash
from dash import dcc, html, Dash
from main import yyyy
import pandas as pd
from dash.dependencies import Output, Input
import numpy as np
import openpyxl

data = pd.read_excel("T-Shirt.HD - Copy.xlsx", sheet_name="Trial-Run")
data['Date'] = data['Date'].str.extract(r'(\d{1,2}\.\d{1,2}\.\d{2,4})')
data['Date'] = data['Date'].apply(yyyy)
data['Date'] = pd.to_datetime(data['Date'], format="%m.%d.%Y", errors='coerce')
data.sort_values("Date", inplace=True)
# data = pd.read_csv("avocado.csv")
# data["Date"] = pd.to_datetime(data["Date"], format="%Y-%m-%d")
# data.sort_values("Date", inplace=True)
external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
                "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    }
]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = '680C-DB'
app.layout = html.Div(
    children=[
        html.Div(
            style={'display': 'flex', 'justify-content': 'center', 'align-items': 'center'},
            children=[
                html.Div(
                    children=[
                        html.Div(children=[
                            html.A(html.Img(src="/assets/inteplast.png"),
                                   href="https://www.inteplast.com/", className="header"),
                            html.H1("Technical Data"),

                        ]
                        )
                    ]
                )
            ]
        ), html.Div(
            style={'display': 'flex', 'justify-content': 'center', 'align-items': 'center'},
            children=[
                html.Div(
                    children=[
                        dcc.DatePickerRange(id="date_range",
                                            min_date_allowed=data.Date.min().date(),
                                            max_date_allowed=data.Date.max().date(),
                                            start_date=data.Date.min().date(),
                                            end_date=data.Date.max().date(),
                                            ),
                    ]
                ),
                html.Div(
                    dcc.Dropdown(id="resin",
                                 placeholder="Resin",
                                 options=[
                                     "HD", "LDPE"
                                 ],
                                 style={'width': '75px'})
                ),
                html.Div(
                    children=[
                        dcc.Dropdown(
                            id="color_filter",
                            placeholder="Color",
                            options=[
                                {"label": color, "value": color}
                                for color in data["Color"].unique()
                            ],
                            style={'width': '120px'}
                        )
                    ]
                ),
                html.Div(
                    children=[
                        dcc.Dropdown(
                            id="line-filter",
                            multi=True, placeholder="Line Numer",
                            options=[
                                {"label": line, "value": line}
                                for line in data["LineNumber"].unique()
                            ],
                        )
                    ]
                ),
                html.Div(
                    children=[
                        dcc.Input(id="layFlat_min",
                                  type="number",
                                  placeholder="LayFlat min"),
                        dcc.Input(id="layFlat_max",
                                  type="number",
                                  placeholder="LayFlat max")
                    ],
                    style={
                        'display': 'flex',
                        'flex-direction': 'column',
                        'width': '100px'
                    }
                )
            ]
        ),
        html.Div(
            children=[
                html.Div(
                    children=[
                        dcc.Graph(id="chart", config={"displayModeBar": False}),
                    ], className="card"
                )
            ], className="wrapper"
        )
    ]
)


@app.callback(
    [Output("chart", "figure")],
    [Input("date_range", "start_date"),
     Input("date_range", "end_date")]
)
def update_chart(start_date, end_date):
    mask = ((data.Date >= start_date) & (data.Date <= end_date))
    filter_data = data.loc[mask]
    property_chart = {
        "date": [
            {
                "x": filter_data["Date"],
                "y": filter_data["md_tear"],
                "type": "Line",
                "hovertemplate": "%{y:.2f}<extra></extra>",
            },
        ],
        "layout": {
            "title": {
                "text": "MD Tear",
                "x": 0.5,
                "xanchor": "left",
            },
            "xaxis": {"fixedrange": True},
            "yaxis": {"tickprefix": "$", "fixedrange": True},
            "colorway": ["#17B897"]
        }
    }
    return property_chart


if __name__ == "__main__":
    app.run_server(debug=True, port=1234)
