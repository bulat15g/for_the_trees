import glob
import os
import pandas as pd
import numpy as np
import time
import warnings

warnings.filterwarnings('ignore')

###
divs_count = 60
folder = os.getcwd() + "/res/"
fail_folder = os.getcwd() + "/results_fail/"
min_mean = 0.8
min_std = 0.1
mid_of_max = 7
side_of_square = 0.1
###
begin_time = time.time()
for i in [folder, fail_folder]:
    if not os.path.exists(i):
        os.makedirs(i)

for file_name in glob.glob("*.txt"):
    print("going to file {} ,time is {}".format(file_name, round(time.time() - begin_time, 2)))
    out_df = pd.DataFrame(columns=['rad', 'std', 'den_std'])
    # shift coords
    df = pd.read_csv(file_name, delimiter=' ', header=None)
    df.columns = ['x', 'y', 'z', 'laser']
    df.drop('laser', 1, inplace=True)
    df['x'] -= df['x'].mean()
    df['y'] -= df['y'].mean()
    df['z'] = (df['z'] - df['z'].min()) / (df['z'].max() - df['z'].min() + 0.001) * divs_count
    df['z'] = df['z'].round(0)
    # count some params
    for num in range(int(divs_count)):
        ndf = df[df['z'] == num]
        ndf['x_t'] = np.round((ndf['x'] - ndf['x'].min()) / side_of_square)
        ndf['y_t'] = np.round((ndf['y'] - ndf['y'].min()) / side_of_square)

        from collections import Counter

        c = Counter(list(zip(ndf['x_t'], ndf['y_t'])))
        b = list(c.values())
        if ndf['x_t'].max() == ndf['x_t'].max():
            for x in range(int(ndf['x_t'].max())):
                for y in range(int(ndf['y_t'].max())):
                    if (x, y) not in c:
                        b.append(0)
        else:
            b = [0]

        ndf['rad'] = np.sqrt(ndf['x'] ** 2 + ndf['y'] ** 2)
        a = ndf['rad'].tolist()
        a.sort()

        out_df = out_df.append(
            {"rad": np.median(a[-mid_of_max:]), 'std': np.std(np.array([ndf['x_t'].values, ndf['y_t'].values])),
             'den_std': np.std(b)},
            ignore_index=True)
    # out data
    out_df.fillna(method='ffill', inplace=True)
    out_fold = ''
    if out_df['rad'].mean() > min_mean and out_df['rad'].std() > min_std:
        out_fold = folder
    else:
        out_fold = fail_folder
    out_df.to_csv(out_fold + file_name, sep='\t',index=False)
