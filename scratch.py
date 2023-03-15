import pandas as pd
from main import yyyy
#
# df = pd.DataFrame({
#     'Date': ['01.01.22', '01.01.2022', '12.31.2021', '1.1.22', '31.12.2021', '31.12.2021-1234', "2.1"]
# })
# df['Date'] = df['Date'].str.extract(r'(\d{1,2}\.\d{1,2}\.\d{2,4})')
#
#
# # df['Date'] = pd.to_datetime(df['Date'], format="%m.%d.%Y", errors='coerce')
# def yyyy(y):
#     y = str(y)
#     parts = y.split(".")
#     if len(parts) == 3 and len(parts[2]) == 2:
#         y = y.split(".")
#         y[2] = "20" + y[2]
#         y = ".".join(y)
#         return y
#     else:
#         return y
#
#
# df['Date'] = df['Date'].apply(yyyy)
#
# print(df['Date'])

import dash
from dash import dcc, html
import pandas as pd

data = pd.read_excel("T-Shirt.HD - Copy.xlsx", sheet_name="Trial-Run")
data['Date'] = pd.to_datetime(data['Date'], format="%m.%d.%Y", errors='coerce')
data.sort_values("Date", inplace=True)

start_date = '2013-04-11 00:00:00'
end_date = data.Date.max()
mask = (data.Date >= start_date) & (data.Date <= end_date)
filter_data = data.loc[mask]

chart_data = {'x': filter_data['Date'], 'y': filter_data['md_tear'], 'type': 'scatter'}

app = dash.Dash(__name__)

app.layout = html.Div(children=[
    dcc.Graph(
        id='my-chart',
        figure={
            'data': [chart_data],
            'layout': {
                'title': 'My Chart',
                'xaxis': {'title': 'X Axis Label'},
                'yaxis': {'title': 'Y Axis Label'}
            }
        }
    )
])

if __name__ == '__main__':
    app.run_server(debug=True, port=7777)
