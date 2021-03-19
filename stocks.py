import yfinance as yf
import pandas as pd
from datetime import date


def InfoStock():
    ## Write the message with the info about the traked indexes ##
    Indexes = ['AAPL', 'MSFT', 'GOOGL', 'AMZN']
    tick = ''
    for x in Indexes:
        tick += x + ' '

    data = GetData(tick)
    data = data.dropna()

    if DateCheck(data):
        value = []

        TOLL = 60
        #changes the index value to numbers
        n_rows = data.shape[0]
        lables = [i for i in range(n_rows)]
        data.set_axis(lables, axis='index', inplace=True)

        textinfo = 'info:\n'
        for x in Indexes:
            data_x = data.loc[[0, n_rows-1, n_rows-3],[('Open', x), ('Close', x)]]
            print(data_x)
            data_x = data_x.values
            percent = round(data_x[1, 1]/data_x[0, 0] * 100 -100, 2)
            diff = round(data_x[1, 1] - data_x[0, 0], 3)
            percent_last = round(data_x[2, 1]/data_x[0, 0] * 100 -100, 2)
            
            delta = round(percent/percent_last *100 - 100, 2)
            if abs(delta) > TOLL:
                textinfo += 'WARNING:\n'

            textinfo += f'{x}\t rating is:  {percent}%\t with:  {diff}\t and delta: {delta}%\n\n'

        if textinfo != 'info:\n':
            print(textinfo)
        return textinfo

    else:
        return 'info:\n'

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
    # download the data
    data = yf.download('AAPL MSFT', period='1d', interval='1m')
    # checks if the dataset is up to date
    print(DateCheck(data))

    data = data.dropna()
    n_rows = data.shape[0]
    print(n_rows)
    lables = [i for i in range(n_rows)]
    data.set_axis(lables, axis='index', inplace=True)
    print(data, data.info())
    x_data = data.loc[[0, n_rows-1], [('Open', 'AAPL'), ('Close', 'AAPL')]]
    print(x_data)
    print(x_data.values)
    print(f'{"AAPL"} rating is {round(100 - x_data.values[1, 1]/x_data.values[0, 0] * 100, 3)} % with {round(x_data.values[0, 0] - x_data.values[1, 1], 3)}')

    InfoStock()