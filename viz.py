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

#label_encoder = LabelEncoder()
#y = label_encoder.fit_transform(y)

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=0
)



X_train = sm.add_constant(X_train)
X_test = sm.add_constant(X_test)

model = sm.OLS(y, X)
results = model.fit()

# Prints out the Report
print(results.summary())

file = open("data/consolidated-donation-data.csv", 'r')
line = file.readline()
line = file.readline()



years_to_ids_to_win = {}
winners = []
winnersDonations = []
losers = []
losersDonations = []
while line:
    members = line.split(",")
    # print(members[2])
    #print(members)
    try:
        if int(members[3]) == 1:
            #print(members[5][:-2])
            try:
                winnersDonations.append(float(members[2]))
                winners.append(float(members[5][:-2]))
            except ValueError:
                winners.append(0)
        else:
            if int(members[3]) == 0:
                #print(members)
                #print(members[5])
                try:
                    losersDonations.append(float(members[2]))
                    losers.append(float(members[5][:-2]))
                except ValueError:
                    losers.append(0)
    except ValueError:
        print(members)

    # setWinners['2012'].add(members[0])
    # setWinners['2014'].add(members[1])
    # setWinners['2016'].add(members[2])
    line = file.readline()
# print(sum(winners)/len(winners))
# print(sum(losers)/len(losers))
winhist = np.histogram(winners)
# print(winhist)
# plt.hist(winners, bins=winhist[1])
# plt.title("winners histogram")
# plt.show()
loseHist = np.histogram(losers)
# print(loseHist)
# plt.hist(losers, bins=loseHist[1])
# plt.title("losers histogram")
# plt.show()
plt.style.use('seaborn-deep')
testBins = [-2.5, -2, -1.5, -1, -.5, 0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5]
#testBins = [-7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7]
# plt.hist(winners, testBins, alpha=0.5, label='Donated to winners', density=True)
# plt.hist(losers, testBins, alpha=0.5, label='Donated to losers', density=True)
# plt.legend(loc='upper right')
# plt.xlabel('Percent change in stock price')
# plt.ylabel('Percentage of donors')
plt.scatter(winners, winnersDonations,color='blue', alpha=.2)
plt.scatter(losers, losersDonations,color='red', alpha=.2)
plt.show()
# plt.scatter(np.append(np.zeros_like(losers), np.ones_like(winners)), np.append(losers, winners))
#
# X_plot = np.linspace(0,1,100)
# plt.plot(X_plot, X_plot*results.params[0] + results.params[1])

#plt.title('')

plt.show()
