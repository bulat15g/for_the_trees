from os import mkdir, stat


class Point3d:
    x = float
    y = float
    z = float

    def __init__(self, x, y, z):
        self.x, self.y, self.z = x, y, z

    def get_dxdy(self, point2):
        return self.x - point2.x, self.y - point2.y, self.z - point2.z

    def get_norm(self, point2):
        import math
        return math.sqrt((self.x - point2.x) ** 2 + (self.y - point2.y) ** 2 + (self.z - point2.z) ** 2)

    def __str__(self):
        return str((self.x, self.y, self.z))


def read_text_file(f, set):
    """
    x,y
    x1,y1
    ...
    ..
    .
    """
    for line in f.readlines():
        local_read = line.replace("\n", "").split(" ")
        set.append(Point3d(float(local_read[0]), float(local_read[1]), float(local_read[2])))
    f.close()


def write_text_file(name, output_set):
    f = open(name.replace(".", "RESULT."), "w")
    for i in range(len(output_set)):
        f.write(str(i) + "\t val:\t" + str(output_set[i]) + "\n")
    f.close()


def get_files_list():
    import glob
    return glob.glob("*.txt")


def create_dir(directory):
    try:
        stat(directory)
    except:
        mkdir(directory)


def get_abs_val_point(points, mins, maxs, middles, absolute_values, scale_all):
    count = len(points)
    for i in points:
        if i.x < mins[0]: mins[0] = i.x
        if i.y < mins[1]: mins[1] = i.y
        if i.z < mins[2]: mins[2] = i.z

        if scale_all:
            if i.x > maxs[0]: maxs[0] = i.x
            if i.y > maxs[1]: maxs[1] = i.y
        if i.z > maxs[2]: maxs[2] = i.z

        middles[0] += i.x
        middles[1] += i.y

    middles[0] /= float(count)
    middles[1] /= float(count)
    for i in range(3):
        absolute_values[i] = maxs[i] - mins[i] + 0.01  # fixed error on scaling!!!!!!


def fill_nan_in_array(data):
    import numpy as np
    idx = np.where(np.isnan(data))
    for i in idx[0]: data[i] = data[i - 1]
    return data