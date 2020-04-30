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
        X = df[['directed_dollars', 'beta']]
        y = df['stock_price_change']
        return X, y

    def classify(classifier):
       classifier.fit(X_train, y_train)
       return classifier.score(X_test, y_test)



    X, y = load_file("directed_dollars2.csv")

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


    #select stock_ticker, donation_amount, candidate_won_lost, stock_price_change,
    #is_democrat, is_senate,is_president, betav, candidate_last, candidate_first
    #from multi join capm on stock_ticker=TICKER where multi.year=2016;








    # select
    #     stock_ticker,
    #     stock_price_change,
    #     sum(directed_dollars * is_president) as directed_dollars_to_pres,
    #     sum(directed_dollars * is_senate) as directed_dollars_to_senate,
    #     sum(directed_dollars) as directed_dollars,
    #     sum(donation_amount) as total_money_donated,
    #     sum(losing_dollars) as lost_money,
    #     sum(winning_dollars) as money_won,
    #     betav
    # from
    # (select
    #     stock_ticker,
    #     donation_amount,
    #     candidate_won_lost,
    #     stock_price_change,
    #     is_democrat,
    #     is_senate,
    #     is_president,
    #     betav,
    #     case
    #         when candidate_won_lost=0
    #         then -1*donation_amount
    #         else donation_amount end as directed_dollars,
    #     donation_amount * candidate_won_lost as winning_dollars,
    #     is_democrat * donation_amount as democrat_dollars,
    #     case
    #         when is_democrat=0
    #         then donation_amount
    #         else 0 end as republican_dollars,
    #     is_democrat * candidate_won_lost as democrat_and_won,
    #     case
    #         when is_democrat=0 and candidate_won_lost=1
    #         then 1 else 0 end as republican_and_won,
    #     case
    #         when candidate_won_lost=1
    #         then donation_amount
    #         else 0 end as winning_dollars,
    #     case
    #         when candidate_won_lost=0
    #         then donation_amount else 0 end as losing_dollars,
    #     candidate_last,
    #     candidate_first
    #     from multi join capm on stock_ticker=TICKER where multi.year=2016)
    # group by stock_ticker;
