import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("ultrasonic_calibration.csv", names=["col"])

df = df.col.str.split(" ", expand=True)

df.columns = ["index", "time", "dist", "mean", "std"]

df.index = pd.to_datetime(df.time, unit="s", utc=True)

df.index = df.index.tz_convert("Asia/Singapore")

df = df.astype("float")

plt.figure()
df["std"].plot()
plt.axhline(y=0.02, color="r", linestyle="-")
plt.show()

df["std"].describe()
