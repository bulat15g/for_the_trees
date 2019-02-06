import os
from sklearn import linear_model
from sklearn.metrics import mean_squared_error
import glob
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings

warnings.filterwarnings('ignore')

# begin
folder1 = os.getcwd() + '/list/res'
folder2 = os.getcwd() + '/hw/res'
count_of_divs = 60
# end
mat = np.ones((count_of_divs,)).T
y = np.array([])
# read data
for i in glob.glob(folder1 + '/*.txt'):
    tree = pd.read_csv(i, delimiter='\t')['rad']
    mat = np.vstack((mat, tree.as_matrix().T))
    y = np.append(y, [1.0])
for i in glob.glob(folder2 + '/*.txt'):
    tree = pd.read_csv(i, delimiter='\t')['rad']
    mat = np.vstack((mat, tree.as_matrix().T))
    y = np.append(y, [-1.0])

mat = mat[1:]

regr = linear_model.LinearRegression()
regr.fit(mat, y)

prediction = regr.predict(mat)

print('Coefficients: \n', np.round(regr.coef_, 1))
print(mean_squared_error(y, prediction))

print(len(y))
