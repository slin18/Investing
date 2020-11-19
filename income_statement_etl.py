import pdb
import os
import re
import time
import requests
import json
import pandas as pd
from sqlalchemy import create_engine
import getpass
from datetime import date, datetime
from dateutil.relativedelta import relativedelta

base_path = "./stocks"
api_key = "REGISTER_AT_BELOW_LINK"

# You can get your own API key and sign up with the options provided
# Free option gives you limited requests calls
# https://financialmodelingprep.com/developer/docs/ 

#future development <- input csv file

def directory(path):
    '''Create base directory to store stocks
    Args:
        path - provide directory path
    Returns:
        boolean - whether directory initially exists
    '''
    path_exists = os.path.isdir(path)
    if path_exists == False: os.mkdir(path)
    return path_exists

def stock_input():
    '''Input stocks until user quits
    Returns:
        stocks - list of stock tickers
    '''
    stocks = []
    print("Enter your stock ticker:")
    while True:
        ticker = str(raw_input()).upper()
        if ticker == 'Q' or ticker == 'QUIT': break
        else: stocks.append(ticker)
    return stocks

if __name__ == "__main__":
    print("Does base directory exist?: {0}".format(directory(base_path)))
    stocks = stock_input()
    #stocks = ["FB","MSFT", "DBX", "SNAP", "AMZN", "UBER", "LYFT", "NVDA", "AMD", "INTC", "WORK", "GOOG", "GOOGL", "COST", "EBAY", "HPE", "HD", "JPM", "BAC", "WFC","NFLX","NIKE","JWN", "PEP", "KO", "CRM", "NOW","SBUX","WMT"]:
    for stock_ticker in stocks:
        path = "{0}/{1}".format(base_path, stock_ticker)
        print("Does stock directory exist?: {0}".format(directory(path)))

        income_qtr_statement_url = "https://financialmodelingprep.com/api/v3/income-statement/{0}?period=quarter&apikey={1}".format(stock_ticker, api_key)
        income_yr_statement_url = "https://financialmodelingprep.com/api/v3/income-statement/{0}?&apikey={1}".format(stock_ticker, api_key)
        balance_qtr_sheet_url = "https://financialmodelingprep.com/api/v3/balance-sheet-statement/{0}?period=quarter&apikey={1}".format(stock_ticker, api_key)
        balance_yr_sheet_url = "https://financialmodelingprep.com/api/v3/balance-sheet-statement/{0}?apikey={1}".format(stock_ticker, api_key)
        cash_qtr_flow_url = "https://financialmodelingprep.com/api/v3/cash-flow-statement/{0}?period=quarter&apikey={1}".format(stock_ticker, api_key)
        cash_yr_flow_url = "https://financialmodelingprep.com/api/v3/cash-flow-statement/{0}?apikey={1}".format(stock_ticker, api_key)

        api_filename = {income_qtr_statement_url: "INCOMESTATEMENT_QTR",
                        income_yr_statement_url: "INCOMESTATEMENT_YR",
                        balance_qtr_sheet_url: "BALANCESHEET_QTR",
                        balance_yr_sheet_url: "BALANCESHEET_YR",
                        cash_qtr_flow_url: "CASHFLOW_QTR",
                        cash_yr_flow_url: "CASHFLOW_YR"
                        }
        #print(api_filename.keys())
        for url in api_filename.keys():
            req = requests.get(url)
            filename = '{0}/{1}_{2}.json'.format(path,api_filename[url],stock_ticker)
            data = json.loads(req.content)

            print("Move all statements to stock directory")
            start = time.time()
            try:
                with open(filename, 'w') as fp:
                    json.dump(data, fp)
                print "SUCCESS: Dumping data to {0}".format(filename)
                if(len(data)==0):
                    print "However... your data is empty"
            except:
                print "FAIL: Could not dump data as JSON"
            end = time.time()
            print "Total time to dump data is {} seconds\n".format(round(end-start,2))
