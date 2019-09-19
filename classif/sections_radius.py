import warnings
from platform import system as getsys

import easygui
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

warnings.filterwarnings('ignore')
sep = "\\"
if getsys() == "Linux":
    sep = "/"

k = 5  # dist = 1 meter/k
persentile = 0.1
begin_quantile = 0.03

file_name = easygui.fileopenbox("select tree to process")
df = pd.read_csv(file_name, delimiter=' ', header=None)
df.columns = ['x', 'y', 'z', 'laser']
df.drop('laser', 1, inplace=True)
df['x'] = np.abs(df['x'] - df['x'].mean())
df['y'] = np.abs(df['y'] - df['y'].mean())
df['z'] = (df['z'] - df['z'].quantile(0.03)) * k

df['z'] = df['z'].round(0)
df['xy'] = 0.707 * df['x'] + 0.707 * df['y']
df['xxy'] = 0.98 * df['x'] + 0.17 * df['y']
df['xyy'] = 0.34 * df['x'] + 0.94 * df['y']
df['xxxy'] = 0.5 * df['x'] + 0.87 * df['y']
df['xyyy'] = 0.64 * df['x'] + 0.77 * df['y']
df['xxxxy'] = 0.77 * df['x'] + 0.64 * df['y']
df['xyyyy'] = 0.87 * df['x'] + 0.5 * df['y']

out_df = pd.DataFrame(columns=['z', 'xy', 'xxy', 'xyy', 'xxxy', 'xyyy', 'xxxxy', 'xyyyy'])

for i in range(int(df['z'].min()), int(df['z'].max())):
    ndf = df[df["z"] == i]
    height = i
    ndf = pd.DataFrame(ndf.quantile(1 - persentile).subtract(ndf.quantile(persentile))).T.round(3)
    ndf.at[0, 'z'] = height
    ndf = ndf[['z', 'xy', 'xxy', 'xyy', 'xxxy', 'xyyy', 'xxxxy', 'xyyyy']]
    out_df = out_df.append(ndf)

plt.figure(figsize=(15, 10))
plt.plot(out_df["z"], out_df['xy'], label="xy")
# plt.plot(out_df["z"], out_df['xxy'], label="xxy")
plt.plot(out_df["z"], out_df['xyy'], label="xyy")
plt.plot(out_df["z"], out_df['xxxy'], label="xxxy")
plt.plot(out_df["z"], out_df['xyyy'], label="xyyy")
plt.plot(out_df["z"], out_df['xxxxy'], label="xxxxy")
plt.plot(out_df["z"], out_df['xyyyy'], label="xyyyy")

plt.ylabel("Diameter of tree")
plt.xlabel(str(round(1.0 / k, 3)) + " *10^-1 M")
plt.title(file_name.split(sep)[-1] + " file at percentile " + str(persentile))
plt.legend()
plt.show()

out_df.to_csv(file_name.replace(".", "_processed."), index=False)
