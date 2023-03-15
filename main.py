from datetime import datetime
import pandas as pd
import openpyxl


def print_date(d):
    _ = pd.concat([d.head(), d.tail()])
    print(_)


def yyyy(y):
    y = str(y)
    parts = y.split(".")
    if len(parts) == 3 and len(parts[2]) == 2:
        y = y.split(".")
        y[2] = "20" + y[2]
        y = ".".join(y)
        return y
    else:
        return y


def fraction_to_decimal(fraction_str):
    if type(fraction_str) == str:
        _ = fraction_str.split(" ")
        whole, frac = _[0], _[2]
        frac_num, frac_denom = frac.split('/')
        return int(whole) + int(frac_num) / int(frac_denom)
    elif type(fraction_str) == float:
        return
    else:
        return 0

# df = pd.read_excel("T-Shirt.HD.xlsx", sheet_name="Follow-up")
# date = df["Date"]
#
#
# df['Date'] = df['Date'].apply(yyyy)
# print(df['Date'])
#
# df['Date'] = pd.to_datetime(df['Date'], format="%m.%d.%Y", errors='coerce')
# print(df['Date'])
