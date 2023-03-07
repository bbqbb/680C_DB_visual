from datetime import datetime
import pandas as pd
import openpyxl


def print_date(d):
    _ = pd.concat([d.head(), d.tail()])
    print(_)


df = pd.read_excel("T-Shirt.HD.xlsx", sheet_name="Trial-Run")
date = df["Date"]
# 1
print_date(date)

date = pd.to_datetime(date, format="%m.%d.%Y", errors="coerce")
# 2
print_date(date)
print("error", date.isna().sum())


