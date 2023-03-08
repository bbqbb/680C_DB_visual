import dash
from dash import dcc, html, Dash
from main import yyyy
import pandas as pd
from dash.dependencies import Output, Input
import openpyxl

# data = pd.read_excel("T-Shirt.HD.xlsx", sheet_name="Trial-Run")
# data['Date'] = data['Date'].str.extract(r'(\d{1,2}\.\d{1,2}\.\d{2,4})')
# data['Date'] = data['Date'].apply(yyyy)
# data['Date'] = pd.to_datetime(data['Date'], format="%m.%d.%Y", errors='coerce')
# data.sort_values("Date", inplace=True)
data = pd.read_csv("avocado.csv")
data["Date"] = pd.to_datetime(data["Date"], format="%Y-%m-%d")
data.sort_values("Date", inplace=True)

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
    style={'display': 'flex', 'justify-content': 'center', 'align-items': 'center'},
    children=[html.Div(children=[
        html.Div(children=[
            html.A(html.Img(src="/assets/inteplast.png"),
                   href="https://www.inteplast.com/"),
            html.H1("Technical Data"),
            dcc.DatePickerRange(id="date_range",
                                min_date_allowed=data.Date.min().date(),
                                max_date_allowed=data.Date.max().date(),
                                start_date=data.Date.min().date(),
                                end_date=data.Date.max().date(),
                                )
        ]
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
        "data": [
            {
                "x": filter_data["Date"],
                "y": filter_data["AveragePrice"],
                "type": "lines",
                "hovertemplate": "$%{y:.2f}<extra></extra>",
            },
        ],
        "layout": {
            "title": {
                "text": "Average Price of Avocados",
                "x": 0.5,
                "xanchor": "left",
            },
            "xaxis": {"fixedrange": True},
            "yaxis": {"tickprefix": "$", "fixedrange": True},
            "colorway": ["#17B897"],
        },
    }
    return property_chart


if __name__ == "__main__":
    app.run_server(debug=True, port=1234)
