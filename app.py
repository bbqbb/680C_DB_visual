import dash
from dash import dcc, html, Dash
from main import yyyy
import pandas as pd
from dash.dependencies import Output, Input

data = pd.read_excel("T-Shirt.HD.xlsx", sheet_name="Follow-up")
data['Date'] = data['Date'].str.extract(r'(\d{1,2}\.\d{1,2}\.\d{2,4})')
data['Date'] = data['Date'].apply(yyyy)
data['Date'] = pd.to_datetime(data['Date'], format="%m.%d.%Y", errors='coerce')

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
            dcc.DatePickerRange(id="date_range")
        ]
        )
    ]
    ),
        html.Div(
            children=[
                html.Div(
                    children=[
                        dcc.Graph(id="chart"),
                    ], className="card"
                )
            ], className="wrapper"
        )
    ]
)
@app.callback()
    [Output("chart")]

if __name__ == "__main__":
    app.run_server(debug=True)
