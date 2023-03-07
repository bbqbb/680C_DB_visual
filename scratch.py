import pandas as pd

df = pd.DataFrame({
    'Date': ['01.01.22', '01.01.2022', '12.31.2021', '1.1.22', '31.12.2021', '31.12.2021-1234', "2.1"]
})
df['Date'] = df['Date'].str.extract(r'(\d{1,2}\.\d{1,2}\.\d{2,4})')


# df['Date'] = pd.to_datetime(df['Date'], format="%m.%d.%Y", errors='coerce')
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


df['Date'] = df['Date'].apply(yyyy)

print(df['Date'])
