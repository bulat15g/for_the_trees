import warnings
from collections import Counter
from glob import glob
from os import path
from platform import system as getsys
from time import time

import easygui
import numpy as np
import pandas as pd

# System settings
warnings.filterwarnings('ignore')
sep = "\\"
if getsys() == "Linux": sep = "/"

# changeable params
divs_count = 40
out_fail_files = False
min_mean = 0.8
min_std = 0.09
mid_of_max = 7
side_of_square = 0.1
count_points_on_square = 5

# GUI queries
pre_fold = easygui.diropenbox(msg=" select folder FROM") + sep
to_fold = easygui.diropenbox(msg=" select folder TO") + sep
fail_fold = easygui.diropenbox(msg=" select folder FAIL") + sep
add_need, add = True, easygui.enterbox("type addition to files")
begin_time = time()


# Process folder
def parse_folder(folder):
    for file_name in glob(folder + sep + "*.txt"):
        print("going to file {} ,time is {}".format(file_name, round(time() - begin_time, 2)))

        out_df = pd.DataFrame(columns=['rad', 'std', 'den_std', 'points_dens'])
        df = pd.read_csv(file_name, delimiter=' ', header=None)
        df.columns = ['x', 'y', 'z', 'laser']

        # get tree absolute params before transform
        extra_params = [
            df["z"].max() - df["z"].min(),
            df['laser'].mean(),
            df['laser'].median()
        ]

        # drop trash column and shift other columns
        df.drop('laser', 1, inplace=True)
        df['x'] -= df['x'].mean()
        df['y'] -= df['y'].mean()
        df['z'] = (df['z'] - df['z'].min()) / (df['z'].max() - df['z'].min() + 0.001) * divs_count
        df['z'] = df['z'].round(0)

        # calculate sections params
        for num in range(int(divs_count)):
            ndf = df[df['z'] == num]
            ndf['x_t'] = np.round((ndf['x'] - ndf['x'].min()) / side_of_square)
            ndf['y_t'] = np.round((ndf['y'] - ndf['y'].min()) / side_of_square)

            # calculate density
            # append zeros if no points in rect
            c = Counter(list(zip(ndf['x_t'], ndf['y_t'])))
            b = list(c.values())
            if ndf['x_t'].max() == ndf['x_t'].max():
                for x in range(int(ndf['x_t'].max())):
                    for y in range(int(ndf['y_t'].max())):
                        if (x, y) not in c:
                            b.append(0)
            else:
                b = [0]

            # calculate rads
            ndf['rad'] = np.sqrt(ndf['x'] ** 2 + ndf['y'] ** 2)
            a = ndf['rad'].tolist()
            a.sort()

            out_df = out_df.append(
                {"rad": np.median(a[-mid_of_max:]),
                 'std': np.std(np.array([ndf['x_t'].values, ndf['y_t'].values])),
                 'den_std': np.std(b),
                 'points_dens': np.size(np.where(np.array(b) > count_points_on_square)) / float(len(b))},
                ignore_index=True)

        # fill NAN values
        out_df.fillna(method='ffill', inplace=True)

        # choose folder
        if out_df['rad'].mean() > min_mean and out_df['rad'].std() > min_std:
            out_fold = to_fold
        else:
            out_fold = fail_fold

        out_values = list(out_df.to_numpy().ravel())
        out_values.extend(extra_params)
        out_values.extend([out_df['rad'].mean(), out_df['rad'].std()])

        # write all to txt
        file_name = add_need * add + file_name.split(sep)[-1]
        with open(out_fold + file_name, "w") as f:
            for s in out_values:
                f.write(str(s) + ' ')


if path.exists(pre_fold) and not len(glob(pre_fold + sep + "*.txt")) < 1:
    parse_folder(pre_fold)
else:
    print("path not exists or small count of data")
