import os
import glob
# import mxnet

# print(mxnet.cpu())
import easygui


def rename(folder, addition):
    for i in glob.glob(folder + "/*.txt"):
        os.rename(i, i.replace('.', addition + '.'))


rename('Buffer', "list")

# import platform
# print(platform.system())
process_path = easygui.enterbox()
print(process_path)
