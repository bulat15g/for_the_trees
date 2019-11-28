import os
import warnings
from glob import glob
from platform import system as getsys

import easygui
import pandas as pd

warnings.filterwarnings('ignore')
sep = "\\"
if getsys() == "Linux":
    sep = "/"

dir_name = easygui.diropenbox("select tree to process")
out_dir = dir_name + sep + "processed"

######################################################################
enable_dx_dy_shift = False
begin_dist = 0.9
end_dist = 1.7
######################################################################


if not os.path.exists(out_dir):
    os.makedirs(out_dir)

for file_name in glob(dir_name + sep + "*.txt"):
    only_file_name = file_name.split(sep)[-1]
    df = pd.read_csv(file_name, delimiter=' ', header=None)
    df.columns = ['x', 'y', 'z', 'laser']
    df.drop('laser', 1, inplace=True)

    if enable_dx_dy_shift:
        df['x'] = df['x'] - df['x'].mean()
        df['y'] = df['y'] - df['y'].mean()
    df['z'] = (df['z'] - df['z'].quantile(0.015))
    df = df[(begin_dist < df['z']) & (df['z'] < end_dist)]

    df.to_csv(out_dir + sep + only_file_name, header=False, sep=" ", index=False)
