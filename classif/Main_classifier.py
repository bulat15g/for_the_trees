import warnings
from glob import glob
from platform import system as getsys

import easygui
import numpy as np
import pandas as pd
import xgboost
from sklearn import linear_model
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import mean_squared_error as mse, accuracy_score as accuracy
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC

warnings.filterwarnings('ignore')
np.set_printoptions(linewidth=80)
process_path = easygui.diropenbox(msg=" select folder to process")
sep = "\\"
if getsys() == "Linux": sep = "/"

# ----------- begin change params-----------
use_density, use_std, point_dens = True, True, True
count_of_divs = 40
out_file_name = process_path + sep + "out.csv"
pred_file_name = process_path + sep + "prediction.txt"

# reg = KNeighborsClassifier(15)
reg = RandomForestClassifier(n_estimators=1000)
# reg = linear_model.LogisticRegression(class_weight='balanced')
# reg = SVC()
# reg = xgboost.XGBClassifier(n_estimators=100)
# ----------- end change params -----------


# some settings
use_snag_flag = False
use_pred_flag = False
# key_words = ['hw', 'list']
key_words = ['dead', 'alive']
folder1 = process_path + sep + key_words[0]
folder2 = process_path + sep + key_words[1]
pred_folder = process_path + sep + "sample"
snag_folder = process_path + sep + "snag"


def read_data(folder_name, sign=-1, scan_name=False):
    X = list()
    names = list()
    y = list()
    for i in glob(folder_name + sep + '*.txt'):
        with open(i, 'r') as f:
            values = [line.split(" ") for line in f][0]
            float_vals = [float(x) for x in values if x != ""]
            X.append(float_vals)
        names.append(i.split(sep)[-1])
        y.append(sign)

    print("already read ", folder_name, np.asarray(X).shape, np.asarray(y).shape, np.asarray(names).shape)
    if scan_name:
        y = [int(key_words[1] in x) for x in names]
    return np.asarray(X), np.asarray(y), np.asarray(names)


X_1, y_1, names1 = read_data(folder1, 0)
X_2, y_2, names2 = read_data(folder2, 1)

X_pred, y_true, names_pred = read_data(pred_folder, scan_name=True)
X_snag, y_snag, names_snag = read_data(snag_folder, scan_name=True)

if not isinstance(X_snag, int): use_snag_flag = True
if not isinstance(X_pred, int): use_pred_flag = True

X_train = np.vstack((X_1, X_2))
y_train = np.append(y_1, y_2)
names_train = np.append(names1, names2)
del X_1, y_1, names1, X_2, y_2, names2

reg.fit(X_train, y_train)

pred, pred_snag = 0, 0
if use_pred_flag: pred = reg.predict(X_pred)
if use_snag_flag: pred_snag = reg.predict(X_snag)
pred_self = reg.predict(X_train)

with open(pred_file_name, "w") as f:
    f.write("Mse on train is " + str(mse(pred_self, y_train)) + "\n")
    f.write("Accuracy on train is " + str(accuracy(pred_self, y_train)) + "\n")

    if use_pred_flag:
        f.write("Mse on predict is " + str(mse(pred, y_true)) + "\n")
        f.write("Accuracy on predict is " + str(accuracy(pred, y_true)) + "\n")

if not isinstance(pred, int):
    df = pd.DataFrame({"name": list(names_train) + list(names_pred) * use_pred_flag + list(names_snag) * use_snag_flag,
                       "true": list(y_train) + list(y_true) * use_pred_flag + list(y_snag) * use_snag_flag,
                       "pred": list(pred_self) + list(pred) * use_pred_flag + list(pred_snag) * use_snag_flag,
                       "type": ["train"] * X_train.shape[0] + ["test"] * X_pred.shape[0] * use_pred_flag + ["snag"] *
                               X_snag.shape[0] * use_snag_flag
                       })
    df.to_csv(out_file_name, index=False)


msg = "Необходимо протестироват сразу несколько моделей?"
choices = ("[<F1>]Да", "[<F2>]Нет")

if easygui.ynbox(msg, "hey", choices, image=None, default_choice="[<F1>]Да", cancel_choice="[<F2>]Нет"):
    models = [KNeighborsClassifier(15),
              RandomForestClassifier(n_estimators=1000),
              linear_model.LogisticRegression(class_weight='balanced'),
              SVC(class_weight="balanced"),
              xgboost.XGBClassifier(n_estimators=100)]
    for i in models:
        cv = StratifiedKFold(n_splits=6, shuffle=True)
        scores = cross_val_score(i, X_train, y_train, scoring="accuracy", cv=cv)
        print(str((type(i), "\t", np.mean(scores), scores)) + "\n")
