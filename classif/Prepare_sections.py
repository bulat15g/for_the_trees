import os
import warnings
from copy import copy
from glob import glob
from platform import system as getsys

import easygui
import pandas as pd

####################
end_dist = 0.5
cut_quantile = 0.005
res_name = "result.txt"
delta = 0.1
####################

warnings.filterwarnings('ignore')
sep = "\\"
if getsys() == "Linux":
    sep = "/"

dir_name = easygui.diropenbox("select tree to process")
out_dir = dir_name + sep + "processed"

if not os.path.exists(out_dir):
    os.makedirs(out_dir)
f = open(out_dir + sep + res_name, "w+")
f.close()

for file_name in glob(dir_name + sep + "*.txt"):
    print("going to file:" + file_name)

    df = pd.read_csv(file_name, delimiter=' ', header=None)
    df.columns = ['x', 'y', 'z', 'laser']
    df.drop('laser', 1, inplace=True)
    # select df
    df = df[(df['z'].quantile(cut_quantile) < df['z']) & (df['z'] < end_dist + df['z'].quantile(cut_quantile))]
    print("count of points", df.shape)
    # shift and copy
    df['z'] = df['z'].min()
    df1 = copy(df)
    df['z'] = df['z'].min() - delta
    df2 = copy(df)
    df['z'] = df['z'].min() - delta

    df.to_csv(out_dir + sep + res_name, header=False, sep=" ", index=False, mode="a")
    df1.to_csv(out_dir + sep + res_name, header=False, sep=" ", index=False, mode="a")
    df2.to_csv(out_dir + sep + res_name, header=False, sep=" ", index=False, mode="a")
