import yfinance as yf
import pandas as pd
from datetime import date

def InfoStock():
    ## Write the message with the info about the traked indexes ##
    Indexes = ['AAPL', 'MSFT', 'GOOGL', 'AMZN']
    tick = ''
    for x in Indexes:
        tick += x + ' '

    data = yf.download(tickers=tick, period='1d', interval='1m')
    # add a function to delete the NaN value from the dataset
    data.dropna()

    value = []
    TOLL = 0.7
    for x in Indexes:
        perc = round(100*(data['Close'][x][-1] / data['Open'][x][0] - 1), 3)
        past = round(100*(data['Close'][x][-5] / data['Open'][x][0] - 1), 3)
        if True:  # abs(perc - past) >= TOLL :
            value.append([perc, x])

    textinfo = 'info:\n'
    for x in value:
        textinfo += str(x[0]) + ' ' + x[1] + '\n'

    if textinfo != 'info:\n':
        print(textinfo)
    return textinfo


def DateCheck(data):
    # Checks the dataframe date
    verify = False
    data_date = data.index[0].strftime('%Y-%m-%d')
    today = date.today().strftime('%Y-%m-%d')
    print(today, data_date)
    if data_date == today:
        verify = True
    return verify


def GetData(tiks):
    return yf.download(tickers=tiks, period='1d', interval='1m')



if __name__ == '__main__':
    #download the data
    data = yf.download('AAPL', period='1d', interval='1m')
    #checks if the dataset is up to date
    print(DateCheck(data))

    data.dropna()