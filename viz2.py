import pandas as pd
from matplotlib import pyplot as plt


# want to plot directed dollars versus performance

def load_file(file_path):
    #candidate,donation_amount,candidate_won_lost,stock_ticker,
    #stock_price_change,year,opening_price,closing_price,party,chamber
    df = pd.read_csv(file_path, delimiter=',')
    df = df.dropna()
    X = df[['directed_dollars_to_pres', 'beta']]
    y = df['stock_price_change']
    return df



df = load_file('directed_dollars2.csv')
print(df['directed_dollars'])

plt.scatter(df['directed_dollars'],df['stock_price_change'])
plt.show()
