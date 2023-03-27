import dash
from dash import dcc, html, Dash
from main import yyyy, fraction_to_decimal
import pandas as pd
from dash.dependencies import Output, Input
import numpy as np
import openpyxl

data = pd.read_excel("T-Shirt.HD - Copy.xlsx", sheet_name="Trial-Run")
data['Date'] = data['Date'].str.extract(r'(\d{1,2}\.\d{1,2}\.\d{2,4})')
data['Date'] = data['Date'].apply(yyyy)
# data['Layflat'] = data['Layflat'].apply(fraction_to_decimal)
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
                                     'All', "HD", "LDPE"
                                 ],

                                 style={'width': '75px'})
                ),
                html.Div(
                    children=[
                        dcc.Dropdown(
                            id="color_filter",
                            placeholder="Color",
                            options=[{'label': 'All', 'value': 'All'}]
                                    + [{"label": color, "value": color}
                                       for color in data["Color"].unique()]
                            ,
                            style={'width': '120px'}
                        )
                    ]
                ),
                html.Div(
                    children=[
                        dcc.Dropdown(
                            id="line_filter",
                            multi=True,
                            placeholder="Line Numer",
                            options=[{'label': 'All', 'value': 'All'}]
                                    + [{"label": line, "value": line}
                                       for line in data["LineNumber"].unique()]
                        )
                    ]
                ),
                html.Div(
                    children=[
                        dcc.Input(id="layflat_min",
                                  type="number",
                                  # value=0,
                                  placeholder="LayFlat min"),
                        dcc.Input(id="layflat_max",
                                  type="number",
                                  # value=100,
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
                        html.Div(
                            children=[
                                dcc.Graph(
                                    id="md_tear", config={"displayModeBar": True}),
                            ], className="card"
                        ),
                        # md_tear
                        html.Div(
                            children=[
                                dcc.Graph(
                                    id="td_tear", config={"displayModeBar": True}),
                            ], className="card"
                        ),
                        # md_tensil
                        html.Div(
                            children=[
                                dcc.Graph(
                                    id="md_tensil", config={"displayModeBar": True}),
                            ], className="card"
                        ),
                    ], className="wrapper"
                )
            ]
        )
    ]
)


@app.callback(
    [Output('md_tear', 'figure'),
     Output('td_tear', 'figure'),
     Output('md_tensil', 'figure')],
    [Input("date_range", "start_date"),
     Input("date_range", "end_date"),
     Input("resin", "value"),
     Input("color_filter", "value"),
     Input('line_filter', 'value')
     # Input("layflat_min", "value"),
     # Input("layflat_max", "value"),
     ]
)
def update_chart(start_date, end_date, resin, color, lines):
    if resin == 'All' or resin is None:
        resin = 'HD' or 'LDPE'
    if color == 'All' or color is None:
        color = list(data['Color'].unique())
    else:
        color = [color]
    if lines is None:
        line = list(data['LineNumber'].unique())
    elif 'All' in lines:
        line = list(data['LineNumber'].unique())
    elif type(lines) == list:
        line = lines
    else:
        line = [lines]
    # if layflat_min and layflat_max is None:

    mask = (
            (data.Date >= start_date) & (data.Date <= end_date)
            # & (data.Layflat >= 10)& (data.Layflat <= 40)
            & (data.Resin == resin)
            & (data.Color.isin(color))
            & (data.LineNumber.isin(line))
    )
    filter_data = data.loc[mask]
    md_tear_figure = {
        "data": [
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
            # "xaxis": {"fixedrange": True},
            # "yaxis": {"fixedrange": True},
            "colorway": ["#17B897"]
        }
    }

    td_tear_figure = {
        "data": [
            {
                "x": filter_data["Date"],
                "y": filter_data["td_tear"],
                "type": "Line",
                "hovertemplate": "%{y:.2f}<extra></extra>",
            },
        ],
        "layout": {
            "title": {
                "text": "TD Tear",
                "x": 0.5,
                "xanchor": "left",
            },
            # "xaxis": {"fixedrange": True},
            # "yaxis": {"fixedrange": True},
            "colorway": ["#17B897"]
        }
    }
    md_tensil_figure = {
        "data": [
            {
                "x": filter_data["Date"],
                "y": filter_data["md_tensil (Lb/in)"],
                "type": "Line",
                "hovertemplate": "%{y:.2f}<extra></extra>",
            },
        ],
        "layout": {
            "title": {
                "text": "MD Tensil",
                "x": 0.5,
                "xanchor": "left",
            },
            # "xaxis": {"fixedrange": True},
            # "yaxis": {"fixedrange": True},
            "colorway": ["#17B897"]
        }
    }
    return md_tear_figure, td_tear_figure, md_tensil_figure


if __name__ == "__main__":
    app.run_server(debug=True, port=1235)
