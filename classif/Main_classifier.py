from os import path, makedirs
from sklearn import linear_model
from sklearn.metrics import mean_squared_error as mse, accuracy_score as accuracy
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from glob import glob
import xgboost
import pandas as pd
import numpy as np
import warnings
import easygui
from platform import system as getsys

warnings.filterwarnings('ignore')
np.set_printoptions(linewidth=80)
process_path = easygui.diropenbox(msg=" select folder to process")
sep = "\\"
if getsys() == "Linux": sep = "/"

# ----------- begin change params-----------
use_density, use_std, point_dens = True, True, True
count_of_divs = 40
out_file_name = process_path + sep + "reg_self.txt"
pred_file_name = process_path + sep + "reg_prediction.txt"

# reg = KNeighborsClassifier(15)
reg = RandomForestClassifier(n_estimators=1000)
# reg = linear_model.LogisticRegression(class_weight='balanced')
# reg = SVC()
# reg = xgboost.XGBClassifier(n_estimators=100)
# ----------- end change params -----------


# some settings
key_words = ['hw', 'list']
folder1 = process_path + sep + key_words[0]
folder2 = process_path + sep + key_words[1]
pred_folder = process_path + sep + "to_pred"
names = np.array([])
X = np.ones((count_of_divs * (1 + use_density + use_std + point_dens),)).T
X_pr = np.ones((count_of_divs * (1 + use_density + use_std + point_dens),)).T
y = np.array([])
if not path.exists(pred_folder):
    makedirs(pred_folder)

# Learn preparing
names = np.append(names, glob(folder1 + sep + '*.txt'))
names = np.append(names, glob(folder2 + sep + '*.txt'))

for i in glob(folder1 + sep + '*.txt'):
    tree = pd.read_csv(i, delimiter='\t')
    X = np.vstack(
        (X, tree.as_matrix(['rad', 'std' * use_std, 'den_std' * use_density, 'points_dens' * point_dens]).ravel().T))
    y = np.append(y, [0])
for i in glob(folder2 + sep + '*.txt'):
    tree = pd.read_csv(i, delimiter='\t')
    X = np.vstack(
        (X, tree.as_matrix(['rad', 'std' * use_std, 'den_std' * use_density, 'points_dens' * point_dens]).ravel().T))
    y = np.append(y, [1])
X = X[1:]

# y_pred preparing
pr_names = [x.split("/")[-1] for x in glob(pred_folder + sep + '*.txt')]
y_test = np.array([int(key_words[1] in x) for x in pr_names])
for i in glob(pred_folder + '/*.txt'):
    tree = pd.read_csv(i, delimiter='\t')
    X_pr = np.vstack(
        (X_pr,
         tree.as_matrix(['rad', 'std' * use_std, 'den_std' * use_density, 'points_dens' * point_dens]).ravel().T))
X_pr = X_pr[1:]

# train regressor
if X.shape[0] < 20:
    print("train samples not found")
    exit(0)
reg.fit(X, y)

# out self results
y_pred = reg.predict(X)
with open(out_file_name, 'w') as f:
    out = [
        ('mse:  ', mse(y, y_pred)),
        ('true / all = ',
         accuracy(y, np.sign(y_pred))),
        ('ans :  ', y),
        ('y_pred: ', np.sign(y_pred)),
        ('FALSE FILES IS: \n \n',
         np.hstack((names[np.argwhere(y != np.sign(y_pred))],
                    y_pred[np.argwhere(y != np.sign(y_pred))])))
    ]
    for i in out:
        line = '\n\n\t'
        for j in i:
            line += str(j).replace("\n", "\n")
        f.write(line)

# out pred results
with open(pred_file_name, 'w') as f:
    if len(list(X_pr.shape)) < 2: print("y_pred samples not found")
    y_pred = reg.predict(X_pr)
    out = [(
        'file - class (' + key_words[0] + ' = 0; ' + key_words[1] + '= 1): \n \n',
        ('mse:  ', mse(y_test, y_pred)),
        " accuracy: " + str(accuracy(y_test, np.sign(y_pred))),
        "\nfile by file result is -",
        list(zip(pr_names, y_pred,
                 np.sign(y_pred), np.sign(y_pred) == y_test)))]
    for i in out:
        line = '\n\n\t'
        for j in i:
            line += "\n" + str(j).replace('), (', "\n")
        f.write(line)
