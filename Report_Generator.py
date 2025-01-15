from Data_Retrevial import *
from datetime import datetime
import calendar
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import csv
from decimal import Decimal
from fpdf import FPDF

def findBloomBergEmails():
    emails = getGmailData()
    dtDic = {month: index for index, month in enumerate(calendar.month_abbr) if month}

    bloomBergEmails = []
    dtTdy = datetime.today().strftime('%d-%m-%Y')
    
    for email in emails:
        eDate = email[2].split(',')[1].split(':')[0].rsplit(' ', 1)[0].strip().split(' ')
        eDate[1] = str(dtDic[eDate[1]])
        eDate = '-'.join(eDate)

        if eDate == dtTdy and 'bloomberg' in email[0].lower():
            bloomBergEmails.append(email)

    return bloomBergEmails

def getStock(symbol):
    
    stockData = getStockData(symbol)['Global Quote']
    print(stockData)
    
    timeSeries = getDailyTimeSeries(symbol)['Time Series (Daily)']
    intraDayTimeSeries = getIntraDayTimeSeries(symbol)['Time Series (5min)']

    close = []
    dates = []

    interClose = []
    interTimes = []
    '''
    close = [137.0100, 139.9300, 140.2200, 139.6700, 134.7000, 130.6800,
             128.9100, 130.3900, 132.0000, 134.2500, 137.3400, 139.3100,
             135.0700, 138.8100, 142.4400, 145.0600, 145.1400, 140.2600,
             138.6300, 138.2500, 135.3400, 136.9200, 136.0200, 141.9500,
             139.9100, 136.0500, 135.4000, 132.7600, 139.3350, 141.2500,
             140.5200, 141.5400, 140.4100, 139.5600, 143.5900, 143.7100,
             138.0000, 136.9300, 135.7200, 131.6000, 138.0700, 134.8000,
             134.8100, 132.6500, 132.8900, 127.7200, 124.9200, 122.8500,
             118.8500, 117.0000, 121.4400, 121.4000, 124.0400, 123.5100,
             120.8700, 116.2600, 116.0000, 117.8700, 113.3700, 115.5900,
             116.7800, 119.1000, 119.1400, 116.9100, 108.1000, 106.4700,
             127.2500, 130.0000, 124.5800, 122.8600, 118.0800, 116.1400,
             109.0200, 104.7500, 104.9700, 98.9100]
    
    
    dates = ['2024-12-27', '2024-12-26', '2024-12-24', '2024-12-23', '2024-12-20',
             '2024-12-19', '2024-12-18', '2024-12-17', '2024-12-16', '2024-12-13',
             '2024-12-12', '2024-12-11', '2024-12-10', '2024-12-09', '2024-12-06',
             '2024-12-05', '2024-12-04', '2024-12-03', '2024-12-02', '2024-11-29',
             '2024-11-27', '2024-11-26', '2024-11-25', '2024-11-22', '2024-11-21',
             '2024-11-20', '2024-11-19', '2024-11-18', '2024-11-15', '2024-11-14',
             '2024-11-13', '2024-11-12', '2024-11-11', '2024-11-08', '2024-11-07',
             '2024-10-23', '2024-10-22', '2024-10-21', '2024-10-18', '2024-10-17',
             '2024-10-16', '2024-10-15', '2024-10-14', '2024-10-11', '2024-10-10',
             '2024-10-09', '2024-10-08', '2024-10-07', '2024-10-04', '2024-10-03',
             '2024-10-02', '2024-10-01', '2024-09-30', '2024-09-27', '2024-09-26',
             '2024-09-25', '2024-09-24', '2024-09-23', '2024-09-20', '2024-09-19',
             '2024-09-18', '2024-09-17', '2024-09-16', '2024-09-13', '2024-09-12',
             '2024-09-11', '2024-09-10', '2024-09-09', '2024-09-06', '2024-09-05',
             '2024-09-04', '2024-09-03', '2024-08-30', '2024-08-29', '2024-08-28',
             '2024-08-27']

    interClose = [136.6, 136.68, 136.69, 136.66, 136.69, 136.71, 136.66, 136.69, 136.78, 136.77, 136.9502, 136.975, 137.01, 136.989, 137.0, 137.025, 137.12, 136.4,
                  136.78, 136.57, 136.8935, 136.68, 136.2313, 136.53, 136.69, 136.2805, 135.9599, 136.37, 136.0489, 135.835, 135.7, 135.4287, 136.03, 136.16, 136.8638,
                  135.74, 135.9601, 135.81, 135.6399, 135.4499, 136.485, 136.305, 138.6, 138.92, 139.1192, 139.1698, 139.05, 139.245, 139.38, 139.36, 
                  139.35, 139.47, 139.28, 139.28, 139.17, 139.11, 139.27, 139.08, 138.95, 138.86, 138.75, 138.84, 138.8, 138.74, 139.59, 139.66, 139.69, 139.79, 
                  139.73, 139.6988, 139.8391, 139.745, 139.83, 139.74, 139.74, 139.65, 139.66, 139.68, 139.71, 139.73, 139.91, 140.19, 140.165, 139.9392, 140.19, 
                  140.1918, 139.99, 139.9901, 140.1491, 140.015, 140.22, 139.8355, 139.88, 139.82, 139.9401, 140.1649, 139.62, 139.5444, 139.37, 139.499  ]

    interTimes = ['2024-12-27 19:45:00', '2024-12-27 19:30:00', '2024-12-27 19:15:00', '2024-12-27 19:00:00', '2024-12-27 18:45:00', '2024-12-27 18:30:00', '2024-12-27 18:15:00', '2024-12-27 18:00:00', '2024-12-27 17:45:00', '2024-12-27 17:30:00', '2024-12-27 17:15:00', '2024-12-27 17:00:00', '2024-12-27 16:45:00',
                  '2024-12-27 16:30:00', '2024-12-27 16:15:00', '2024-12-27 16:00:00', '2024-12-27 15:45:00', '2024-12-27 15:30:00', '2024-12-27 15:15:00', '2024-12-27 15:00:00', '2024-12-27 14:45:00', '2024-12-27 14:30:00', '2024-12-27 14:15:00', '2024-12-27 14:00:00', '2024-12-27 13:45:00', '2024-12-27 13:30:00', 
                  '2024-12-27 13:15:00', '2024-12-27 13:00:00', '2024-12-27 12:45:00', '2024-12-27 12:30:00', '2024-12-27 12:15:00', '2024-12-27 12:00:00', '2024-12-27 11:45:00', '2024-12-27 11:30:00', '2024-12-27 11:15:00', '2024-12-27 11:00:00', '2024-12-27 10:45:00', '2024-12-27 10:30:00', '2024-12-27 10:15:00', 
                  '2024-12-27 10:00:00', '2024-12-27 09:45:00', '2024-12-27 09:30:00', '2024-12-27 09:15:00', '2024-12-27 09:00:00', '2024-12-27 08:45:00', '2024-12-27 08:30:00', '2024-12-27 08:15:00', '2024-12-27 08:00:00', '2024-12-27 07:45:00', '2024-12-27 07:30:00', '2024-12-27 07:15:00', '2024-12-27 07:00:00', 
                  '2024-12-27 06:45:00', '2024-12-27 06:30:00', '2024-12-27 06:15:00', '2024-12-27 06:00:00', '2024-12-27 05:45:00', '2024-12-27 05:30:00', '2024-12-27 05:15:00', '2024-12-27 05:00:00', '2024-12-27 04:45:00', '2024-12-27 04:30:00', '2024-12-27 04:15:00', '2024-12-27 04:00:00', '2024-12-26 19:45:00', 
                  '2024-12-26 19:30:00', '2024-12-26 19:15:00', '2024-12-26 19:00:00', '2024-12-26 18:45:00', '2024-12-26 18:30:00', '2024-12-26 18:15:00', '2024-12-26 18:00:00', '2024-12-26 17:45:00', '2024-12-26 17:30:00', '2024-12-26 17:15:00', '2024-12-26 17:00:00', '2024-12-26 16:45:00', '2024-12-26 16:30:00', 
                  '2024-12-26 16:15:00', '2024-12-26 16:00:00', '2024-12-26 15:45:00', '2024-12-26 15:30:00', '2024-12-26 15:15:00', '2024-12-26 15:00:00', '2024-12-26 14:45:00', '2024-12-26 14:30:00', '2024-12-26 14:15:00', 
                  '2024-12-26 14:00:00', '2024-12-26 13:45:00', '2024-12-26 13:30:00', '2024-12-26 13:15:00', '2024-12-26 13:00:00', '2024-12-26 12:45:00', '2024-12-26 12:30:00', '2024-12-26 12:15:00', '2024-12-26 12:00:00', '2024-12-26 11:45:00', '2024-12-26 11:30:00', '2024-12-26 11:15:00', '2024-12-26 11:00:00']

    '''
    for day in timeSeries:
        dates.append(day)
        close.append(timeSeries[day]['4. close'])

    for time in intraDayTimeSeries:
        interClose.append(intraDayTimeSeries[time]['4. close'])
        interTimes.append(time)
    
    close = [float(x) for x in close]
    interClose = [float(x) for x in interClose]
    
    close = close[::-1]
    dates = dates[::-1]
    interClose = interClose[::-1]
    interTimes = interTimes[::-1]

    dtDic = {index: month for index, month in enumerate(calendar.month_abbr) if month}
    months = []
    mticks = []

    timeofdays = []
    tticks = []

    for date in dates:
        d = dtDic[int(date.split('-')[1])] + ' ' + date.split('-')[0]
        if d not in months:
            if date.endswith('0',len(date)-3, len(date)-1):
                months.append(d)
                mticks.append(date)
    
    for times in interTimes:
        t = times.split('-')
        t = t[len(t)-1][3:len(t[len(t)-1])-3]
        if t.endswith('00'):
            tticks.append(times)
            timeofdays.append(t)
        
    print(timeofdays)

    start_price = close[0]
    end_price = close[len(close)-1]
    perc = round(((end_price - start_price) / start_price) * 100, 2)
    diff = round((end_price - start_price), 2)
    num_months = len(months)
    gain = ''

    start_price_daily = float(stockData['02. open'])
    end_price_daily = float(stockData['05. price'])
    perc_daily = round(((end_price_daily - start_price_daily) / start_price_daily) * 100, 2)
    diff_daily = round((end_price_daily - start_price_daily), 2)
    gain_daily = ''

    if perc > 0:
        gain = '+'

    if perc_daily > 0:
        gain_daily = '+'

    perc_txt = f'{gain}{diff} USD ({perc}%) in past {num_months} months'
    perc_txt_daily = f'{gain_daily}{diff_daily} USD ({perc_daily}%) Yesterday'

    x = np.array(dates)
    y = np.array(close)

    fig, ax = plt.subplots(facecolor='white')
    ax.plot(x, y)
    ax.set_xticks(mticks)
    ax.set_xticklabels(months)
    ax.set_title(symbol, loc='left', pad=50, fontsize=24)
    ax.text(0,1.125, end_price,transform=ax.transAxes,fontsize=15)
    ax.text(0,1.05, perc_txt,transform=ax.transAxes)
    fig.tight_layout(pad=2)
    fig.subplots_adjust(bottom=0.2)

    plt.savefig('Graphs\\' + symbol + '.png')

    x = np.array(interTimes)
    y = np.array(interClose)

    fig, ax = plt.subplots(facecolor='white')
    ax.plot(x, y)
    ax.set_xticks(tticks)
    ax.set_xticklabels(timeofdays)
    ax.set_title(symbol, loc='left', pad=50, fontsize=24)
    ax.text(0,1.125, end_price_daily,transform=ax.transAxes,fontsize=15)
    ax.text(0,1.05, perc_txt_daily,transform=ax.transAxes)
    fig.tight_layout(pad=2)
    fig.subplots_adjust(bottom=0.2)

    plt.savefig('Graphs\\' + symbol + '_daily.png')

def findNews():

    data = []
    with open('Portfolios\\portfolio.csv', mode='r') as pfile:
        csv_reader = csv.DictReader(pfile)
        for row in csv_reader:
            data.append(row)
    
    portfolios = {}
    for row in data:
        if row['Account'] not in portfolios:
            portfolios[row['Account']] = [{'Symbol': row['Symbol'], 'Shares': row['Shares']}]
        else:
            portfolios[row['Account']].append({'Symbol': row['Symbol'], 'Shares': row['Shares']})

    for portfolio in portfolios:
        for stock in portfolios[portfolio]:
            print(stock)

def createPDF():
    pdf_report = FPDF()
    pdf_report.add_page()
    pdf_report.image('C:\\Users\\cole-\\Documents\\Workspace\\Stock-Analysis\\Graphs\\NVDA.png', x = 10, y = 10, w = 90)
    pdf_report.output('tuto1.pdf', 'F')

if __name__ == '__main__':
    #getStock('NVDA')
    #findNews()
    createPDF()