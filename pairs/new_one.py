import time

import xlrd

from pairs.lib_homo import print_dict, Point2d, read_text_file, export_res_set_mode, export_res

#### CHANGE PARAMS HERE

eps = 0.5
eps_dist = 4
dist_between_trees = 30

count_of_trees_B = 800
first_tree_in_B = 0
count_of_trees_A = 800
first_tree_in_A = 0

debug_status = False
show_percent_of_arc_fill = True
show_points_in_fill_arcs = False
print_all_arcs_in_console = False

output_set_mode = True
accelerate_by_sorted_points = True
use_test_samples = False  # IF EXCEL -True

excel_A_file = "FMRanspurk.xlsx"
excel_B_file = "TLSRanspurk.xlsx"
x_col_number_A, y_col_number_A = 0, 1
x_col_number_B, y_col_number_B = 0, 1

#### end CHANGE PARAMS


f = open("A.txt", "r")
f1 = open("B.txt", "r")
A_set = list()
B_set = list()
homomorph = {}
time_start = time.time()


# read file and find all arcs

def open_excel(name, set, x_col_number, y_col_number, replace_comma=False):
    """
    for FGEO_FM_trees.xlsx
    'x_coord' (0, 3) 'y_coord' (0, 4)

    for FGEO_Drone_trees.xlsx
    'x position coordinate' (0, 1)
    'y position coordinate' (0, 2)

    """
    workbook = xlrd.open_workbook(name)
    worksheet = workbook.sheet_by_index(0)
    if replace_comma:
        for row in range(1, worksheet.nrows):
            set.append(Point2d(
                float(worksheet.cell_value(row, x_col_number).replace(",", ".")),
                float(worksheet.cell_value(row, y_col_number).replace(",", "."))))
    else:
        for row in range(1, worksheet.nrows):
            set.append(Point2d(
                float(worksheet.cell_value(row, x_col_number)),
                float(worksheet.cell_value(row, y_col_number))))


if use_test_samples:
    read_text_file(f, A_set)
    read_text_file(f1, B_set)

    count_of_trees_B = len(B_set)
    count_of_trees_A = len(A_set)
else:
    # todo mistake here
    # if count_of_trees_B > len(B_set): count_of_trees_B = len(B_set)
    # if count_of_trees_A > len(A_set): count_of_trees_A = len(A_set)
    if excel_A_file == "FGEO_Drone_trees.xlsx":
        open_excel(excel_B_file, B_set, x_col_number_B, y_col_number_B, True)
    else:
        open_excel(excel_B_file, B_set, x_col_number_B, y_col_number_B)
    open_excel(excel_A_file, A_set, x_col_number_A, y_col_number_A)
print("\n Files opnened, begin fill arcs \n")

# fill arcs

if accelerate_by_sorted_points:
    for i in range(first_tree_in_B, count_of_trees_B):
        if show_percent_of_arc_fill: print("success percent=", i / float(count_of_trees_B), "%")

        for j in range(i + 1, count_of_trees_B):
            dx2, dy2 = B_set[i].get_dxdy(B_set[j])
            if dx2 ** 2 + dy2 ** 2 > dist_between_trees ** 2 or i == j:
                break

            for k in range(first_tree_in_A, count_of_trees_A):

                for m in range(k, first_tree_in_A, -1):  ############################## THIS IS BIG DILEMMA
                    dx1, dy1 = A_set[k].get_dxdy(A_set[m])

                    if not k == m and dx1 ** 2 + dy1 ** 2 < dist_between_trees ** 2:
                        if (dx1 - dx2) ** 2 < eps and (dy1 - dy2) ** 2 < eps \
                                and A_set[k].get_norm(B_set[i]) < eps_dist:
                            if (i, j) in homomorph:
                                homomorph[(i, j)].append((k, m))
                            else:
                                homomorph[(i, j)] = [(k, m)]

                            if show_points_in_fill_arcs:
                                print((str(A_set[k]), str(A_set[m])))
                                print((str(B_set[i]), str(B_set[j])))
                                print("_________________")
                    else:
                        break

                for m in range(k + 1, count_of_trees_A):  ############################## THIS IS BIG DILEMMA
                    dx1, dy1 = A_set[k].get_dxdy(A_set[m])

                    if not k == m and dx1 ** 2 + dy1 ** 2 < dist_between_trees ** 2:

                        if (dx1 - dx2) ** 2 < eps and (dy1 - dy2) ** 2 < eps \
                                and A_set[k].get_norm(B_set[i]) < eps_dist:
                            if (i, j) in homomorph:
                                homomorph[(i, j)].append((k, m))
                            else:
                                homomorph[(i, j)] = [(k, m)]

                            if show_points_in_fill_arcs:
                                print((str(A_set[k]), str(A_set[m])))
                                print((str(B_set[i]), str(B_set[j])))
                                print("_________________")
                    else:
                        break

