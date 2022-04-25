
import pandas as pd
import numpy as np
# print(data)


### STOCKS DATA ###

df_stocks = pd.read_csv('spy_data.csv')
df_stocks['Date'] = pd.to_datetime(df_stocks['Date'])
df_stocks = df_stocks.set_index('Date')
df_stocks['% Change'] = (df_stocks['Close'] - df_stocks['Open'])/df_stocks['Open']*100 
df_stocks = df_stocks.drop(['High','Low','Open','Close','OpenInt'], axis=1)
df_stocks['% change binned'] = pd.cut(df_stocks['% Change'], [-50,0,50], labels = ['positive', 'negative'])

#print(df_stocks)

### NEW WEATHER DATA ###

df_weather = pd.read_csv('NYCweather-data.csv')
df_weather['Date'] = pd.to_datetime(df_weather['DATE'])
df_weather = df_weather.set_index('DATE')
df_weather['TOTALPRCP'] = df_weather['PRCP'].fillna(0) + df_weather['SNOW'].fillna(0)
df_weather = df_weather.drop(['TAVG','PRCP','SNOW', 'SNWD','STATION'], axis=1)
bins = [-1, 1, 4, 100]
df_weather['binned'] = pd.cut(df_weather['TOTALPRCP'], bins, labels = ['Low', 'Med', 'High'])


#print(df_weather)

df_merged = pd.merge(
    df_stocks,
    df_weather,
    how="left",
    on='Date',
    left_on=None,
    right_on=None,
    left_index=False,
    right_index=False,
    sort=True,
    suffixes=("_x", "_y"),
    copy=True,
    indicator=False,
    validate=None,
)

df_merged = df_merged.set_index('Date')
#print(df_merged)

ag_data = pd.read_csv("dba.us.txt", sep = ",")
ag_data['Date'] = pd.to_datetime(ag_data['Date'])
ag_data = ag_data.set_index('Date')
ag_data['% Change'] = (ag_data['Close'] - ag_data['Open'])/ag_data['Open']*100 
ag_data = ag_data.drop(['High','Low','Open','Close','OpenInt'], axis=1)
ag_data['% change binned'] = pd.cut(ag_data['% Change'], [-50,0,50], labels = ['positive', 'negative'])


ag_merged = pd.merge(
    ag_data,
    df_weather,
    how="left",
    on='Date',
    left_on=None,
    right_on=None,
    left_index=False,
    right_index=False,
    sort=True,
    suffixes=("_x", "_y"),
    copy=True,
    indicator=False,
    validate=None,
)

ag_merged = ag_merged.set_index('Date')
# display DataFrame
#print(ag_merged)


names = ['spy.us.txt', 'ivv.us.txt', 'vti.us.txt', 'voo.us.txt', 'qqq.us.txt', 'vea.us.txt', 'vtv.us.txt', 'iefa.us.txt', 'agg.us.txt', 'bnd.us.txt']
stocks = {}
for stock in names: 
    stocks[stock] = pd.read_csv(stock)
    stocks[stock]['Date'] = pd.to_datetime(stocks[stock]['Date'])
    stocks[stock] = stocks[stock].set_index('Date')
    stocks[stock]['% Change'] = (stocks[stock]['Close'] - stocks[stock]['Open'])/stocks[stock]['Open']*100 
    stocks[stock] = stocks[stock].drop(['High','Low','Open','Close','OpenInt'], axis=1)
    
etfs_avg = pd.concat((stocks['spy.us.txt'], stocks['ivv.us.txt'], stocks['vti.us.txt'], stocks['voo.us.txt']\
                 , stocks['qqq.us.txt'], stocks['vea.us.txt'], stocks['vtv.us.txt'], stocks['iefa.us.txt'], stocks['agg.us.txt'], stocks['bnd.us.txt']))
etfs_avg = etfs_avg.groupby(etfs_avg.index).mean()
etfs_avg['% change binned'] = pd.cut(etfs_avg['% Change'], [-50,0,50], labels = ['positive', 'negative'])

#etfs_avg['Date'] = pd.to_datetime(etfs_avg['Date'])
#etfs_avg = etfs_avg.set_index('Date')
#etfs_avg['% Change'] = (etfs_avg['Close'] - etfs_avg['Open'])/etfs_avg['Open']*100 
#etfs_avg = etfs_avg.drop(['High','Low','Open','Close','OpenInt'], axis=1)
#print(etfs_avg)

etfs_merged = pd.merge(
    etfs_avg,
    df_weather,
    how="left",
    on='Date',
    left_on=None,
    right_on=None,
    left_index=False,
    right_index=False,
    sort=True,
    suffixes=("_x", "_y"),
    copy=True,
    indicator=False,
    validate=None,
)

etfs_merged = etfs_merged.set_index('Date')
print(df_weather.Date['1999-03-10'])
print(etfs_merged)