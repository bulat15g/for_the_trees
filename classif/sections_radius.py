import os
import warnings
from glob import glob
from math import sin, cos
from platform import system as getsys

import easygui
import numpy as np
import pandas as pd
from scipy.spatial import ConvexHull

# cross platforms support
warnings.filterwarnings('ignore')
sep = "\\"
if getsys() == "Linux":
    sep = "/"

######################################################################
section_distance = 0.1  # METERS 0.1 = 10 santimeters
persentile = 0.00
begin_dist = 0.9
end_dist = 1.7
angles = [x for x in range(0, 171, 10)]
medians = [x for x in angles if x < 90]
enable_dz_shift = False
######################################################################
# folder
dir_name = easygui.diropenbox("select tree to process")
out_dir = dir_name + sep + "processed"

# scale and initialization arrays
section_distance = 1 / section_distance
angle_names = [str(x) for x in angles]
all_stats_dict = {}
trees_means_global_array = []
out_table = [["name", "mean", "std", "MMmean", "MMstd"]]

if not os.path.exists(out_dir):
    os.makedirs(out_dir)

for file_name in glob(dir_name + sep + "*.txt"):
    print("going to file ", file_name)
    # read,shift and scale values
    only_file_name = file_name.split(sep)[-1]
    df = pd.read_csv(file_name, delimiter=' ', header=None)
    df.columns = ['x', 'y', 'z', 'laser']
    df.drop('laser', 1, inplace=True)
    df['x'] = df['x'] - df['x'].mean()
    df['y'] = df['y'] - df['y'].mean()
    if enable_dz_shift: df['z'] = (df['z'] - df['z'].quantile(0.015))
    df = df[(begin_dist < df['z']) & (df['z'] < end_dist)]
    df['z'] *= section_distance
    # get projections values
    df['z'] = df['z'].round(0)
    for x in enumerate(angles):
        df[angle_names[x[0]]] = cos(x[1]) * df['x'] + sin(x[1]) * df['y']

    out_df = pd.DataFrame(
        columns=['z'] + angle_names + ['hull_volume', 'hull_area'])

    this_tree_min_max = []
    for i in range(int(df['z'].min()), int(df['z'].max())):
        ndf = df[df["z"] == i]
        hull_volume = 0
        hull_area = 0
        try:
            hull = ConvexHull(ndf[['x', 'y']])
            hull_volume = hull.volume
            hull_area = hull.area
        except Exception:
            pass

        height = i
        ndf = pd.DataFrame(ndf.quantile(1 - persentile).subtract(ndf.quantile(persentile))).T.round(3)
        ndf.at[0, 'z'] = height
        ndf = ndf[['z'] + angle_names]
        ndf["hull_volume"] = round(hull_volume, 5)
        ndf["hull_area"] = round(hull_area, 5)
        out_df = out_df.append(ndf)
        # add min max metrics
        this_tree_min_max.append((np.max(ndf[angle_names].to_numpy()) + np.min(ndf[angle_names].to_numpy())) / 2.0)
    out_df['z'] /= section_distance

    for i in medians:
        out_df[str(i) + "med"] = (out_df[str(i)] + out_df[str(i + 90)]) / 2

    out_df = out_df[['z'] + angle_names + [str(x) + "med" for x in medians] + ['hull_volume', 'hull_area']]
    out_df.to_csv(out_dir + sep + file_name.split(sep)[-1], index=False)

    stats_df = out_df[[str(x) + "med" for x in medians]].values
    out_table.append(
        [only_file_name, np.mean(stats_df), np.std(stats_df), np.mean(this_tree_min_max), np.std(this_tree_min_max)])
    trees_means_global_array.append(np.mean(stats_df))
    all_stats_dict["min_max_sections__" + only_file_name] = this_tree_min_max
    all_stats_dict["min_max_sections__" + only_file_name] = this_tree_min_max

all_stats_dict["forest_mean"] = np.mean(trees_means_global_array)
all_stats_dict["forest_std"] = np.std(trees_means_global_array)
all_stats_dict["forest_min_max_mean"] = np.mean(trees_means_global_array)
all_stats_dict["forest_min_max_std"] = np.std(trees_means_global_array)

ndf = pd.DataFrame(out_table)
ndf.to_csv(out_dir + sep + "stats_table.txt", header=None)

with open(out_dir + sep + "stats.txt", "w") as f:
    for k, v in all_stats_dict.items():
        s = "** " + str(k) + "  =  " + str(v) + "\n"
        b = f.write(s)
