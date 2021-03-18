import yfinance as yf

def InfoStock():
    ## Write the message with the info about the traked indexes ##
    Indexes = ['AAPL', 'MSFT', 'GOOGL', 'AMZN']
    tick = ''
    for x in Indexes:
        tick += x + ' '
    
    
    data = yf.download(tickers=tick, period='1d', interval='1m')

    value = []
    TOLL = 0.7
    for x in Indexes:
        perc = round(100*(data['Close'][x][-1] / data['Open'][x][0] -1), 3)
        past = round(100*(data['Close'][x][-5] / data['Open'][x][0] -1), 3)
        if  True:#abs(perc - past) > TOLL :
            value.append([perc, x])

    textinfo = 'info:\n'
    for x in value:
        textinfo += str(x[0]) + ' ' + x[1] + '\n'

    if textinfo != 'info:\n':
        print(textinfo)
    return textinfo


if __name__ == '__main__':
    print(InfoStock())