import os
import warnings
from glob import glob
from platform import system as getsys

import easygui
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.spatial import ConvexHull

warnings.filterwarnings('ignore')
sep = "\\"
if getsys() == "Linux":
    sep = "/"

k = 20.0  # dist = 1 meter/k
persentile = 0.1
begin_quantile = 0.03
begin_dist = 0.9
end_dist = 1.8

dir_name = easygui.diropenbox("select tree to process")
out_dir = dir_name + sep + "processed"

if not os.path.exists(out_dir):
    os.makedirs(out_dir)

for file_name in glob(dir_name + sep + "*.txt"):
    df = pd.read_csv(file_name, delimiter=' ', header=None)
    df.columns = ['x', 'y', 'z', 'laser']
    df.drop('laser', 1, inplace=True)
    df['x'] = df['x'] - df['x'].mean()
    df['y'] = df['y'] - df['y'].mean()
    df['z'] = (df['z'] - df['z'].quantile(0.02))
    df = df[(begin_dist < df['z']) & (df['z'] < end_dist)]
    df['z'] *= k

    df['z'] = df['z'].round(0)
    df['xy'] = 0.707 * df['x'] + 0.707 * df['y']
    df['xxy'] = 0.98 * df['x'] + 0.17 * df['y']
    df['xyy'] = 0.34 * df['x'] + 0.94 * df['y']
    df['xxxy'] = 0.5 * df['x'] + 0.87 * df['y']
    df['xyyy'] = 0.64 * df['x'] + 0.77 * df['y']
    df['xxxxy'] = 0.77 * df['x'] + 0.64 * df['y']
    df['xyyyy'] = 0.87 * df['x'] + 0.5 * df['y']

    out_df = pd.DataFrame(
        columns=['z', 'xy', 'xxy', 'xyy', 'xxxy', 'xyyy', 'xxxxy', 'xyyyy', 'hull_volume', 'hull_area'])

    for i in range(int(df['z'].min()), int(df['z'].max())):
        ndf = df[df["z"] == i]
        hull_volume = 0
        hull_area = 0
        try:
            hull = ConvexHull(ndf[['x', 'y']])
            hull_volume = hull.volume
            hull_area = hull.area

            points = np.array(ndf[['x', 'y']])
            if i % 4 == 0:
                plt.plot(ndf['x'], ndf['y'], 'o')
                for simplex in hull.simplices:
                    plt.plot(points[simplex, 0], points[simplex, 1], 'k-')
                plt.plot(points[hull.vertices, 0], points[hull.vertices, 1], 'r--', lw=2)
                plt.plot(points[hull.vertices[0], 0], points[hull.vertices[0], 1], 'ro')
                plt.show()

        except Exception:
            pass

        height = i
        ndf = pd.DataFrame(ndf.quantile(1 - persentile).subtract(ndf.quantile(persentile))).T.round(3)
        ndf.at[0, 'z'] = height
        ndf = ndf[['z', 'xy', 'xxy', 'xyy', 'xxxy', 'xyyy', 'xxxxy', 'xyyyy']]
        ndf["hull_volume"] = round(hull_volume, 5)
        ndf["hull_area"] = round(hull_area, 5)
        out_df = out_df.append(ndf)
    out_df['z'] /= k

    # plots
    # plt.figure(figsize=(15, 10))
    # plt.plot(out_df["z"], out_df['xy'], label="xy")
    # # plt.plot(out_df["z"], out_df['xxy'], label="xxy")
    # plt.plot(out_df["z"], out_df['xyy'], label="xyy")
    # plt.plot(out_df["z"], out_df['xxxy'], label="xxxy")
    # plt.plot(out_df["z"], out_df['xyyy'], label="xyyy")
    # plt.plot(out_df["z"], out_df['xxxxy'], label="xxxxy")
    # plt.plot(out_df["z"], out_df['xyyyy'], label="xyyyy")
    #
    # plt.ylabel("Diameter of tree")
    # plt.xlabel(str(round(1.0 / k, 3)) + " *10^-1 M")
    # plt.title(file_name.split(sep)[-1] + " file at percentile " + str(persentile))
    # plt.legend()
    # plt.show()

    out_df.to_csv(out_dir + sep + file_name.split(sep)[-1], index=False)
