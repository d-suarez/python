import argparse as ap
import csv
import datetime as dt
import pandas as pd
import numpy as np
import qstkutil.qsdateutil as du
import qstkutil.DataAccess as da

argparser = ap.ArgumentParser(description="Takes an order file and outputs a" \
   + " values file.")
   
argparser.add_argument("cash", type=float)
argparser.add_argument("infile")
argparser.add_argument("outfile")

args = argparser.parse_args()

print "Starting with " + str(args.cash) + " dollars."
print "Input file: " + args.infile
print "Values file: " + args.outfile

cash = args.cash


#set up an empty list to store our order information
orders = []

#opening our files with the "with" command ensures that they close automatically
with open(args.infile, "rU") as infile:
  with open(args.outfile, "w") as outfile:
    #set up our reading and writing objects
    reader = csv.reader(infile, "excel")
    writer = csv.writer(outfile)
    #read each row, store the info in the orders list and write it to the values
    #file
    for row in reader:
      orders.append([dt.datetime(int(row[0]), int(row[1]), int(row[2]),16), 
        row[3], row[4], int(row[5])])
      #parrot what we read back into the output file
      writer.writerow(row)

#print our orders to the screen so we can make sure they read correctly
for order in orders:
  print order

#wait for user input
foo = raw_input("\nPress enter\n")

#get our timestamps for our trading days, print them to the screen
startday = min(orders)[0]
endday = max(orders)[0]
endday.replace(hour = 23, minute = 59)
timeofday=dt.timedelta(hours=16)
timestamps = du.getNYSEdays(startday,endday,timeofday)

print "\n\n", timestamps

#wait for user input
bar = raw_input("\nPress enter\n")

#get list of unique symbols
symbols = list(set([order[1] for order in orders]))
#load in data
dataobj = da.DataAccess('Yahoo')
close = dataobj.get_data(timestamps, symbols, "close")

print symbols
print "variable 'close' is ", type(close), " object class"


portafolio = {'GOOG' : 0, 'AAPL':0, 'XOM':0, 'IBM': 0}


orderdates = [order[0] for order in orders]

da = [(timestamp in orderdates) for timestamp in timestamps]

d = ['GOOG', 'AAPL', 'XOM', 'IBM']

le = []
indx = 0
t =[]

stocks = 0
for timestamp in timestamps:
        if timestamp in orderdates:
                while orders[indx][0] == timestamp:
                        if orders[indx][2] == 'Buy':
                                portafolio[orders[indx][1]] += orders[indx][3]
                                cash -= orders[indx][3]*close.ix[timestamp].values[d.index(orders[indx][1])]
                        if orders[indx][2] == 'Sell':
                                portafolio[orders[indx][1]] -= orders[indx][3]
                                cash += orders[indx][3]*close.ix[timestamp].values[d.index(orders[indx][1])]
                        indx += 1
        for k in portafolio:
                t.append(portafolio[k])                   
        stock = np.sum(portafolio.values() * close.ix[timestamp].values)
        total = cash + stock
        le.append([timestamp,cash, stock, total,  t])   
        t = []                    
                        


for l in le:
        print l

