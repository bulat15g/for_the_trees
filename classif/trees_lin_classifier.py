import os
from sklearn import linear_model
from sklearn.metrics import mean_squared_error
import glob
import pandas as pd
import numpy as np
import warnings

warnings.filterwarnings('ignore')
np.set_printoptions(linewidth=80)

# begin change params
folder1 = os.getcwd() + '/list'
folder2 = os.getcwd() + '/hw'
count_of_divs = 60
out_file_name = "Linear_reg_self_res.txt"
pred_file_name = "Linear_reg_prediction_res.txt"
predict_folder = os.getcwd() + "/to_pred"
# end change params

names = np.array([])
mat = np.ones((count_of_divs,)).T
y = np.array([])
if not os.path.exists(predict_folder):
    os.makedirs(predict_folder)

# Learn preparing
names = np.append(names, glob.glob(folder1 + '/*.txt'))
names = np.append(names, glob.glob(folder2 + '/*.txt'))
for i in glob.glob(folder1 + '/*.txt'):
    tree = pd.read_csv(i, delimiter='\t')['rad']
    mat = np.vstack((mat, tree.as_matrix().T))
    y = np.append(y, [1.0])
for i in glob.glob(folder2 + '/*.txt'):
    tree = pd.read_csv(i, delimiter='\t')['rad']
    mat = np.vstack((mat, tree.as_matrix().T))
    y = np.append(y, [-1.0])
mat = mat[1:]

# prediction preparing
names_pred = np.append(predict_folder, glob.glob(predict_folder + '/*.txt'))
mat_to_predict = np.ones((count_of_divs,)).T
for i in glob.glob(predict_folder + '/*.txt'):
    tree = pd.read_csv(i, delimiter='\t')['rad']
    mat_to_predict = np.vstack((mat_to_predict, tree.as_matrix().T))
mat_to_predict = mat_to_predict[1:]
# learn process
regr = linear_model.LinearRegression()
regr.fit(mat, y)

# out self results
prediction = regr.predict(mat)
with open(out_file_name, 'w') as f:
    out = [('Coefficients: \n', np.round(regr.coef_, 1)),
           ('mse:  ', mean_squared_error(y, prediction) / 4),
           ('true / all = ', len(np.argwhere(y == np.sign(prediction))) / float(len(y))), ('ans :  ', y),
           ('predict: ', np.sign(prediction)),
           ('FALSE FILES IS: \n \n', np.hstack(
               (names[np.argwhere(y != np.sign(prediction))], prediction[np.argwhere(y != np.sign(prediction))]))),
           ('end ', '')
           ]
    for i in out:
        line = '\n\n\t'
        for j in i:
            line += str(j).replace("\n", "\n")
        f.write(line)
# out pred results
with open(pred_file_name, 'w') as f:
    prediction = regr.predict(mat_to_predict)
    out = [('file - class (hw = -1; list= 1): \n \n', list(zip(names_pred, prediction,np.sign(prediction))))]
    for i in out:
        line = '\n\n\t'
        for j in i:
            line += str(j).replace('), (',"\n")
        f.write(line)
