from datetime import datetime
from dateutil.relativedelta import relativedelta
import time
import urllib.parse as urlparse
from urllib.parse import urlencode
import pandas as pd
import numpy as np
# from scipy.stats import linregress

start = (datetime.now() - relativedelta(years=5)).timestamp() # select a start timestamp
stop = time.time()

params = {
    'period1': int(start),
    'period2': int(stop),
    'interval': '1d',  #1d = daily, 1wk = weekly, 1mo = monthly
    'events': 'history'
}

spy_endpoint = 'https://query1.finance.yahoo.com/v7/finance/download/SPY'
spy_endpoint_parts = list(urlparse.urlparse(spy_endpoint))
spy_endpoint_parts[4] = urlencode(params)
spy_csv = urlparse.urlunparse(spy_endpoint_parts)

ticker = str(input('Ticker: ')).upper()
company_endpoint = 'https://query1.finance.yahoo.com/v7/finance/download/' + ticker
company_endpoint_parts = list(urlparse.urlparse(company_endpoint))
company_endpoint_parts[4] = urlencode(params)
company_csv = urlparse.urlunparse(company_endpoint_parts)

spy_data = pd.read_csv(spy_csv)
spy_data = spy_data[['Date', 'Adj Close']]
spy_data.columns.values[1] = 'SPY Adj Close'

company_data = pd.read_csv(company_csv)
company_data = company_data[['Date', 'Adj Close']]
company_data.columns.values[1] = ticker + ' Adj Close'

data = pd.merge(spy_data, company_data, on='Date')
returns = data.loc[:, data.columns != 'Date'].pct_change().drop(0).values
log_returns = np.log(1 + returns)

beta = (np.cov(log_returns[:,0], log_returns[:,1], bias=True) / np.var(log_returns[:,0]))[0][1]  # calculation of beta based on slope of LSR
print('Beta: ', beta)

# best_fit = linregress(log_returns[:,0], log_returns[:,1])  # another, easier way to calculate
# print('Beta: ', best_fit.slope)


