import pandas as pd
import matplotlib.pyplot as plt
import os

cwd = os.getcwd()
data_file = os.path.join(cwd, "control_signals_analysis", "control_signals.csv")

df = pd.read_csv(data_file, names=["col"])

df = df.col.str.split(" ", expand=True)

df.columns = ["index", "time", "sensor", "light_type", "control"]

df.index = pd.to_datetime(df.time, unit="s", utc=True)

df.index = df.index.tz_convert("Asia/Singapore")

df = df.astype({'control': 'int32'})

plt.figure()

for light in df["light_type"].unique():

    _df = df[df["light_type"] == light]

    _df["control"].plot(label=light)

plt.legend()
plt.show()
