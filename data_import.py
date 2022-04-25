import pandas as pd
import numpy as np

# # Metadata specs #

# metadata_col_specs = [
#     (0,  12),
#     (12, 21),
#     (21, 31),
#     (31, 38),
#     (38, 41),
#     (41, 72),
#     (72, 76),
#     (76, 80),
#     (80, 86)
# ]

# metadata_names = [
#     "ID",
#     "LATITUDE",
#     "LONGITUDE",
#     "ELEVATION",
#     "STATE",
#     "NAME",
#     "GSN FLAG",
#     "HCN/CRN FLAG",
#     "WMO ID"]

# metadata_dtype = {
#     "ID": str,
#     "STATE": str,
#     "NAME": str,
#     "GSN FLAG": str,
#     "HCN/CRN FLAG": str,
#     "WMO ID": str
#     }


# # Data specs #

# data_header_names = [
#     "ID",
#     "YEAR",
#     "MONTH",
#     "ELEMENT"]

# data_header_col_specs = [
#     (0,  11),
#     (11, 15),
#     (15, 17),
#     (17, 21)]

# data_header_dtypes = {
#     "ID": str,
#     "YEAR": int,
#     "MONTH": int,
#     "ELEMENT": str}

# data_col_names = [[
#     "VALUE" + str(i + 1),
#     "MFLAG" + str(i + 1),
#     "QFLAG" + str(i + 1),
#     "SFLAG" + str(i + 1)]
#     for i in range(31)]
# # Join sub-lists
# data_col_names = sum(data_col_names, [])

# data_replacement_col_names = [[
#     ("VALUE", i + 1),
#     ("MFLAG", i + 1),
#     ("QFLAG", i + 1),
#     ("SFLAG", i + 1)]
#     for i in range(31)]
# # Join sub-lists
# data_replacement_col_names = sum(data_replacement_col_names, [])
# data_replacement_col_names = pd.MultiIndex.from_tuples(
#     data_replacement_col_names,
#     names=['VAR_TYPE', 'DAY'])

# data_col_specs = [[
#     (21 + i * 8, 26 + i * 8),
#     (26 + i * 8, 27 + i * 8),
#     (27 + i * 8, 28 + i * 8),
#     (28 + i * 8, 29 + i * 8)]
#     for i in range(31)]
# data_col_specs = sum(data_col_specs, [])

# data_col_dtypes = [{
#     "VALUE" + str(i + 1): int,
#     "MFLAG" + str(i + 1): str,
#     "QFLAG" + str(i + 1): str,
#     "SFLAG" + str(i + 1): str}
#     for i in range(31)]
# data_header_dtypes.update({k: v for d in data_col_dtypes for k, v in d.items()})


# # Reading functions #

# def read_station_metadata(filename="ghcnd-stations.txt"):
#     """Reads in station metadata

#     :filename: ghcnd station metadata file.
#     :returns: station metadata as a pandas Dataframe

#     """
#     df = pd.read_fwf(filename, metadata_col_specs, names=metadata_names,
#                      index_col='ID', dtype=metadata_dtype)

#     return df


# def read_ghcn_data_file(filename="USW00094789.dly",
#                         variables=None, include_flags=False,
#                         dropna='all'):
#     """Reads in all data from a GHCN .dly data file

#     :param filename: path to file
#     :param variables: list of variables to include in output dataframe
#         e.g. ['TMAX', 'TMIN', 'PRCP']
#     :param include_flags: Whether to include data quality flags in the final output
#     :returns: Pandas dataframe
#     """

#     df = pd.read_fwf(
#         filename,
#         colspecs=data_header_col_specs + data_col_specs,
#         names=data_header_names + data_col_names,
#         index_col=data_header_names,
#         dtype=data_header_dtypes
#         )

#     if variables is not None:
#         df = df[df.index.get_level_values('ELEMENT').isin(variables)]

#     df.columns = data_replacement_col_names

#     if not include_flags:
#         df = df.loc[:, ('VALUE', slice(None))]
#         df.columns = df.columns.droplevel('VAR_TYPE')

#     df = df.stack(level='DAY').unstack(level='ELEMENT')

#     if dropna:
#         df.replace(-9999.0, np.nan, inplace=True)
#         df.dropna(how=dropna, inplace=True)

#     # replace the entire index with the date.
#     # This loses the station ID index column!
#     # This will usuall fail if dropna=False, since months with <31 days
#     # still have day=31 columns
#     df.index = pd.to_datetime(
#         df.index.get_level_values('YEAR') * 10000 +
#         df.index.get_level_values('MONTH') * 100 +
#         df.index.get_level_values('DAY'),
#         format='%Y%m%d')

#     return df

# df = read_ghcn_data_file()
# df['TMAX'] = df['TMAX'] / 10
# #print(df)
# data = df[['PRCP','SNOW','TMAX']].copy(deep=True)
# data['Total Rain/Snow'] = (df['PRCP'].fillna(0)/10) + df['SNOW'].fillna(0)
# bins = [-1, 100, 500, 2000]
# data['binned'] = pd.cut(data['Total Rain/Snow'], bins, labels = ['Low', 'Med', 'High'])


# # print(data)


### STOCKS DATA ###

df_stocks = pd.read_csv('spy_data.csv')
df_stocks['Date'] = pd.to_datetime(df_stocks['Date'])
df_stocks = df_stocks.set_index('Date')
df_stocks['% Change'] = (df_stocks['Close'] - df_stocks['Open'])/df_stocks['Open']*100 
df_stocks = df_stocks.drop(['High','Low','Open','Close','OpenInt'], axis=1)

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

#print(df_merged)

ag_data = pd.read_csv("dba.us.txt", sep = ",")
ag_data['Date'] = pd.to_datetime(ag_data['Date'])
ag_data = ag_data.set_index('Date')
ag_data['% Change'] = (ag_data['Close'] - ag_data['Open'])/ag_data['Open']*100 
ag_data = ag_data.drop(['High','Low','Open','Close','OpenInt'], axis=1)


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
print(df_weather.Date['1999-03-10'])
print(etfs_merged)