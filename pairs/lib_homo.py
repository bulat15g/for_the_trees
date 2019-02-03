class Point2d:
    x = float
    y = float

    def __init__(self, x, y):
        self.x, self.y = x, y

    def get_dxdy(self, point2):
        return self.x - point2.x, self.y - point2.y

    def get_norm(self, point2):
        import math
        return math.sqrt((self.x - point2.x) ** 2 + (self.y - point2.y) ** 2)

    def __str__(self):
        return str((self.x, self.y))


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
        set.append(Point2d(float(local_read[0]), float(local_read[1])))
    f.close()


def print_dict(dictionary):
    print("(points in B(n-1))_(points in A(n-1))")
    for key in dictionary.keys():
        print("k:" + str(key) + "  v:" + str(dictionary[key]))
    print("\n\n")


def ordered_set(in_list):
    out_list = []
    added = set()
    for val in in_list:
        if not val in added:
            out_list.append(val)
            added.add(val)
    return out_list


def export_res_set_mode(name, set_list_not_num, B_set, A_set):
    import xlwt
    workbook = xlwt.Workbook()
    sheet = workbook.add_sheet(name)

    set_list_num = ordered_set(set_list_not_num)

    sheet.write(0, 0, "set")
    sheet.write(0, 1, "POINT IN B(N-1)")
    sheet.write(0, 2, "POINT IN A(N-1)")

    sheet.write(0, 5, "X IN B")
    sheet.write(0, 6, "Y IN B")

    sheet.write(0, 8, "X IN A")
    sheet.write(0, 9, "Y IN A")

    for i in range(len(set_list_num)):
        sheet.write(i + set_list_num[i][0] * 2 + 1, 0, str(set_list_num[i][0]))
        sheet.write(i + set_list_num[i][0] * 2 + 1, 1, str(set_list_num[i][1]))
        sheet.write(i + set_list_num[i][0] * 2 + 1, 2, str(set_list_num[i][2]))
        sheet.write(i + set_list_num[i][0] * 2 + 1, 5, str(B_set[set_list_num[i][1]].x))
        sheet.write(i + set_list_num[i][0] * 2 + 1, 6, str(B_set[set_list_num[i][1]].y))
        sheet.write(i + set_list_num[i][0] * 2 + 1, 8, str(A_set[set_list_num[i][2]].x))
        sheet.write(i + set_list_num[i][0] * 2 + 1, 9, str(A_set[set_list_num[i][2]].y))

    workbook.save(name + ".xls")


def export_res(name, dictionary, B_set, A_set):
    import xlwt
    workbook = xlwt.Workbook()
    sheet = workbook.add_sheet(name)

    sheet.write(0, 0, "POINT IN B(N-1)")
    sheet.write(0, 1, "POINT IN A(N-1)")

    sheet.write(0, 5, "X IN B")
    sheet.write(0, 6, "Y IN B")

    sheet.write(0, 8, "X IN A")
    sheet.write(0, 9, "Y IN A")

    sheet.write(0, 11, "DX")
    sheet.write(0, 12, "DY")

    counter = 1
    for key in dictionary:
        sheet.write(counter, 0, str(key))
        sheet.write(counter, 1, str(dictionary[key]))
        sheet.write(counter, 5, str(B_set[key].x))
        sheet.write(counter, 6, str(B_set[key].y))
        sheet.write(counter, 8, str(A_set[dictionary[key]].x))
        sheet.write(counter, 9, str(A_set[dictionary[key]].y))

        sheet.write(counter, 11, str(A_set[dictionary[key]].x - B_set[key].x))
        sheet.write(counter, 12, str(A_set[dictionary[key]].y - B_set[key].y))

        # print(counter,key," key ",[dictionary[key]]," val  ",B_set[key].x,A_set[dictionary[key]].x)
        counter += 1

    workbook.save(name + ".xls")
