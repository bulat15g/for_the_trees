import glob
import os
import pandas as pd
import numpy as np

######
divs_count = 60
folder = os.getcwd() + "/res/"
fail_folder = os.getcwd() + "/fail/"
min_mean = 0.6
min_std = 0.1
mid_of_max = 7
side_of_square=0.1
###
for i in [folder,fail_folder]:
    if not os.path.exists(i):
        os.makedirs(i)

for file_name in glob.glob("*.txt"):
    out_df = pd.DataFrame(columns=['rad', 'den_std'])

    df = pd.read_csv(file_name, delimiter=' ', header=None)
    df.columns = ['x', 'y', 'z', 'laser']
    df.drop('laser', 1, inplace=True)
    df['x'] -= df['x'].mean()
    df['y'] -= df['y'].mean()
    df['z'] = (df['z'] - df['z'].min()) / (df['z'].max() - df['z'].min() + 0.01) * divs_count
    df['z'] = df['z'].round(0)

    for num in range(int(divs_count)):
        ndf = df[df['z'] == num]
        ndf['x_t'] = np.round((ndf['x'] - ndf['x'].min()) / side_of_square)
        ndf['y_t'] = np.round((ndf['y'] - ndf['y'].min()) / side_of_square)

        ndf['rad'] = np.sqrt(ndf['x'] ** 2 + ndf['y'] ** 2)
        a = ndf['rad'].tolist()
        a.sort()

        out_df = out_df.append({"rad": np.median(a[-mid_of_max:]),'den_std':np.std(np.array([ndf['x_t'].values, ndf['y_t'].values]))}, ignore_index=True)

    out_df.fillna(method='ffill', inplace=True)

    out_fold = ''
    if out_df['rad'].mean() > min_mean and out_df['rad'].std() > min_std:
        out_fold = folder
    else:
        out_fold = fail_folder
    out_df.to_csv(out_fold + file_name,sep='\t')
