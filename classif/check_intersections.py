import warnings
from glob import glob
from platform import system as getsys

import easygui
import pandas as pd

##############################
k_multiplier = 2
check_N_next = 6
distance_break = 100
##############################
pd.set_option('display.expand_frame_repr', False)
warnings.filterwarnings('ignore')
sep = "\\"
if getsys() == "Linux":
    sep = "/"

folder = easygui.diropenbox(msg=" Select folder to find intersections ") + sep
trees_means = []

for file_name in glob(folder + sep + "*.txt"):
    df = pd.read_csv(file_name, sep=' ', header=None, names=['x', 'y', 'z', 'laser'])
    df.drop(columns='laser', inplace=True)

    sample = df.mean().tolist()[:-1]
    sample.extend(df.std().tolist()[:-1])
    sample.append(file_name)
    trees_means.append(sample)

trees_means = pd.DataFrame(data=trees_means, columns=["x", "y", "stdX", "stdY", "name"])
trees_means = trees_means[["name", "x", "y", "stdX", "stdY"]]

print("All trees on folder are readed showing Head \n ")
print(trees_means.head())
print(" Look at", (trees_means.shape[0] + 1) * check_N_next, " combinations")

dfX = trees_means.loc[:, ["x", "stdX"]]
dfY = trees_means.loc[:, ["y", "stdY"]]

dfX.sort_values(by=['x'], inplace=True)
dfX['ind'] = dfX.index

dfY.sort_values(by=['y'], inplace=True)
dfY['ind'] = dfY.index

x_list = dfX.values.tolist()
y_list = dfY.values.tolist()

x_prepassed_index = []
y_prepassed_index = []

for i in range(len(x_list) - check_N_next):
    x_0 = x_list[i][0]
    x_1 = x_list[i][1]
    y_0 = y_list[i][0]
    y_1 = y_list[i][1]

    for n in range(1, check_N_next + 1):
        if x_list[i + n][0] - x_0 < (x_1 + x_list[i + n][1]) * k_multiplier:
            x_prepassed_index.append((x_list[i][2], x_list[i + n][2]))

        if y_list[i + n][0] - y_0 < (y_1 + y_list[i + n][1]) * k_multiplier:
            y_prepassed_index.append((y_list[i][2], y_list[i + n][2]))

        if (x_list[i + n][0] - x_0) ** 2 + (y_list[i + n][0] - y_0) ** 2 > distance_break:
            break

passed_indexes = set(x_prepassed_index).intersection(y_prepassed_index)

trees_list = []
for i in passed_indexes:
    trees_list.extend(i)
trees_list = list(set(trees_list))
names_only = trees_means.loc[trees_list, "name"].apply(lambda x: str.split(x, sep)[-1])
print("\n", names_only)
print("\n all find pairs is ", [(names_only[x[0]], names_only[x[1]]) for x in list(passed_indexes)])

passed_names_full = [(trees_means.loc[x[0], "name"], trees_means.loc[x[1], "name"]) for x in list(passed_indexes)]

for pair in passed_names_full:
    tree1 = pd.read_csv(pair[0], delimiter=' ', header=None, names=['x', 'y', 'z', 'laser'])
    tree2 = pd.read_csv(pair[1], delimiter=' ', header=None, names=['x', 'y', 'z', 'laser'])
    min_z = min(tree1['z'].min(), tree2['z'].min())
    for i in [tree1, tree2]:
        i.drop('laser', 1, inplace=True)
        i['z'] -= (min_z + 0.001)
