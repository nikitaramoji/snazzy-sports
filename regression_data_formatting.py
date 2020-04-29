# get the line reader past the bull shit header
# data = ''
#
with open('multivar_2016.csv', 'r') as file:
    data = file.read().replace('\"', '')
    #data = file.read().replace('[', '')
with open('multivar_2016.csv', 'w') as file:
    file.write('candidate_last,candidate_first,donation_amount,candidate_won_lost,stock_ticker,stock_price_change,year,opening_price,closing_price,party,chamber,is_democrat,is_senate,is_president\n')
    file.write(data)
# get the line reader past the bull shit header
# with open('data/consolidated_data2.csv', 'w') as file:
#     file.write('candidate_last,candidate_first,donation_amount,candidate_won_lost,stock_ticker,stock_price_change,year,opening_price,closing_price,party,chamber\n')
# for i in range(1, 6):
#     data = ''
#     with open('data/combined_output_data'+ str(i) +'.txt', 'r') as file2:
#         data = file2.read()
#         data = data
#     #data = file.read().replace('[', '')
#     with open('data/consolidated_data2.csv', 'a') as file3:
#         file3.write(data)