# if not accelerate
else:
    for i in range(first_tree_in_B, count_of_trees_B):
        if show_percent_of_arc_fill: print("success percent=", i / float(count_of_trees_B), "%")

        for j in range(i + 1, count_of_trees_B):
            dx2, dy2 = B_set[i].get_dxdy(B_set[j])
            if dx2 ** 2 + dy2 ** 2 > dist_between_trees ** 2 or i == j:
                continue

            for k in range(first_tree_in_A, count_of_trees_A):
                for m in range(first_tree_in_A, count_of_trees_A):  ############################## THIS IS BIG DILEMMA
                    dx1, dy1 = A_set[k].get_dxdy(A_set[m])
                    if not k == m and dx1 ** 2 + dy1 ** 2 < dist_between_trees ** 2:

                        if (dx1 - dx2) ** 2 < eps and (dy1 - dy2) ** 2 < eps \
                                and A_set[k].get_norm(B_set[i]) < eps_dist:

                            if (i, j) in homomorph:
                                homomorph[(i, j)].append((k, m))
                            else:
                                homomorph[(i, j)] = [(k, m)]

                            if show_points_in_fill_arcs:
                                print((str(A_set[k]), str(A_set[m])))
                                print((str(B_set[i]), str(B_set[j])))
                                print("_________________")

if print_all_arcs_in_console: print_dict(homomorph)

# find max sub_graph

local_sub = {}
local_used_A = []
local_used_B = []
main_homo = {}
main_homo_set_mode = []
counter_set_mode = 0


def iteration(iter_counter, key, values_index, debug=False):
    """

    :param iter_counter:
    :param key: tuple to dict
    :param values_index: value[i]
    :param debug:
    :return:
    """
    if iter_counter > 15:
        return

    value = homomorph[key].pop(values_index)
    # add block
    for i in range(2):
        local_used_B.append(key[i])
        local_used_A.append(value[i])
        main_homo[key[i]] = value[i]
        if output_set_mode: main_homo_set_mode.append((counter_set_mode, key[i], value[i]))
        if debug: print("debug:  ", iter_counter, "it  ", key[i], "-B  ", value[i], "-A")

    # check next block
    for next_key in homomorph.keys():
        shift_R = 0
        if next_key[0] == key[1] and (not (next_key[1] in local_used_B)):
            for next_val_index in range(len(homomorph[next_key])):

                next_val = homomorph[next_key][next_val_index - shift_R]
                if next_val[0] == value[1] and not next_val[1] in local_used_A:
                    iteration(iter_counter + 1, next_key, next_val_index - shift_R, debug)
                    shift_R += 1


for key in homomorph.keys():
    for i in range(len(homomorph[key])):
        iter_counter = 0
        local_sub.clear()
        local_used_A.clear()
        local_used_B.clear()

        if not (key[0] in main_homo.keys() or key[1] in main_homo.keys()):
            iteration(iter_counter, key, i, debug_status)
            counter_set_mode += 1

# print results


if print_all_arcs_in_console: print_dict(main_homo)

if output_set_mode:
    export_res_set_mode("result", main_homo_set_mode, B_set, A_set)
else:
    export_res("result", main_homo, B_set, A_set)

print("\n", time.time() - time_start, " seconds was worked")
