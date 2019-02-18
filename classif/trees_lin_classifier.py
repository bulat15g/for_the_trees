import os
from sklearn import linear_model
from sklearn import ensemble
from sklearn.metrics import mean_squared_error, accuracy_score
import glob
import pandas as pd
import numpy as np
import warnings

warnings.filterwarnings('ignore')
np.set_printoptions(linewidth=80)

# begin change params
key_words = ['hw', 'list']
use_density, use_std = True, True
folder1 = os.getcwd() + '/' + key_words[0]
folder2 = os.getcwd() + '/' + key_words[1]
count_of_divs = 40
out_file_name = "Linear_reg_self_res.txt"
pred_file_name = "Linear_reg_prediction_res.txt"
predict_folder = os.getcwd() + "/to_pred"
# end change params

names = np.array([])
mat = np.ones((count_of_divs * (1 + use_density + use_std),)).T
mat_to_predict = np.ones((count_of_divs * (1 + use_density + use_std),)).T
y = np.array([])
if not os.path.exists(predict_folder):
    os.makedirs(predict_folder)

# Learn preparing
names = np.append(names, glob.glob(folder1 + '/*.txt'))
names = np.append(names, glob.glob(folder2 + '/*.txt'))
for i in glob.glob(folder1 + '/*.txt'):
    tree = pd.read_csv(i, delimiter='\t')
    mat = np.vstack((mat, tree.as_matrix(['rad', 'std' * use_std, 'den_std' * use_density]).ravel().T))
    y = np.append(y, [0])
for i in glob.glob(folder2 + '/*.txt'):
    tree = pd.read_csv(i, delimiter='\t')
    mat = np.vstack((mat, tree.as_matrix(['rad', 'std' * use_std, 'den_std' * use_density]).ravel().T))
    y = np.append(y, [1])
mat = mat[1:]

# prediction preparing
names_pred = [x.split("/")[-1] for x in glob.glob(predict_folder + '/*.txt')]
y_test_true = np.array([int(key_words[1] in x) for x in names_pred])
for i in glob.glob(predict_folder + '/*.txt'):
    tree = pd.read_csv(i, delimiter='\t')
    mat_to_predict = np.vstack(
        (mat_to_predict, tree.as_matrix(['rad', 'std' * use_std, 'den_std' * use_density]).ravel().T))
mat_to_predict = mat_to_predict[1:]

# learn process
regressor = linear_model.LogisticRegression(class_weight='balanced')

if len(list(mat.shape)) < 2:
    print("train samples not found")
    exit(0)
regressor.fit(mat, y)

# out self results
prediction = regressor.predict(mat)
with open(out_file_name, 'w') as f:
    out = [
        ('coefs', regressor.coef_), ('mse:  ', mean_squared_error(y, prediction)),
        ('true / all = ', accuracy_score(y, np.sign(prediction))), ('ans :  ', y),
        ('predict: ', np.sign(prediction)), ('FALSE FILES IS: \n \n',
                                             np.hstack((names[np.argwhere(y != np.sign(prediction))],
                                                        prediction[np.argwhere(y != np.sign(prediction))]))),
        ('end ', '')]
    for i in out:
        line = '\n\n\t'
        for j in i:
            line += str(j).replace("\n", "\n")
        f.write(line)

# out pred results
with open(pred_file_name, 'w') as f:
    if len(list(mat_to_predict.shape)) < 2: print("prediction samples not found")
    # print(mat_to_predict.shape)
    # print(mat_to_predict)
    prediction = regressor.predict(mat_to_predict)
    out = [(
        'file - class (' + key_words[0] + ' = 0; ' + key_words[1] + '= 1): \n \n',
        ('mse:  ', mean_squared_error(y_test_true, prediction)),
        " accuracy: " + str(accuracy_score(y_test_true, np.sign(prediction))),
        "\nfile by file result is -",
        list(zip(names_pred, np.round(regressor.predict_proba(mat_to_predict)[:, 1], 2),
                 np.sign(prediction), np.sign(prediction) == y_test_true)))]
    for i in out:
        line = '\n\n\t'
        for j in i:
            line += "\n"+str(j).replace('), (', "\n")
        f.write(line)
