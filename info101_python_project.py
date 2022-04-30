from statistics import mode
from os import getcwd
from datetime import datetime
import csv
import collections

def format_output(days, txs, total, cpd, avg, cat, vend, txs_vend, total_month, 
txs_month, total_year, txs_year): #formats output to be easily readable in the terminal
    print('\n////////////////////////////////////////////')
    print('---------------natty\'s amazon---------------')
    print('total days elapsed: ____________________ ' + str(days))
    print('total transactions: ____________________ ' + str(txs))
    print('total purchases: _________________ ~$ ' + str(round(total, 2)))
    print('cost per day: _____________________ ~$ ' + str(round(cpd, 2)))
    print('average purchase: _________________ ~$ ' + str(round(avg, 2)))
    print('fav. category: ___________________ ' + cat)
    print('fav. vendor, # of purchases: ' + vend + ', ' + str(txs_vend))
    print('////////////////////////////////////////////')
    print('---------------month to date----------------')
    print('total purchases: __________________ ~$ ' + str(round(total_month, 2)))
    print('total transactions: ______________________ ' + str(txs_month))
    print('////////////////////////////////////////////')
    print('----------------year to date---------------')
    print('total purchases: ________________ ~$ ' + str(round(total_year, 2)))
    print('total transactions: _____________________ ' + str(txs_year))
    print('////////////////////////////////////////////\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n')
def most_common(list): #returns the most frequent entry of a list
    return(mode(list))
def open_file(file): #a function that opens the .csv and returns each row as an element of a list
    file = open(file)
    csv_reader = csv.reader(file)
    header = [next(csv_reader)]
    rows = []

    for row in csv_reader:
        rows.append(row)
    file.close()
    return rows
def date_at_index(row, list): #returns a formatted date of the row specified
    return datetime.strptime(list[row][0], '%m/%d/%y')
def elem_at_index(row, index, list): #returns the element in the row of the list specified
    return list[row][index]
def net_cost(a, b): #returns float of price times quantity
    return float(a.strip('$'))*int(b)
def time_delta(a, b, list): #returns difference in days between two datetimes
    if(a == 'today'): return (datetime.today() - date_at_index(b, list)).days
    else: return (date_at_index(a, list) - date_at_index(b, list)).days
def last_period(list, days): #returns sum and # of txs for last # of days specified
    difference = time_delta('today', -1, list)
    sum = 0
    txs = 0
    i = len(list) - 1 
    if(difference > days):
        return 'No purchases', 'No txs'
    else:
        while(difference < days):
            sum += net_cost(elem_at_index(i, 12, list), elem_at_index(i , 13, list))
            txs += 1
            i -= 1
            difference = time_delta('today', i, list)
        return sum, txs

rows = open_file(getcwd() + '/Downloads/INFO101-Python-Project-main/amazon_history.csv') #location of amazon .csv

purchase_sum = 0
purchase_cats = []
purchase_vends = []
for i in range(0, len(rows)-1):
    purchase_sum += net_cost(elem_at_index(i, 12, rows), elem_at_index(i , 13, rows)) #12 col is price, 13 is quantity
    purchase_cats.append(elem_at_index(i, 3, rows)) #3 col is categories
    purchase_vends.append(elem_at_index(i, 9, rows)) #9 col is vendors

txs_num = len(rows)
average_purchase = purchase_sum / txs_num
fav_cat = most_common(purchase_cats)
fav_vend, vend_txs = collections.Counter(purchase_vends).most_common(1)[0]
total_days = time_delta(-1, 0, rows)
cost_per_day = purchase_sum / total_days
month_purchase_sum, month_txs = last_period(rows, 31)
year_purchase_sum, year_txs = last_period(rows, 365)

format_output(total_days, txs_num, purchase_sum, cost_per_day, average_purchase, 
fav_cat, fav_vend, vend_txs, month_purchase_sum, month_txs, year_purchase_sum, 
year_txs)
