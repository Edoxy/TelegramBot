import yfinance as yf

Indexes = ['AAPL', 'MSFT', 'GOOGL', 'AMZN',]
tick = ''
for x in Indexes:
    tick += x + ' '


data = yf.download(tickers=tick, period='60m', interval='2m')
#print(data)
#print(data['DateTime'][-1], (data['DateTime'][-2]))

value = []
TOLL = 0.7
for x in Indexes:
    perc = round(100*(data['Close'][x][-2] / data['Open'][x][0] -1), 3)
    past = round(100*(data['Close'][x][-6] / data['Open'][x][0] -1), 3)
    print (perc, past, (perc -past), x)
    if abs(perc - past) > TOLL :
        value.append([perc, x])


textinfo = 'info:\n'
for x in value:
    textinfo += str(x[0]) + ' ' + x[1] + '\n'

if textinfo != 'info:\n':
    print(textinfo)
#print(data['Close APPL'][-1])
#print(100*(data['Close'][-1] / data['Open'][0] -1))