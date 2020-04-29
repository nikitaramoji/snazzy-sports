import numpy as np
import pandas as pd
import random
import csv
from scipy import stats
import statsmodels.api as sm
from statsmodels.tools import eval_measures
from sklearn.model_selection import train_test_split

from sklearn.preprocessing import LabelEncoder
from matplotlib import pyplot as plt

from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier

if __name__=='__main__':

    random.seed(1)


    # need to make new columns/values for columns
    # party - will be 0 for republican, 1 for democrat
    # chamber - 3 columns - is_pres, is_senate, is_congressional

    def load_file(file_path):
        #candidate,donation_amount,candidate_won_lost,stock_ticker,
        #stock_price_change,year,opening_price,closing_price,party,chamber
        df = pd.read_csv(file_path, delimiter=',')
        df = df.dropna()
        X = df[['donation_amount', 'candidate_won_lost', 'is_democrat', 'is_senate']]
        y = df['stock_price_change']
        return X, y

    def classify(classifier):
       classifier.fit(X_train, y_train)
       return classifier.score(X_test, y_test)



    X, y = load_file("multivar_2012.csv")

    #label_encoder = LabelEncoder()
    #y = label_encoder.fit_transform(y)

    X_train, X_test, y_train, y_test = train_test_split(
		X,
		y,
		test_size=0.01,
		random_state=0
	)



    X_train = sm.add_constant(X_train)
    X_test = sm.add_constant(X_test)

    model = sm.OLS(y_train,X_train.astype(float))
    results = model.fit()

	# Prints out the Report
    print(results.summary())
