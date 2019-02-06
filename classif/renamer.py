import os
import glob


def rename(folder, addition):
    for i in glob.glob(folder + "/*.txt"):
        os.rename(i, i.replace('.', addition + '.'))
