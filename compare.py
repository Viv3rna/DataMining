# Utilities
import pandas as pd
import numpy as np
import tkinter as tk
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score, accuracy_score, confusion_matrix, recall_score

# Models
from sklearn.linear_model import Perceptron, LogisticRegression
from sklearn.naive_bayes import GaussianNB, MultinomialNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.svm import SVC
from xgboost import XGBClassifier

CLASIFFIER_LIST = [
    Perceptron,
    GaussianNB,
    MultinomialNB,
    DecisionTreeClassifier,
    RandomForestClassifier,
    KNeighborsClassifier,
    MLPClassifier,
    SVC,
    XGBClassifier,
]


def build_models(
    data: pd.DataFrame,
    target,
    classifier_list: list,
    random_state: int,
    param_grid=None,
) -> dict:

    results_dictionary = {}

    if param_grid == None:
        default = True

    x_train, x_test, y_train, y_test = train_test_split(
        data, target, test_size=0.3, random_state=random_state
    )

    for model in classifier_list:
        if default == True:
            if model in [KNeighborsClassifier, MultinomialNB, GaussianNB]:
                clf = model()
            elif model == XGBClassifier:
                clf = model(use_label_encoder=False, eval_metric="logloss")
            else:
                clf = model(random_state=random_state)
            clf.fit(x_train, y_train)
            predicted = clf.predict(x_test)
            ax = sns.heatmap(confusion_matrix(y_test, predicted), annot=True, fmt="g")
            fig = ax.get_figure()
            print(model.__name__)
            fig.savefig(f"matrices\\{model.__name__}.jpg", dpi=300)
            plt.close()
            results_dictionary[model.__name__] = {
                "f1_score": round(
                    f1_score(
                        y_test,
                        predicted,
                    ),
                    2,
                ),
                "accuracy": round(accuracy_score(y_test, predicted), 2),
                "recall": round(recall_score(y_test, predicted), 2),
                "confusion_matrix_path": f"matrices\\{model.__name__}.jpg",
            }

    return results_dictionary