import time
from math import sqrt

import numpy as np

from classif.trees_lib import *

# script will parse all txt files in this directory

divs_count = 60.0
scale_all = False
res_folder_name = "res"
min_middle_of_section = 1.5
min_sigma_of_sections = 1
middle_of_max = 7

###### exit change
time_start = time.time()


def parse_file(name, dir_name):
    file_name = name
    f = open(file_name, "r")
    points = list()
    read_text_file(f, points)

    # find params
    mins = [9999999.0, 9999999.0, 9999999.0]
    maxs = [-9999999.0, -9999999.0, -9999999.0]
    middles = [0.0, 0.0, 0.0]
    absolute_values = [0.0, 0.0, 0.0]
    get_abs_val_point(points, mins, maxs, middles, absolute_values, scale_all)

    # do shift and find rads
    sec_val = []
    pre_final_sec_val = [0.0] * int(divs_count)
    for i in range(int(divs_count)):
        sec_val.append([])

    for i in points:
        if scale_all:
            i.x = (i.x - middles[0]) / absolute_values[0]
            i.y = (i.y - middles[1]) / absolute_values[1]
        else:
            i.x -= middles[0]
            i.y -= middles[1]
        i.z = (i.z - mins[2]) / absolute_values[2]
        rad = sqrt(i.x ** 2 + i.y ** 2)
        section_num = int(i.z * divs_count)
        sec_val[section_num].append(rad)

    # parse to final results

    for i in range(int(divs_count)):
        sec_val[i].sort()
        loc = sec_val[i][-middle_of_max:]
        loc = np.array(loc)
        pre_final_sec_val[i] = float(np.median(loc))

    fin_sec_val_numpy = fill_nan_in_array(np.array(pre_final_sec_val))

    if float(fin_sec_val_numpy.std()) < min_sigma_of_sections or float(
            fin_sec_val_numpy.mean()) < min_middle_of_section:
        print(name, "  Is wery small :mean  ", fin_sec_val_numpy.mean(), "   std ", fin_sec_val_numpy.std())
        create_dir(dir_name + "_fail")
        write_text_file(dir_name + "_fail" + "/" + file_name, pre_final_sec_val)

    # out results
    else:
        create_dir(dir_name)
        write_text_file(dir_name + "/" + file_name, pre_final_sec_val)


files_list = get_files_list()

for i in files_list:
    parse_file(i, res_folder_name)

print("\n\t", time.time() - time_start, "   seconds was worked")
