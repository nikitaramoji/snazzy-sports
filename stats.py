import numpy as np
import pandas as pd
import random
import csv
from scipy import stats
import statsmodels.api as sm
from statsmodels.tools import eval_measures

def split_data(data, prob):
    train = []
    test = []
    for pair in data:
        if random.random() >= prob:
        	train.append(pair)
        else:
        	test.append(pair)
    return train, test

def train_test_split(x, y, test_pct):
    data = zip(x.values,y.values)
    train, test = split_data(data, test_pct)
    X_train, y_train = zip(*train)
    X_train = list(X_train)
    X_test, y_test = zip(*test)
    X_test = list(X_test)
    return X_train, X_test, y_train, y_test


if __name__=='__main__':

	# DO not change this seed. It guarantees that all students perform the same train and test split
    random.seed(1)
	# Setting p to 0.2 allows for a 80% training and 20% test split
    p = 0.2

    def load_file(file_path):
        df = pd.read_csv(file_path, delimiter=',')
        df = df.dropna()
        X = df[['donationamount', 'candidatewonlost']]
        y = df['percentchangeinstockprice']
        return X, y

    X, y = load_file("data/consolidated-donation-data.csv")


	##################################################################################
	# TODO: use train test split to split data into x_train, x_test, y_train, y_test #
	#################################################################################
    X_train, X_test, y_train, y_test = train_test_split(X, y, p)

	##################################################################################
	# TODO: Use StatsModels to create the Linear Model and Output R-squared
	#################################################################################
    X_train = sm.add_constant(X_train)
    X_test = sm.add_constant(X_test)

    model = sm.OLS(y_train, X_train)
    results = model.fit()

	# Prints out the Report
	# TODO: print R-squared, test MSE & train MSE
    print(results.summary())
    print('R-squared: ', results.rsquared)
    print("training MSE is " + str(eval_measures.mse(y_train, results.predict(X_train))))
    print("testing MSE is " + str(eval_measures.mse(y_test, results.predict(X_test))))
