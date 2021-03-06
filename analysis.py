import numpy as np
import pandas as pd
import random
import csv
from scipy import stats
import statsmodels.api as sm
from statsmodels.tools import eval_measures
from sklearn.model_selection import train_test_split

from sklearn.preprocessing import LabelEncoder

from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier

if __name__=='__main__':

    random.seed(1)

    def load_file(file_path):
        df = pd.read_csv(file_path, delimiter=',')
        df = df.dropna()
        X = df[['donationamount', 'candidatewonlost']]
        y = df['percentchangeinstockprice']
        return X, y

    def classify(classifier):
       classifier.fit(X_train, y_train)
       return classifier.score(X_test, y_test)

    X, y = load_file("data/consolidated-donation-data.csv")

    # label_encoder = LabelEncoder()
    # y_label = label_encoder.fit_transform(y)

    X_train, X_test, y_train, y_test = train_test_split(
		X,
		y,
		test_size=0.2,
		random_state=0
	)

    X_train = sm.add_constant(X_train)
    X_test = sm.add_constant(X_test)

    model = sm.OLS(y_train, X_train)
    results = model.fit()

	# # Prints out the Report
    # print(results.summary())
    # print('R-squared: ', results.rsquared)
    # print("training MSE is " + str(eval_measures.mse(y_train, results.predict(X_train))))
    # print("testing MSE is " + str(eval_measures.mse(y_test, results.predict(X_test))))
    #
    # knn = KNeighborsClassifier(n_neighbors=3)
    # knn_score = classify(knn)
    # print("knn score: " + str(knn_score))
    #
    # decision_tree = DecisionTreeClassifier(random_state=0)
    # decision_tree_score = classify(decision_tree)
    # print("decision tree score: " + str(decision_tree_score))
    #
    # svm = SVC(random_state=0)
    # svm_score = classify(svm)
    # print("svm score: " + str(svm_score))
    #
    # mlp = MLPClassifier(random_state=0)
    # mlp_score = classify(mlp)
    # print("mlp score: " + str(mlp_score))
